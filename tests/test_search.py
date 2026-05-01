from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Query, Session

from app.component.category.repository import CategoryRepository
from app.component.product.product import Product
from app.component.product.schema import ProductSearch
from app.component.product.search import Search


def compiled(expr) -> str:
    """Render a SQLAlchemy expression as MySQL SQL with parameters inlined.

    Used to assert the *shape and value* of filters emitted by Search.search,
    not just that `.filter()` was called.
    """
    return str(expr.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True}))


def filter_sqls(mock_query) -> list[str]:
    return [compiled(call.args[0]) for call in mock_query.filter.call_args_list]


def make_search(products=None, category_ids=None):
    """Build a Search instance with a mocked db and category_repository."""
    mock_query = MagicMock(spec=Query)
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = products or []

    mock_db = MagicMock(spec=Session)
    mock_db.query.return_value = mock_query

    mock_category_repository = MagicMock(spec=CategoryRepository)
    mock_category_repository.get_all_children_ids.return_value = category_ids or []

    search = Search.__new__(Search)
    search.db = mock_db
    search.category_repository = mock_category_repository

    return search, mock_query, mock_category_repository


class TestSearchNoFilters:
    def setup_method(self):
        self.search, self.mock_query, self.mock_category_repository = make_search()

    def test_returns_all_products_when_no_filters(self):
        products = [MagicMock(spec=Product), MagicMock(spec=Product)]
        self.mock_query.all.return_value = products

        result = self.search.search(ProductSearch())

        self.mock_query.filter.assert_not_called()
        self.mock_query.all.assert_called_once()
        assert result == products

    def test_returns_empty_list_when_no_products(self):
        result = self.search.search(ProductSearch())

        assert result == []


class TestSearchByTitle:
    def setup_method(self):
        self.search, self.mock_query, _ = make_search()

    def test_applies_filter_when_title_provided(self):
        self.search.search(ProductSearch(title="apple"))

        assert filter_sqls(self.mock_query) == [
            "MATCH (products.title) AGAINST ('apple*' IN BOOLEAN MODE)"
        ]

    def test_no_filter_when_title_is_none(self):
        self.search.search(ProductSearch(title=None))

        self.mock_query.filter.assert_not_called()

    def test_uses_sanitized_title_from_schema(self):
        # ProductSearch strips boolean-mode operators; Search just consumes the
        # already-sanitized value.
        self.search.search(ProductSearch(title="C++ pens"))

        assert filter_sqls(self.mock_query) == [
            "MATCH (products.title) AGAINST ('C  pens*' IN BOOLEAN MODE)"
        ]

    @pytest.mark.parametrize("raw", ["+++", "---", "@@@", "   ", "()*"])
    def test_no_filter_when_title_is_only_operators(self, raw):
        # Schema collapses these to None, so Search applies no filter.
        self.search.search(ProductSearch(title=raw))

        self.mock_query.filter.assert_not_called()


class TestProductSearchTitleSanitization:
    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("apple", "apple"),
            ("C++ pens", "C  pens"),
            ('"foo bar"', "foo bar"),
            ("-apple", "apple"),
            ("rice@home", "rice home"),
            # Non-operator punctuation is left intact - MySQL FT treats it as a separator.
            ("beef  steak!!", "beef  steak!!"),
            ("  spaced  ", "spaced"),
            # Unicode word chars are preserved.
            ("Café", "Café"),
            ("日本茶", "日本茶"),
            ("Bob's apples", "Bob's apples"),
            # Mixed: operators stripped, unicode kept.
            ("+Café -bitter", "Café  bitter"),
        ],
    )
    def test_sanitizes_only_boolean_mode_operators(self, raw, expected):
        assert ProductSearch(title=raw).title == expected

    @pytest.mark.parametrize("raw", ["+++", "---", "@@@", "   ", "()*", ""])
    def test_collapses_to_none_when_nothing_remains(self, raw):
        assert ProductSearch(title=raw).title is None

    def test_none_passes_through(self):
        assert ProductSearch(title=None).title is None


class TestSearchBySku:
    def setup_method(self):
        self.search, self.mock_query, _ = make_search()

    def test_applies_filter_when_sku_provided(self):
        self.search.search(ProductSearch(sku="GRO-BRD-APP-016"))

        assert filter_sqls(self.mock_query) == [
            "products.sku = 'GRO-BRD-APP-016'"
        ]

    def test_no_filter_when_sku_is_none(self):
        self.search.search(ProductSearch(sku=None))

        self.mock_query.filter.assert_not_called()


class TestSearchByPrice:
    def setup_method(self):
        self.search, self.mock_query, _ = make_search()

    def test_applies_filter_for_price_min(self):
        self.search.search(ProductSearch(price_min=Decimal("5.00")))

        assert filter_sqls(self.mock_query) == ["products.price >= 5.00"]

    def test_applies_filter_for_price_max(self):
        self.search.search(ProductSearch(price_max=Decimal("20.00")))

        assert filter_sqls(self.mock_query) == ["products.price <= 20.00"]

    def test_applies_two_filters_for_price_range(self):
        self.search.search(ProductSearch(price_min=Decimal("5.00"), price_max=Decimal("20.00")))

        assert filter_sqls(self.mock_query) == [
            "products.price >= 5.00",
            "products.price <= 20.00",
        ]

    def test_no_filter_when_price_is_none(self):
        self.search.search(ProductSearch(price_min=None, price_max=None))

        self.mock_query.filter.assert_not_called()

    def test_price_min_is_applied_when_zero(self):
        self.search.search(ProductSearch(price_min=Decimal("0.00"), price_max=None))

        assert filter_sqls(self.mock_query) == ["products.price >= 0.00"]

    @pytest.mark.parametrize("bad_value", [Decimal("0"), Decimal("-1.00")])
    def test_price_max_must_be_greater_than_zero(self, bad_value):
        with pytest.raises(ValidationError):
            ProductSearch(price_max=bad_value)


class TestSearchByCategory:
    def setup_method(self):
        self.search, self.mock_query, self.mock_category_repository = make_search()

    def test_applies_filter_when_category_id_provided(self):
        self.mock_category_repository.get_all_children_ids.return_value = [1, 2, 3]

        self.search.search(ProductSearch(category_id=1))

        self.mock_category_repository.get_all_children_ids.assert_called_once_with(1)
        assert filter_sqls(self.mock_query) == [
            "products.category_id IN (1, 2, 3)"
        ]

    def test_resolves_descendant_category_ids(self):
        self.mock_category_repository.get_all_children_ids.return_value = [2, 5, 6]

        self.search.search(ProductSearch(category_id=2))

        self.mock_category_repository.get_all_children_ids.assert_called_once_with(2)
        assert filter_sqls(self.mock_query) == [
            "products.category_id IN (2, 5, 6)"
        ]

    def test_no_filter_when_category_id_is_none(self):
        self.search.search(ProductSearch(category_id=None))

        self.mock_category_repository.get_all_children_ids.assert_not_called()
        self.mock_query.filter.assert_not_called()


class TestSearchCombinedFilters:
    def setup_method(self):
        self.search, self.mock_query, self.mock_category_repository = make_search()

    def test_all_filters_applied(self):
        self.mock_category_repository.get_all_children_ids.return_value = [3]

        self.search.search(ProductSearch(
            title="steak",
            sku="GRO-BRD-BEE-017",
            price_min=Decimal("5.00"),
            price_max=Decimal("50.00"),
            category_id=3,
        ))

        assert filter_sqls(self.mock_query) == [
            "products.category_id IN (3)",
            "products.price >= 5.00",
            "products.price <= 50.00",
            "MATCH (products.title) AGAINST ('steak*' IN BOOLEAN MODE)",
            "products.sku = 'GRO-BRD-BEE-017'",
        ]
        self.mock_category_repository.get_all_children_ids.assert_called_once_with(3)

    def test_returns_results_with_combined_filters(self):
        products = [MagicMock(spec=Product)]
        self.mock_query.all.return_value = products
        self.mock_category_repository.get_all_children_ids.return_value = [1]

        result = self.search.search(ProductSearch(price_min=Decimal("1.00"), category_id=1))

        assert result == products
