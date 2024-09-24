import unittest
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute
from app.db.models.common import StatsMapAttribute, DropItemAttribute
from app.db.models.base import BaseModel
from app.db.models.enemy import EnemyModel, EnemyResistanceModel, EnemyAbilityModel, EnemyByAreaModel

class TestEnemyModels(unittest.TestCase):

    def test_enemy_model(self):
        # Create an instance of EnemyModel
        enemy = EnemyModel(
            areas=['Twoson', 'Fourside'],
            is_boss='TRUE',
            data_type='profile',
            enemy_type='insect',
            initial_status='Poisoned',
            stats=StatsMapAttribute(hp=200, offense=50, defense=30),
            exp_reward=100,
            money_reward=50,
            drop=DropItemAttribute(item='Cookie', chance='1/128'),
            battle_tip='Use Fire attacks'
        )
        
        # Check attribute values
        self.assertEqual(enemy.areas, ['Twoson', 'Fourside'])
        self.assertEqual(enemy.is_boss, 'TRUE')
        self.assertEqual(enemy.data_type, 'profile')
        self.assertEqual(enemy.enemy_type, 'insect')
        self.assertEqual(enemy.initial_status, 'Poisoned')
        self.assertEqual(enemy.stats.hp, 200)
        self.assertEqual(enemy.stats.offense, 50)
        self.assertEqual(enemy.exp_reward, 100)
        self.assertEqual(enemy.money_reward, 50)
        self.assertEqual(enemy.drop.item, 'Cookie')
        self.assertEqual(enemy.drop.chance, '1/128')
        self.assertEqual(enemy.battle_tip, 'Use Fire attacks')

    def test_enemy_resistance_model(self):
        # Create an instance of EnemyResistanceModel
        resistance = EnemyResistanceModel(
            data_type='resistance',
            resistance_type='PSI Fire',
            resistance_value=50
        )
        
        # Check attribute values
        self.assertEqual(resistance.data_type, 'resistance')
        self.assertEqual(resistance.resistance_type, 'PSI Fire')
        self.assertEqual(resistance.resistance_value, 50)

    def test_enemy_ability_model(self):
        # Create an instance of EnemyAbilityModel
        ability = EnemyAbilityModel(
            data_type='ability',
            ability_target='single',
            ability_aoe='none',
            ability_effect=''
        )
        
        # Check attribute values
        self.assertEqual(ability.data_type, 'ability')
        self.assertEqual(ability.ability_target, 'single')
        self.assertEqual(ability.ability_aoe, 'none')
        self.assertEqual(ability.ability_effect, '')

    def test_enemy_by_area_model(self):
        # Create an instance of EnemyByAreaModel
        enemy_by_area = EnemyByAreaModel(
            area='Twoson'
        )
        
        # Check attribute values
        self.assertEqual(enemy_by_area.area, 'Twoson')

if __name__ == "__main__":
    unittest.main()
