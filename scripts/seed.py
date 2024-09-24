import os
import csv
import glob
from tqdm import tqdm

from app.db.models.base import BaseModel
from app.db.models.character import PCModel, NPCModel
from app.db.models.enemy import EnemyModel, EnemyResistanceModel, EnemyAbilityModel, EnemyByAreaModel
from app.db.models.enemy import DropItemAttribute
from app.db.models.item import WeaponModel, ArmorModel, EdibleModel, BattleItemModel, KeyItemModel
from app.db.models.psi import PsiModel, PointsRange, UsedByMapAttribute
from app.db.models.area import AreaModel
from app.db.models.shop import ShopModel, ShopItemModel
from app.db.models.common import StatsMapAttribute

from app.common import normalize_name, parse_foe_stats
from app.settings import API_DATA_TABLE

# Path to the seed data folder
DATA_DIR = 'scripts/data/'


def create_table_if_not_exists():
    if not BaseModel.exists():
        BaseModel.create_table(billing_mode='PAY_PER_REQUEST', wait=True)
        print(f"Table '{API_DATA_TABLE}' created.")


def load_seed_files(data_dir):
    """
    Load all CSV files with "seed_" prefix into memory.
    """
    seed_files = glob.glob(os.path.join(data_dir, 'seed_*.csv'))
    file_data = {}
    
    for file_path in seed_files:
        file_name = os.path.basename(file_path)
        key = file_name.split('.')[0]  # Use file name without extension as key
        with open(file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            file_data[key] = list(reader)  # Store the file content as list of rows
    return file_data


def seed_table(model_class, pk, sk, data):
    """Helper function to seed a DynamoDB table."""
    item = model_class(
        pk=pk,
        sk=sk,
        **data  # Unpack the rest of the data as attributes
    )
    item.save()

def seed_pc_characters(data):
    for row in tqdm(data, desc="Player Characters", unit="character"):
        name = row['name']

        pk = 'character'
        sk = f"pc#{normalize_name(name)}"
        data = {
            "name": name,
            "age": int(row.get('age', 0)) if row.get('age') else None,
            "bio": row.get('bio'),
            "hometown": row.get('hometown'),
        }
        seed_table(PCModel, pk, sk, data)


def seed_npc_characters(data):
    for row in tqdm(data, desc="NPC Characters", unit="character"):
        name = row['name']
        areas = row['areas'].split('/')
        role = row['role']
        
        pk = 'character'
        sk = f"npc#{normalize_name(name)}"

        npc_data = {
            'name': name,
            'areas': areas,
            'role': role
        }

        seed_table(NPCModel, pk, sk, npc_data)


def seed_enemies(data):
    """
    Seed the enemies table with the given data.
    
    The data will be split into different data models based on data_type
    """
    for row in tqdm(data, desc="Enemies", unit="enemy"):
        name = row['name']
        name_normalized = normalize_name(name)
        data_type = row.get('data_type')

        is_boss = str(row.get('is_boss'))
        if row.get('is_boss') == 'TRUE':
            pk='boss'
        else:
            pk='enemy'

        if data_type == 'profile':
            stats, areas = parse_foe_stats(row)
            sk = f"{name_normalized}#detail"

            drop = {
                "item": row.get('drop_item', None),
                "chance": row.get('drop_chance', None)
            }
            enemy = {
                "name": name,
                "data_type": data_type,
                "is_boss": is_boss,
                "areas": areas,
                "enemy_type": row.get('enemy_type'),
                "initial_status": row.get('initial_status'),
                "stats": StatsMapAttribute(**stats) if stats else None,
                "exp_reward": int(row.get('exp_reward')),
                "money_reward": int(row.get('money_reward')),
                "drop": DropItemAttribute(**drop) if drop else None,
                "battle_tip": row.get('battle_tip')
            }
            seed_table(EnemyModel, pk, sk, enemy)

        if data_type == 'resistance':
            resistance_name = row.get('resistance_name')
            resistance_name_normalized = normalize_name(resistance_name)
            sk = f"{name_normalized}#{data_type}#{resistance_name_normalized}"
            resistance = {
                "name": resistance_name,
                "data_type": data_type,
                "resistance_type": row.get('resistance_type'),
                "resistance_value": int(row.get('resistance_value'))
            }
            seed_table(EnemyResistanceModel, pk, sk, resistance)

        if data_type == 'ability':
            ability_name = row.get('ability_name')
            ability_name_normalized = normalize_name(ability_name)
            sk = f"{name_normalized}#{data_type}#{ability_name_normalized}"
            ability = {
                "name": ability_name,
                "data_type": data_type,
                "ability_target": row.get('ability_target'),
                "ability_aoe": row.get('ability_aoe'),
                "ability_effect": row.get('ability_effect')
            }
            seed_table(EnemyAbilityModel, pk, sk, ability)

        for area in areas:
            area_sk = f"area#{normalize_name(area)}#{name_normalized}"
            enemy_area_entry = {
                "name": name,
                "area": area
            }
            seed_table(EnemyByAreaModel, pk, area_sk, enemy_area_entry)


def seed_weapons(data):
    for row in tqdm(data, desc="Weapons", unit="item"):
        item_type = 'weapon'
        name = row['name']
        pk = 'item'
        sk = f"{normalize_name(name)}"
        weapon = {
            "name": name,
            "areas": row.get('areas', None).split('/') if row.get('areas') else None,
            "used_by": row.get('used_by'),
            "buy_price": int(row.get('buy_price', 0)) if row.get('buy_price') else None,
            "sell_price": int(row.get('sell_price', 0)) if row.get('sell_price') else None,
            "item_type": item_type,
            "offense": int(row.get('offense', 0)) if row.get('offense') else None,
            "effects": row.get('effects')
        }
        seed_table(WeaponModel, pk, sk, weapon)


def seed_armor(data):
    for row in tqdm(data, desc="Armor", unit="item"):
        item_type = 'armor'
        name = row['name']
        pk = 'item'
        sk = f"{normalize_name(name)}"
        armor = {
            "name": name,
            "areas": row.get('areas', '').split('/') if row.get('areas') else None,
            "used_by": row.get('used_by'),
            "buy_price": int(row.get('buy_price')),
            "sell_price": int(row.get('sell_price')),
            "item_type": item_type,
            "equip_slot": row.get('equip_slot'),
            "defense": int(row.get('defense', None)) if row.get('defense', None) is not None else None,
            "luck": int(row.get('luck', None)) if row.get('luck', None) is not None else None,
            "speed": int(row.get('speed', None)) if row.get('speed', None) is not None else None,
            "protects": row.get('protects', '').split('/') if row.get('protects') else None,
        }
        seed_table(ArmorModel, pk, sk, armor)


def seed_edibles(data):
    for row in tqdm(data, desc="Edible", unit="item"):
        item_type = 'edible'
        name = row['name']
        pk = 'item'
        sk = f"{normalize_name(name)}"
        edible = {
            "name": name,
            "areas": row.get('areas', '').split('/') if row.get('areas') else None,
            "used_by": row.get('used_by', '').split('/') if row.get('used_by') else None,
            "buy_price": int(row.get('buy_price', 0)) if row.get('buy_price') else None,
            "sell_price": int(row.get('sell_price', 0)) if row.get('sell_price') else None,
            "item_type": item_type,
            "healing": int(row.get('healing', 0)) if row.get('healing') else None,
            "effect_type": row.get('effect_type'),
            "effects": row.get('effects'),
            "condiment": row.get('condiment')
        }
        seed_table(EdibleModel, pk, sk, edible)


def seed_battle_items(data):
    for row in tqdm(data, desc="Battle Item", unit="item"):
        item_type = 'battle_item'
        name = row['name']
        pk = 'item'
        sk = f"{normalize_name(name)}"
        battle_item = {
            "name": name,
            "areas": row.get('areas', '').split('/') if row.get('areas') else None,
            "used_by": row.get('used_by'),
            "buy_price": int(row.get('buy_price', 0)) if row.get('buy_price') else None,
            "sell_price": int(row.get('sell_price', 0)) if row.get('sell_price') else None,
            "item_type": item_type,
            "target": row.get('target'),
            "aoe": row.get('aoe'),
            "effects": row.get('effects'),
        }
        seed_table(BattleItemModel, pk, sk, battle_item)


def seed_key_items(data):
    for row in tqdm(data, desc="Key Item", unit="item"):
        item_type = 'key_item'
        name = row['name']
        pk = 'item'
        sk = f"{normalize_name(name)}"
        key_item = {
            "name": name,
            "areas": row.get('areas', '').split('/') if row.get('areas') else None,
            "used_by": row.get('used_by', ''),
            "item_type": item_type,
            "buy_price": int(row.get('buy_price', 0)) if row.get('buy_price') else None,
            "sell_price": int(row.get('sell_price', 0)) if row.get('sell_price') else None,
            "used_for": row.get('used_for')
        }
        seed_table(KeyItemModel, pk, sk, key_item)


def seed_psi(data):
    for row in tqdm(data, desc="PSI", unit="psi"):
        name = row['name']
        pk = 'psi'
        sk = row['id']

        # Parse the 'used_by' data
        used_by_data = row.get('used_by', '').split('/') if row.get('used_by') else []
        used_by = [UsedByMapAttribute(name=entry.split(':')[0], level=int(entry.split(':')[1])) for entry in used_by_data if entry]

        # Parse the 'points' range
        points = None
        points_range = row.get('points', None).split('-')
        if points_range and len(points_range) == 2:
            points = PointsRange(start=int(points_range[0]), end=int(points_range[1]))

        psi = {
            "name": name,
            "psi_type": row.get('psi_type'),
            "psi_class": row.get('psi_class'),
            "used_by": used_by if used_by else None,
            "target": row.get('target'),
            "pp_cost": int(row.get('pp_cost', 0)) if row.get('pp_cost') else None,
            "aoe": row.get('aoe'),
            "points": points,
            "effects": row.get('effects')
        }
        seed_table(PsiModel, pk, sk, psi)


def seed_areas(data):
    for row in tqdm(data, desc="Areas", unit="area"):
        name = row['name']
        pk = 'area'
        sk = f"{normalize_name(name)}#detail"
        area = {
            "name": name,
            "primary_area": row.get('primary_area'),
        }
        seed_table(AreaModel, pk, sk, area)


def seed_shops(data):
    shops = []
    pk = 'shop'
    for row in tqdm(data, desc="Shops", unit="shop"):
        name = row['name']
        if name not in shops:
            shops.append(name)
            shop_sk = f"shop#{normalize_name(name)}#detail"
            shop = {
                "name": name,
                "area": row.get('area'),
            }
            seed_table(ShopModel, pk, shop_sk, shop)
        shop_item_sk = f"{normalize_name(name)}#item#{normalize_name(row.get('item'))}"
        shop_item = {
            "name": row.get('item'),
            "price": int(row.get('price')) if row.get('price') else None,
            "area": row.get('area'),
        }
        seed_table(ShopItemModel, pk, shop_item_sk, shop_item)


def main():
    print("Creating table if not exists...")
    create_table_if_not_exists()

    print("Loading data into memory...")
    data = load_seed_files(DATA_DIR)

    print("Seeding database...")
    seed_pc_characters(data['seed_player_characters'])
    seed_npc_characters(data['seed_nonplayer_characters'])
    seed_enemies(data['seed_enemies'])
    seed_weapons(data['seed_weapons'])
    seed_armor(data['seed_armor'])
    seed_edibles(data['seed_edibles'])
    seed_battle_items(data['seed_battle_items'])
    seed_key_items(data['seed_key_items'])
    seed_psi(data['seed_psi'])
    seed_areas(data['seed_areas'])
    seed_shops(data['seed_shops'])
    
    print("Database seeding completed.")

if __name__ == "__main__":
    main()
