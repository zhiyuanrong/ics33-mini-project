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
        yield from self._walk_node(self.source.root())

    @validate_predicate
    def filter_items(self, pred: Callable[[Item], bool]) -> Iterator[Item]:
        # TODO: Yield matching items lazily.
        for item in self.walk_items():
            if pred(item):
                yield item


    def map_items(self, fn: Callable[[Item], T]) -> Iterator[T]:
        # TODO: Yield mapped values lazily.
        for item in self.walk_items():
            yield fn(item)

    def reduce_items(self, reducer: Callable[[U, Item], U], initial: U) -> U:
        # TODO: Fold all items from the traversal into an accumulator.
        total = initial
        for item in self.walk_items():
            total = reducer(total , item)
        return total


    def find_item_by_sku(self, sku: str) -> Item | None:
        """Sort by SKU and use a student-written binary-search loop.

        Linear search, dictionary lookup, and the bisect module do not satisfy
        the assignment requirement.
        """
        # TODO: Materialize, sort, and implement lo/hi/mid binary search.
        all_items = []
        for item in self.walk_items():
            all_items.append(item)
            all_items.sort(key=lambda item: item.sku)
        lo = 0
        hi = len(all_items)-1
        while lo <= hi:
            mid = (lo+hi)//2
            mid_sku = all_items[mid].sku
            if mid_sku == sku:
                return all_items[mid]
            elif mid_sku < sku:
                lo = mid+1
            else:
                hi = mid-1
        return None




