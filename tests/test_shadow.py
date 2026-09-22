import unittest

from colibri_shadow import parse_route_record, shadow_recommendation


class ShadowTests(unittest.TestCase):
    def test_parses_upstream_trace_format(self):
        record = parse_route_record("4 0 12 3:0.75 7:0.25")
        self.assertEqual(record.layer, 12)
        self.assertEqual(record.experts, ((3, 0.75), (7, 0.25)))

    def test_recommendation_cannot_apply_itself(self):
        result = shadow_recommendation(parse_route_record("4 0 12 3:0.25 7:0.75"), 1)
        self.assertEqual(result["recommended_experts"], [7])
        self.assertEqual(result["authority"], "colibri-native")
        self.assertFalse(result["applied"])

    def test_rejects_malformed_or_duplicate_experts(self):
        for line in ("bad", "1 2 3", "1 2 3 4:0.5 4:0.5"):
            with self.subTest(line=line), self.assertRaises(ValueError):
                parse_route_record(line)


if __name__ == "__main__":
    unittest.main()
