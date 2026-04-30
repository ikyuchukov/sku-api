from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.component.category.manager import CategoryManager
from app.component.product.product import Product
from app.component.product.schema import ProductSearch
from app.component.product.search import Search
from sqlalchemy.orm import Query, Session


def make_search(products=None, category_ids=None):
    """Build a Search instance with a mocked db and category_manager."""
    mock_query = MagicMock(spec=Query)
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = products or []

    mock_db = MagicMock(spec=Session)
    mock_db.query.return_value = mock_query

    mock_category_manager = MagicMock(spec=CategoryManager)
    mock_category_manager.get_all_children_ids.return_value = category_ids or []

    search = Search.__new__(Search)
    search.db = mock_db
    search.category_manager = mock_category_manager

    return search, mock_query, mock_category_manager


class TestSearchNoFilters:
    def setup_method(self):
        self.search, self.mock_query, self.mock_category_manager = make_search()

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

        self.mock_query.filter.assert_called_once()

    def test_no_filter_when_title_is_none(self):
        self.search.search(ProductSearch(title=None))

        self.mock_query.filter.assert_not_called()


class TestSearchBySku:
    def setup_method(self):
        self.search, self.mock_query, _ = make_search()

    def test_applies_filter_when_sku_provided(self):
        self.search.search(ProductSearch(sku="GRO-BRD-APP-016"))

        self.mock_query.filter.assert_called_once()

    def test_no_filter_when_sku_is_none(self):
        self.search.search(ProductSearch(sku=None))

        self.mock_query.filter.assert_not_called()


class TestSearchByPrice:
    def setup_method(self):
        self.search, self.mock_query, _ = make_search()

    def test_applies_filter_for_price_min(self):
        self.search.search(ProductSearch(price_min=Decimal("5.00")))

        self.mock_query.filter.assert_called_once()

    def test_applies_filter_for_price_max(self):
        self.search.search(ProductSearch(price_max=Decimal("20.00")))

        self.mock_query.filter.assert_called_once()

    def test_applies_two_filters_for_price_range(self):
        self.search.search(ProductSearch(price_min=Decimal("5.00"), price_max=Decimal("20.00")))

        assert self.mock_query.filter.call_count == 2

    def test_no_filter_when_price_is_none(self):
        self.search.search(ProductSearch(price_min=None, price_max=None))

        self.mock_query.filter.assert_not_called()


class TestSearchByCategory:
    def setup_method(self):
        self.search, self.mock_query, self.mock_category_manager = make_search()

    def test_applies_filter_when_category_id_provided(self):
        self.mock_category_manager.get_all_children_ids.return_value = [1, 2, 3]

        self.search.search(ProductSearch(category_id=1))

        self.mock_category_manager.get_all_children_ids.assert_called_once_with(1)
        self.mock_query.filter.assert_called_once()

    def test_resolves_descendant_category_ids(self):
        self.mock_category_manager.get_all_children_ids.return_value = [2, 5, 6]

        self.search.search(ProductSearch(category_id=2))

        self.mock_category_manager.get_all_children_ids.assert_called_once_with(2)

    def test_no_filter_when_category_id_is_none(self):
        self.search.search(ProductSearch(category_id=None))

        self.mock_category_manager.get_all_children_ids.assert_not_called()
        self.mock_query.filter.assert_not_called()


class TestSearchCombinedFilters:
    def setup_method(self):
        self.search, self.mock_query, self.mock_category_manager = make_search()

    def test_all_filters_applied(self):
        self.mock_category_manager.get_all_children_ids.return_value = [3]

        self.search.search(ProductSearch(
            title="steak",
            sku="GRO-BRD-BEE-017",
            price_min=Decimal("5.00"),
            price_max=Decimal("50.00"),
            category_id=3,
        ))

        assert self.mock_query.filter.call_count == 5
        self.mock_category_manager.get_all_children_ids.assert_called_once_with(3)

    def test_returns_results_with_combined_filters(self):
        products = [MagicMock(spec=Product)]
        self.mock_query.all.return_value = products
        self.mock_category_manager.get_all_children_ids.return_value = [1]

        result = self.search.search(ProductSearch(price_min=Decimal("1.00"), category_id=1))

        assert result == products
