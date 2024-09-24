import unittest
from app.db.models.common import StatsMapAttribute, DropItemAttribute, UsedByMapAttribute

class TestMapAttributes(unittest.TestCase):

    def test_stats_map_attribute(self):
        # Create an instance of StatsMapAttribute
        stats = StatsMapAttribute(hp=100, pp=50, offense=20, defense=15, speed=10, guts=5)
        
        # Check that the attributes are set correctly
        self.assertEqual(stats.hp, 100)
        self.assertEqual(stats.pp, 50)
        self.assertEqual(stats.offense, 20)
        self.assertEqual(stats.defense, 15)
        self.assertEqual(stats.speed, 10)
        self.assertEqual(stats.guts, 5)

        # Test null attributes
        empty_stats = StatsMapAttribute()
        self.assertIsNone(empty_stats.hp)
        self.assertIsNone(empty_stats.pp)

    def test_drop_item_attribute(self):
        # Create an instance of DropItemAttribute
        drop_item = DropItemAttribute(item="Hamburger", chance="1/128")
        
        # Check that the attributes are set correctly
        self.assertEqual(drop_item.item, "Hamburger")
        self.assertEqual(drop_item.chance, "1/128")
        
        # Test null attributes
        empty_drop_item = DropItemAttribute()
        self.assertIsNone(empty_drop_item.item)
        self.assertIsNone(empty_drop_item.chance)

    def test_used_by_map_attribute(self):
        # Create an instance of UsedByMapAttribute
        used_by = UsedByMapAttribute(name="Ness", level=10)
        
        # Check that the attributes are set correctly
        self.assertEqual(used_by.name, "Ness")
        self.assertEqual(used_by.level, 10)

        # Test equality operator
        same_used_by = UsedByMapAttribute(name="Ness", level=10)
        different_used_by = UsedByMapAttribute(name="Paula", level=5)

        self.assertEqual(used_by, same_used_by)
        self.assertNotEqual(used_by, different_used_by)

        # Test hash
        self.assertEqual(hash(used_by), hash(same_used_by))
        self.assertNotEqual(hash(used_by), hash(different_used_by))

if __name__ == "__main__":
    unittest.main()
