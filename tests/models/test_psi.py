import unittest
from app.db.models.psi import PsiModel, PointsRange
from app.db.models.common import UsedByMapAttribute


class TestPsiModel(unittest.TestCase):

    def test_psi_model_attributes(self):
        # Create a PsiModel object with all attributes populated
        psi = PsiModel(
            psi_type='offense',
            psi_class='α',
            used_by=[
                UsedByMapAttribute(name='Ness', level=5),
                UsedByMapAttribute(name='Paula', level=7)
            ],
            target='enemy',
            pp_cost=10,
            aoe='single',
            points=PointsRange(start=50, end=100),
            effects='Fire damage'
        )

        # Assertions for top-level attributes
        self.assertEqual(psi.psi_type, 'offense')
        self.assertEqual(psi.psi_class, 'α')
        self.assertEqual(psi.target, 'enemy')
        self.assertEqual(psi.pp_cost, 10)
        self.assertEqual(psi.aoe, 'single')
        self.assertEqual(psi.effects, 'Fire damage')

        # Assertions for nested ListAttribute used_by
        self.assertEqual(len(psi.used_by), 2)
        self.assertEqual(psi.used_by[0].name, 'Ness')
        self.assertEqual(psi.used_by[0].level, 5)
        self.assertEqual(psi.used_by[1].name, 'Paula')
        self.assertEqual(psi.used_by[1].level, 7)

        # Assertions for the nested PointsRange attribute
        self.assertIsInstance(psi.points, PointsRange)
        self.assertEqual(psi.points.start, 50)
        self.assertEqual(psi.points.end, 100)

    def test_psi_model_with_null_attributes(self):
        # Test PsiModel with some null attributes
        psi = PsiModel(
            psi_type=None,
            psi_class=None,
            used_by=None,
            target=None,
            pp_cost=None,
            aoe=None,
            points=None,
            effects=None
        )

        # Assertions for null attributes
        self.assertIsNone(psi.psi_type)
        self.assertIsNone(psi.psi_class)
        self.assertIsNone(psi.used_by)
        self.assertIsNone(psi.target)
        self.assertIsNone(psi.pp_cost)
        self.assertIsNone(psi.aoe)
        self.assertIsNone(psi.points)
        self.assertIsNone(psi.effects)

    def test_points_range(self):
        # Create a PointsRange object
        points_range = PointsRange(start=10, end=30)

        # Assertions for PointsRange
        self.assertEqual(points_range.start, 10)
        self.assertEqual(points_range.end, 30)

        # Test PointsRange with None
        points_range = PointsRange(start=None, end=None)
        self.assertIsNone(points_range.start)
        self.assertIsNone(points_range.end)

    def test_used_by_map_attribute(self):
        # Create UsedByMapAttribute object
        used_by = UsedByMapAttribute(name='Poo', level=3)

        # Assertions for UsedByMapAttribute
        self.assertEqual(used_by.name, 'Poo')
        self.assertEqual(used_by.level, 3)

        # Test UsedByMapAttribute with None values
        used_by = UsedByMapAttribute(name=None, level=None)
        self.assertIsNone(used_by.name)
        self.assertIsNone(used_by.level)


if __name__ == '__main__':
    unittest.main()
