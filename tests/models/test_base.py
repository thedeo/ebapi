import unittest
from app.db.models.base import BaseModel
from app.settings import API_DATA_TABLE, AWS_REGION

class TestBaseModel(unittest.TestCase):

    def test_base_model_initialization(self):
        # Create an instance of BaseModel
        base_model_instance = BaseModel(pk='123', sk='456', name='Test Item')

        # Assert that attributes are set correctly
        self.assertEqual(base_model_instance.pk, '123')
        self.assertEqual(base_model_instance.sk, '456')
        self.assertEqual(base_model_instance.name, 'Test Item')

    def test_base_model_indexes(self):
        # Create an instance of BaseModel
        base_model_instance = BaseModel(pk='123', sk='456', name='Test Item')

        # Check that the indexes are initialized correctly
        self.assertTrue(hasattr(base_model_instance, 'by_area_index'))
        self.assertTrue(hasattr(base_model_instance, 'by_item_type_index'))
        self.assertTrue(hasattr(base_model_instance, 'by_data_type_index'))
        self.assertTrue(hasattr(base_model_instance, 'by_enemy_type_index'))
        self.assertTrue(hasattr(base_model_instance, 'by_is_boss_index'))
        self.assertTrue(hasattr(base_model_instance, 'by_psi_type_index'))
        self.assertTrue(hasattr(base_model_instance, 'by_psi_class_index'))

    def test_base_model_meta_configuration(self):
        # Check that the Meta class has the correct table name and region
        self.assertEqual(BaseModel.Meta.table_name, API_DATA_TABLE)
        self.assertEqual(BaseModel.Meta.region, AWS_REGION)

if __name__ == '__main__':
    unittest.main()
