from unittest.mock import MagicMock

import pytest

from app.component.category.category import Category
from app.component.category.manager import CategoryManager
from app.component.category.schema import CategoryDto


class TestBuildCategoryTree:
    def test_single_root_no_children(self):
        categories = [MagicMock(spec=Category, id=1, name="Root", parent_id=None, children=[])]
        result = CategoryManager.build_category_tree(categories)

        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].name == "Root"
        assert result[0].children == []

    def test_flat_list_with_children(self):
        categories = [
            MagicMock(spec=Category, id=1, name="Root", parent_id=None, children=[]),
            MagicMock(spec=Category, id=2, name="Child A", parent_id=1, children=[]),
            MagicMock(spec=Category, id=3, name="Child B", parent_id=1, children=[]),
        ]
        result = CategoryManager.build_category_tree(categories)

        assert len(result) == 1
        root = result[0]
        assert root.id == 1
        assert len(root.children) == 2
        assert [c.id for c in root.children] == [2, 3]

    def test_nested_grandchildren(self):
        categories = [
            MagicMock(spec=Category, id=1, name="Root", parent_id=None, children=[]),
            MagicMock(spec=Category, id=2, name="Child", parent_id=1, children=[]),
            MagicMock(spec=Category, id=3, name="Grandchild", parent_id=2, children=[]),
        ]
        result = CategoryManager.build_category_tree(categories)

        root = result[0]
        assert root.children[0].id == 2
        assert root.children[0].children[0].id == 3
