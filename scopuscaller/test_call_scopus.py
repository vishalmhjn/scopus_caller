import os
import unittest
import call_scopus as sc

API_KEY = os.environ["API_KEY"]


class TestDivideByThree(unittest.TestCase):
    def test_caller(self):
        YEAR = 2023
        KEYWORDS = ["predicting", "flows", "speeds", "transfer learning", "open data"]
        df = sc.get_titles(API_KEY, KEYWORDS, YEAR)
        self.assertEqual(
            df.title[0],
            "Predicting network flows from speeds using open data and transfer learning",
        )


unittest.main()
