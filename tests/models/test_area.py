import unittest
from app.db.models.area import AreaModel

class TestAreaModel(unittest.TestCase):

    def test_area_model_initialization(self):
        # Create an instance of AreaModel with a primary_area value
        area = AreaModel(primary_area='Test Area')

        # Assert that the primary_area attribute is set correctly
        self.assertEqual(area.primary_area, 'Test Area')

    def test_area_model_initialization_with_none(self):
        # Create an instance of AreaModel with a None value
        area = AreaModel()

        # Assert that the primary_area attribute is None
        self.assertIsNone(area.primary_area)

    def test_area_model_attributes(self):
        # Check the attributes of the AreaModel
        area = AreaModel(primary_area='Test Area')
        self.assertTrue(hasattr(area, 'primary_area'))
        self.assertIsInstance(area.primary_area, str)

if __name__ == '__main__':
    unittest.main()
