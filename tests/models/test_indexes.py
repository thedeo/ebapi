import unittest
from app.db.models.indexes import (
    ByAreaIndex, ByItemTypeIndex, ByDataTypeIndex,
    ByEnemyTypeIndex, ByIsBossIndex, ByPsiTypeIndex, ByPsiClassIndex
)

class TestGlobalSecondaryIndexes(unittest.TestCase):

    def test_by_area_index(self):
        # Create an instance of ByAreaIndex
        index = ByAreaIndex()
        
        # Check that the index name and hash key are correct
        self.assertEqual(index.Meta.index_name, 'by-area')

    def test_by_item_type_index(self):
        # Create an instance of ByItemTypeIndex
        index = ByItemTypeIndex()
        
        # Check that the index name and hash key are correct
        self.assertEqual(index.Meta.index_name, 'by-item-type')

    def test_by_data_type_index(self):
        # Create an instance of ByDataTypeIndex
        index = ByDataTypeIndex()
        
        # Check that the index name and hash key are correct
        self.assertEqual(index.Meta.index_name, 'by-data-type')

    def test_by_enemy_type_index(self):
        # Create an instance of ByEnemyTypeIndex
        index = ByEnemyTypeIndex()
        
        # Check that the index name and hash key are correct
        self.assertEqual(index.Meta.index_name, 'by-enemy-type')

    def test_by_is_boss_index(self):
        # Create an instance of ByIsBossIndex
        index = ByIsBossIndex()
        
        # Check that the index name and hash key are correct
        self.assertEqual(index.Meta.index_name, 'by-is-boss')

    def test_by_psi_type_index(self):
        # Create an instance of ByPsiTypeIndex
        index = ByPsiTypeIndex()
        
        # Check that the index name and hash key are correct
        self.assertEqual(index.Meta.index_name, 'by-psi-type')

    def test_by_psi_class_index(self):
        # Create an instance of ByPsiClassIndex
        index = ByPsiClassIndex()
        
        # Check that the index name and hash key are correct
        self.assertEqual(index.Meta.index_name, 'by-psi-class')

if __name__ == '__main__':
    unittest.main()
