import unittest
from app.db.models.character import PCModel, NPCModel  # Adjust the import based on your directory structure

class TestPCModel(unittest.TestCase):

    def test_pc_model_initialization(self):
        # Create an instance of PCModel
        pc = PCModel(pk='character', sk='ness', age=13, bio='Trash can digger', hometown='Onett')

        # Assert that attributes are set correctly
        self.assertEqual(pc.pk, 'character')
        self.assertEqual(pc.sk, 'ness')
        self.assertEqual(pc.age, 13)
        self.assertEqual(pc.bio, 'Trash can digger')
        self.assertEqual(pc.hometown, 'Onett')

    def test_pc_model_attributes_nullable(self):
        # Create an instance of PCModel with None values
        pc = PCModel(pk='character', sk='poo', age=None, bio=None, hometown=None)

        # Assert that nullable attributes are None
        self.assertIsNone(pc.age)
        self.assertIsNone(pc.bio)
        self.assertIsNone(pc.hometown)

class TestNPCModel(unittest.TestCase):

    def test_npc_model_initialization(self):
        # Create an instance of NPCModel
        npc = NPCModel(pk='character', sk='mr_everdread', areas=['Twoson', 'cave'], role='Quest Giver')

        # Assert that attributes are set correctly
        self.assertEqual(npc.pk, 'character')
        self.assertEqual(npc.sk, 'mr_everdread')
        self.assertEqual(npc.areas, ['Twoson', 'cave'])
        self.assertEqual(npc.role, 'Quest Giver')

    def test_npc_model_attributes_nullable(self):
        # Create an instance of NPCModel with None values
        npc = NPCModel(pk='character', sk='mr_everdread', areas=None, role=None)

        # Assert that nullable attributes are None
        self.assertIsNone(npc.areas)
        self.assertIsNone(npc.role)

if __name__ == '__main__':
    unittest.main()
