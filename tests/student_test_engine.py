from __future__ import annotations

import json
import os
import tempfile
import unittest
from abc_sources import JSONInventorySource
from engine import QueryEngine
from errors import QueryValidationError


def make_sample_inventory_file() -> str:
    data = {
        "world": "Azeron",
        "regions": [
            {
                "name": "Frostvale",
                "dungeons": [
                    {
                        "name": "Grimhold",
                        "rooms": [
                            {
                                "name": "Antechamber",
                                "chests": [
                                    {
                                        "name": "Iron Chest #1",
                                        "items": [
                                            {
                                                "sku": "7F-ICE-BOW",
                                                "name": "Ice Bow",
                                                "rarity": "epic",
                                                "qty": 1,
                                                "base_price": 420.0,
                                                "tags": ["bow", "ice", "ranged"],
                                            },
                                            {
                                                "sku": "HP-POT-SM",
                                                "name": "Small Health Potion",
                                                "rarity": "common",
                                                "qty": 5,
                                                "base_price": 5.0,
                                                "tags": ["potion", "health"],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "name": "Sunreach",
                "dungeons": [
                    {
                        "name": "Amber Vault",
                        "rooms": [
                            {
                                "name": "Treasure Hall",
                                "chests": [
                                    {
                                        "name": "Golden Chest",
                                        "items": [
                                            {
                                                "sku": "SR-SWD-LG",
                                                "name": "Sunreach Greatsword",
                                                "rarity": "rare",
                                                "qty": 1,
                                                "base_price": 250.0,
                                                "tags": ["sword", "two-handed"],
                                            },
                                            {
                                                "sku": "MP-POT-MD",
                                                "name": "Medium Mana Potion",
                                                "rarity": "uncommon",
                                                "qty": 3,
                                                "base_price": 12.0,
                                                "tags": ["potion", "mana"],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
        ],
        "version": 1,
    }

    temp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
    )

    with temp:
        json.dump(data, temp)
    return temp.name

class EngineTests(unittest.TestCase):
    def make_engine(self) -> tuple[QueryEngine, str]:
        path = make_sample_inventory_file()
        return QueryEngine(JSONInventorySource(path)), path

    def test_filter_only_returns_matching_items(self):
        engine, path = self.make_engine()
        try:
            items = list(engine.filter_items(lambda item: item.rarity == "rare"))
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].name, "Sunreach Greatsword")
            self.assertTrue(all(item.rarity == "rare" for item in items))
        finally:
            os.remove(path)

    def test_find_item_by_sku_finds_first_and_last_sorted_skus(self):
        engine, path = self.make_engine()
        try:
            items = sorted(engine.walk_items(), key=lambda item: item.sku)
            first = engine.find_item_by_sku(items[0].sku)
            last = engine.find_item_by_sku(items[-1].sku)
            self.assertEqual(first, items[0])
            self.assertEqual(last, items[-1])
        finally:
            os.remove(path)

    def test_reduce_can_collect_names(self):
        engine, path = self.make_engine()

        try:
            names = engine.reduce_items(
                lambda acc, item: acc + [item.name],
                [],
            )

            self.assertEqual(
                names,
                [
                    "Ice Bow",
                    "Small Health Potion",
                    "Sunreach Greatsword",
                    "Medium Mana Potion",
                ],
            )
        finally:
            os.remove(path)

    def test_non_callable_predicate_raises(self):
        engine, path = self.make_engine()

        try:
            with self.assertRaises(QueryValidationError):
                list(engine.filter_items("not callable"))
        finally:
            os.remove(path)

    def test_predicate_exception_is_preserved_as_cause(self):
        engine, path = self.make_engine()

        def broken_predicate(_item):
            raise ValueError("boom")

        try:
            with self.assertRaises(QueryValidationError) as context:
                list(engine.filter_items(broken_predicate))

            self.assertIsInstance(context.exception.__cause__, ValueError)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()