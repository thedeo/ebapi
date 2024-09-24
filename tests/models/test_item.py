import unittest
from app.db.models.item import (
    ItemModel, WeaponModel, ArmorModel, EdibleModel, BattleItemModel, KeyItemModel
)

class TestItemModels(unittest.TestCase):
    
    def test_item_model_attributes(self):
        item = ItemModel(
            item_type="general",
            areas=["Area 1", "Area 2"],
            used_by="Character A",
            buy_price=100,
            sell_price=50
        )
        self.assertEqual(item.item_type, "general")
        self.assertEqual(item.areas, ["Area 1", "Area 2"])
        self.assertEqual(item.used_by, "Character A")
        self.assertEqual(item.buy_price, 100)
        self.assertEqual(item.sell_price, 50)

    def test_weapon_model_attributes(self):
        weapon = WeaponModel(
            item_type="weapon",
            areas=["Area 1"],
            used_by="Hero",
            buy_price=200,
            sell_price=100,
            weapon_type="Sword",
            offense=50,
            effects="Fire"
        )
        self.assertEqual(weapon.item_type, "weapon")
        self.assertEqual(weapon.areas, ["Area 1"])
        self.assertEqual(weapon.used_by, "Hero")
        self.assertEqual(weapon.buy_price, 200)
        self.assertEqual(weapon.sell_price, 100)
        self.assertEqual(weapon.weapon_type, "Sword")
        self.assertEqual(weapon.offense, 50)
        self.assertEqual(weapon.effects, "Fire")

    def test_armor_model_attributes(self):
        armor = ArmorModel(
            item_type="armor",
            areas=["Area 2"],
            used_by="Warrior",
            buy_price=150,
            sell_price=75,
            armor_type="Helmet",
            equip_slot="Head",
            defense=30,
            luck=10,
            speed=5,
            protects=["Fire", "Ice"]
        )
        self.assertEqual(armor.item_type, "armor")
        self.assertEqual(armor.areas, ["Area 2"])
        self.assertEqual(armor.used_by, "Warrior")
        self.assertEqual(armor.buy_price, 150)
        self.assertEqual(armor.sell_price, 75)
        self.assertEqual(armor.armor_type, "Helmet")
        self.assertEqual(armor.equip_slot, "Head")
        self.assertEqual(armor.defense, 30)
        self.assertEqual(armor.luck, 10)
        self.assertEqual(armor.speed, 5)
        self.assertEqual(armor.protects, ["Fire", "Ice"])

    def test_edible_model_attributes(self):
        edible = EdibleModel(
            item_type="food",
            areas=["Area 3"],
            used_by="Mage",
            buy_price=50,
            sell_price=25,
            edible_type="Healing Herb",
            healing=20,
            effect_type="Healing",
            effects="Cure poison",
            condiment="Salt"
        )
        self.assertEqual(edible.item_type, "food")
        self.assertEqual(edible.areas, ["Area 3"])
        self.assertEqual(edible.used_by, "Mage")
        self.assertEqual(edible.buy_price, 50)
        self.assertEqual(edible.sell_price, 25)
        self.assertEqual(edible.edible_type, "Healing Herb")
        self.assertEqual(edible.healing, 20)
        self.assertEqual(edible.effect_type, "Healing")
        self.assertEqual(edible.effects, "Cure poison")
        self.assertEqual(edible.condiment, "Salt")

    def test_battle_item_model_attributes(self):
        battle_item = BattleItemModel(
            item_type="battle item",
            areas=["Area 4"],
            used_by="Thief",
            buy_price=300,
            sell_price=150,
            battle_item_type="Bomb",
            target="Enemy",
            aoe="Single",
            effects="Explosion"
        )
        self.assertEqual(battle_item.item_type, "battle item")
        self.assertEqual(battle_item.areas, ["Area 4"])
        self.assertEqual(battle_item.used_by, "Thief")
        self.assertEqual(battle_item.buy_price, 300)
        self.assertEqual(battle_item.sell_price, 150)
        self.assertEqual(battle_item.battle_item_type, "Bomb")
        self.assertEqual(battle_item.target, "Enemy")
        self.assertEqual(battle_item.aoe, "Single")
        self.assertEqual(battle_item.effects, "Explosion")

    def test_key_item_model_attributes(self):
        key_item = KeyItemModel(
            item_type="key item",
            areas=["Area 5"],
            used_by="Prince",
            buy_price=None,
            sell_price=None,
            key_item_type="Royal Key",
            used_for="Unlock palace"
        )
        self.assertEqual(key_item.item_type, "key item")
        self.assertEqual(key_item.areas, ["Area 5"])
        self.assertEqual(key_item.used_by, "Prince")
        self.assertEqual(key_item.buy_price, None)
        self.assertEqual(key_item.sell_price, None)
        self.assertEqual(key_item.key_item_type, "Royal Key")
        self.assertEqual(key_item.used_for, "Unlock palace")


if __name__ == '__main__':
    unittest.main()
