from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, TypeVar

from abc_sources import InventorySource
from decorators import logged_query, validate_predicate
from models import Item

T = TypeVar("T")
U = TypeVar("U")


class QueryEngine:
    """Queries over a hierarchical inventory source."""

    def __init__(self, source: InventorySource):
        self.source = source

    def _walk_node(self, node: Any) -> Iterator[Item]:
        """Yield Items lazily in documented JSON order.

        You may implement this traversal recursively or with an explicit stack.
        Do not first build a complete list of Item objects.
        """
        # TODO: Implement the traversal. This unreachable yield keeps the stub a
        # generator without doing the students' work for them.
        if isinstance(node, dict):
            if "items" in node:
                for item_data in node["items"]:
                    yield Item(
                        sku=item_data["sku"],
                        name=item_data["name"],
                        rarity=item_data["rarity"],
                        qty=item_data["qty"],
                        base_price=item_data["base_price"],
                        tags=item_data["tags"],
                    )
            else:
                for value in node.values():
                    yield from self._walk_node(value)

        elif isinstance(node, list):
            for element in node:
                yield from self._walk_node(element)


    @logged_query
    def walk_items(self) -> Iterator[Item]:
        # TODO: Delegate lazily to _walk_node(self.source.root()).
        raise NotImplementedError
        yield  # pragma: no cover

    @validate_predicate
    def filter_items(self, pred: Callable[[Item], bool]) -> Iterator[Item]:
        # TODO: Yield matching items lazily.
        raise NotImplementedError
        yield  # pragma: no cover

    def map_items(self, fn: Callable[[Item], T]) -> Iterator[T]:
        # TODO: Yield mapped values lazily.
        raise NotImplementedError
        yield  # pragma: no cover

    def reduce_items(self, reducer: Callable[[U, Item], U], initial: U) -> U:
        # TODO: Fold all items from the traversal into an accumulator.
        raise NotImplementedError

    def find_item_by_sku(self, sku: str) -> Item | None:
        """Sort by SKU and use a student-written binary-search loop.

        Linear search, dictionary lookup, and the bisect module do not satisfy
        the assignment requirement.
        """
        # TODO: Materialize, sort, and implement lo/hi/mid binary search.
        raise NotImplementedError
