import unittest
from datetime import date

from expense_tracker import validators as v


class TestValidators(unittest.TestCase):
    def test_amount_ok(self):
        self.assertEqual(v.parse_amount(" 12.5 "), 12.5)

    def test_amount_bad(self):
        for bad in ("abc", "0", "-5", "nan", "inf"):
            with self.assertRaises(v.ValidationError):
                v.parse_amount(bad)

    def test_date_default_and_future(self):
        today = date(2026, 5, 10)
        self.assertEqual(v.parse_date("", today), "2026-05-10")
        with self.assertRaises(v.ValidationError):
            v.parse_date("2026-05-11", today)
        with self.assertRaises(v.ValidationError):
            v.parse_date("10/05/2026", today)

    def test_category(self):
        self.assertEqual(v.parse_category("food"), "Food")
        with self.assertRaises(v.ValidationError):
            v.parse_category("Pets")

    def test_month(self):
        self.assertEqual(v.parse_month("2026-03"), "2026-03")
        with self.assertRaises(v.ValidationError):
            v.parse_month("03-2026")
