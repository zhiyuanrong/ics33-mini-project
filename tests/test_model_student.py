from models import Item
from unittest import TestCase
from dataclasses import FrozenInstanceError

class test_module(TestCase):
    def test_item_stores_all_fields(self):
        item = Item(
            sku="HP-POT-SM",
            name="Small Health Potion",
            rarity="common",
            qty=5,
            base_price=5.0,
            tags=["potion", "health"],
        )

        self.assertEqual(item.sku, "HP-POT-SM")
        self.assertEqual(item.name, "Small Health Potion")
        self.assertEqual(item.rarity, "common")
        self.assertEqual(item.qty, 5)
        self.assertEqual(item.base_price, 5.0)
        self.assertEqual(item.tags, ["potion", "health"])

    def test_item_is_frozen(self):
        item = Item("A", "Arrow", "common", 2, 1.5, ["ammo"])
        with self.assertRaises(FrozenInstanceError):
            item.qty = 10