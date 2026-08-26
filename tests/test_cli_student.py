from __future__ import annotations

import io
import os
import unittest
from contextlib import redirect_stdout

import cli as guild_cli


SAMPLE = os.path.join(os.path.dirname(__file__), "..", "data", "sample_small.json")
class StudentCliTests(unittest.TestCase):
    def run_command(self, command: list[str]) -> tuple[int, list[str]]:
        args = guild_cli.build_parser().parse_args([SAMPLE, *command])
        output = io.StringIO()
        with redirect_stdout(output):
            result = args.func(args)
        lines = [
            line
            for line in output.getvalue().splitlines()
            if not line.startswith("[LOG]")
        ]
        return result, lines

    def test_list_without_rarity_prints_all_items(self):
        result, lines = self.run_command(["list"])

        self.assertEqual(result, 0)
        self.assertEqual(len(lines), 4)
        self.assertIn("Ice Bow", lines[0])
        self.assertIn("Medium Mana Potion", lines[-1])

    def test_list_with_rarity_prints_only_matching_items(self):
        result, lines = self.run_command(["list", "--rarity", "epic"])

        self.assertEqual(result, 0)
        self.assertEqual(len(lines), 1)
        self.assertIn("7F-ICE-BOW", lines[0])
        self.assertIn("Ice Bow", lines[0])

    def test_find_existing_sku_prints_item_and_returns_zero(self):
        result, lines = self.run_command(["find", "--sku", "SR-SWD-LG"])

        self.assertEqual(result, 0)
        self.assertEqual(len(lines), 1)
        self.assertIn("SR-SWD-LG", lines[0])
        self.assertIn("Sunreach Greatsword", lines[0])

    def test_find_missing_sku_prints_not_found_and_returns_one(self):
        result, lines = self.run_command(["find", "--sku", "NO-SUCH-SKU"])

        self.assertEqual(result, 1)
        self.assertEqual(lines[-1], "Not found")

    def test_value_without_rarity_prints_total_with_two_decimals(self):
        result, lines = self.run_command(["value"])

        self.assertEqual(result, 0)
        self.assertEqual(lines[-1], "731.00")

    def test_value_with_rarity_prints_filtered_total(self):
        result, lines = self.run_command(["value", "--rarity", "uncommon"])

        self.assertEqual(result, 0)
        self.assertEqual(lines[-1], "36.00")

