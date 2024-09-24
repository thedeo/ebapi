import unittest
from unittest.mock import MagicMock, patch
from app.common import normalize_name, replace_greek_letters, parse_foe_stats, extract_attributes
from app.db.models.psi import PSI_CLASS_TYPE_MAP

class TestCommonFunctions(unittest.TestCase):

    def test_normalize_name(self):
        self.assertEqual(normalize_name("Fuzzy Pickles!"), "fuzzy_pickles")
        self.assertEqual(normalize_name("Special@Chars#"), "specialchars")
        self.assertEqual(normalize_name("Multiple   Spaces"), "multiple_spaces")
        self.assertEqual(normalize_name("PSI fire!"), "psi_fire")

    def test_replace_greek_letters(self):
        # Assuming PSI_CLASS_TYPE_MAP contains Greek letter mappings
        greek_map = {
            'α': 'alpha',
            'β': 'beta',
            'γ': 'gamma'
        }
        
        global PSI_CLASS_TYPE_MAP
        PSI_CLASS_TYPE_MAP = greek_map
        
        self.assertEqual(replace_greek_letters("α β γ"), "alpha beta gamma")
        self.assertEqual(replace_greek_letters("No Greek"), "No Greek")
        self.assertEqual(replace_greek_letters("α and γ"), "alpha and gamma")

    def test_parse_foe_stats(self):
        row = {
            'hp': '100',
            'pp': '50',
            'offense': '30',
            'defense': '20',
            'spd': '15',
            'guts': '10',
            'areas': 'area1/area2'
        }
        stats, areas = parse_foe_stats(row)
        expected_stats = {
            'hp': 100,
            'pp': 50,
            'offense': 30,
            'defense': 20,
            'speed': 15,
            'guts': 10
        }
        self.assertEqual(stats, expected_stats)
        self.assertEqual(areas, ['area1', 'area2'])

        # Test with missing keys
        row_missing = {'areas': 'area1/area2'}
        stats, areas = parse_foe_stats(row_missing)
        expected_stats_missing = {
            'hp': 0,
            'pp': 0,
            'offense': 0,
            'defense': 0,
            'speed': 0,
            'guts': 0
        }
        self.assertEqual(stats, expected_stats_missing)
        self.assertEqual(areas, ['area1', 'area2'])

    def test_extract_attributes(self):
        # Create mock items with attribute_values
        item_mock = MagicMock()
        item_mock.attribute_values = {
            'pk': 'partition_key',
            'sk': 'sort_key',
            'data_type': 'example_type',
            'attr1': 'value1',
            'attr2': MagicMock()
        }

        from app.db.models.common import StatsMapAttribute
        item_mock.attribute_values['attr2'] = StatsMapAttribute()  # Mocking a custom attribute type

        # Mock the behavior of the custom attribute's extract_attributes call
        def mock_extract_attributes(value):
            return {'mocked': True}

        # Patch the extract_attributes function
        with patch('app.common.extract_attributes', side_effect=mock_extract_attributes) as mock_extract:
            result = extract_attributes(item_mock)

        expected_result = {
            'attr1': 'value1',
            'attr2': {'mocked': True}
        }

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
