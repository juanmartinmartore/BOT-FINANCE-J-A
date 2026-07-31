import unittest

from src.fetchers.macro import _parse_dolar_futuro_payload
from src.fetchers.stocks import _calculate_change_pct


class FetcherRegressionTests(unittest.TestCase):
    def test_parse_dolar_futuro_payload_from_list(self):
        payload = [["vencimiento", "valor"], ["Sep 2026", "1250"], ["Oct 2026", "1280"]]
        self.assertEqual(
            _parse_dolar_futuro_payload(payload),
            "Sep 2026: $1250 | Oct 2026: $1280"
        )

    def test_parse_dolar_futuro_payload_from_dict(self):
        payload = {"data": [{"mes": "Nov 2026", "valor": "1300"}]}
        self.assertEqual(_parse_dolar_futuro_payload(payload), "Nov 2026: $1300")

    def test_calculate_change_pct(self):
        self.assertEqual(_calculate_change_pct(110, 100), 10.0)
        self.assertEqual(_calculate_change_pct(100, 110), -9.09)


if __name__ == "__main__":
    unittest.main()
