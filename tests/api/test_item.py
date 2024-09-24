from moto import mock_aws
from unittest.mock import patch
from app.db.models.item import WeaponModel
from app.db.models.item import ArmorModel
from app.db.models.item import EdibleModel
from app.db.models.item import BattleItemModel
from app.db.models.item import KeyItemModel

@mock_aws
def test_item_list_all(client, config):
    with patch('app.db.models.item.WeaponModel') as mock_weapon_model, \
         patch('app.db.models.item.ArmorModel') as mock_armor_model, \
         patch('app.db.models.item.EdibleModel') as mock_edible_model, \
         patch('app.db.models.item.BattleItemModel') as mock_battle_item_model, \
         patch('app.db.models.item.KeyItemModel') as mock_key_item_model:
        WeaponModel.create_table()
        for weapon in config.mock_items['weapons']:
            WeaponModel(**weapon).save()
        for armor in config.mock_items['armor']:
            ArmorModel(**armor).save()
        for edible in config.mock_items['edibles']:
            EdibleModel(**edible).save()
        for battle_item in config.mock_items['battle_items']:
            BattleItemModel(**battle_item).save()
        for key_item in config.mock_items['key_items']:
            KeyItemModel(**key_item).save()
        mock_weapon_model = WeaponModel
        mock_armor_model = ArmorModel
        mock_edible_model = EdibleModel
        mock_battle_item_model = BattleItemModel
        mock_key_item_model = KeyItemModel
        response = client.get("/item/list/all")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert len(response_json) == 5
    assert len(response_json['weapon']) == 3
    assert len(response_json['armor']) == 2
    assert len(response_json['edible']) == 9
    assert len(response_json['battle_item']) == 5
    assert len(response_json['key_item']) == 5
    assert response_json['weapon'][0]['name'] == 'Baddest Beam'
    assert response_json['armor'][0]['name'] == 'Baseball Cap'
    assert response_json['edible'][0]['name'] == 'Bag of Fries'
    assert response_json['battle_item'][0]['name'] == 'Bag of Dragonite'
    assert response_json['key_item'][0]['name'] == 'ATM Card'

@mock_aws
def test_item_list_weapon(client, config):
    with patch('app.db.models.item.WeaponModel') as mock_weapon_model:
        WeaponModel.create_table()
        for weapon in config.mock_items['weapons']:
            WeaponModel(**weapon).save()
        mock_weapon_model = WeaponModel
        response = client.get("/item/list/weapon")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert len(response_json) == 1
    assert len(response_json['weapon']) == 3
    assert response_json['weapon'][0]['name'] == 'Baddest Beam'

@mock_aws
def test_item_list_armor(client, config):
    with patch('app.db.models.item.ArmorModel') as mock_armor_model:
        ArmorModel.create_table()
        for armor in config.mock_items['armor']:
            ArmorModel(**armor).save()
        mock_armor_model = ArmorModel
        response = client.get("/item/list/armor")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert len(response_json) == 1
    assert len(response_json['armor']) == 2
    assert response_json['armor'][0]['name'] == 'Baseball Cap'

@mock_aws
def test_item_list_edible(client, config):
    with patch('app.db.models.item.EdibleModel') as mock_edible_model:
        EdibleModel.create_table()
        for edible in config.mock_items['edibles']:
            EdibleModel(**edible).save()
        mock_edible_model = EdibleModel
        response = client.get("/item/list/edible")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert len(response_json) == 1
    assert len(response_json['edible']) == 9
    assert response_json['edible'][0]['name'] == 'Bag of Fries'

@mock_aws
def test_item_list_battle_item(client, config):
    with patch('app.db.models.item.BattleItemModel') as mock_battle_item_model:
        BattleItemModel.create_table()
        for battle_item in config.mock_items['battle_items']:
            BattleItemModel(**battle_item).save()
        mock_battle_item_model = BattleItemModel
        response = client.get("/item/list/battle")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert len(response_json) == 1
    assert len(response_json['battle_item']) == 5
    assert response_json['battle_item'][0]['name'] == 'Bag of Dragonite'

@mock_aws
def test_item_list_key_item(client, config):
    with patch('app.db.models.item.KeyItemModel') as mock_key_item_model:
        KeyItemModel.create_table()
        for key_item in config.mock_items['key_items']:
            KeyItemModel(**key_item).save()
        mock_key_item_model = KeyItemModel
        response = client.get("/item/list/key")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert len(response_json) == 1
    assert len(response_json['key_item']) == 5
    assert response_json['key_item'][0]['name'] == 'ATM Card'

@mock_aws
def test_item_list_invalid_type(client, config):
    with patch('app.db.models.item.KeyItemModel') as mock_key_item_model:
        KeyItemModel.create_table()
        for key_item in config.mock_items['key_items']:
            KeyItemModel(**key_item).save()
        mock_key_item_model = KeyItemModel
        response = client.get("/item/list/INVALID")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

@mock_aws
def test_get_item_info(client, config):
    with patch('app.db.models.item.WeaponModel') as mock_weapon_model:
        WeaponModel.create_table()
        for weapon in config.mock_items['weapons']:
            WeaponModel(**weapon).save()
        mock_weapon_model = WeaponModel
        response = client.get("/item/get/weapon/Baddest Beam")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json['name'] == 'Baddest Beam'
    assert response_json['offense'] == 98
    assert response_json['effects'] == 'Repair Broken Harmonica'

    with patch('app.db.models.item.ArmorModel') as mock_armor_model:
        ArmorModel.create_table()
        for armor in config.mock_items['armor']:
            ArmorModel(**armor).save()
        mock_armor_model = ArmorModel
        response = client.get("/item/get/armor/Bracer of Kings")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json['name'] == 'Bracer of Kings'
    assert response_json['defense'] == 30
    assert response_json['equip_slot'] == 'Arms'
    assert response_json['protects'][0] == 'Hypnosis'

@mock_aws
def test_get_item_info_invalid_type(client, config):
    with patch('app.db.models.item.WeaponModel') as mock_weapon_model:
        WeaponModel.create_table()
        for weapon in config.mock_items['weapons']:
            WeaponModel(**weapon).save()
        mock_weapon_model = WeaponModel
        response = client.get("/item/get/asdf/INVALID")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item type not found'}

@mock_aws
def test_get_item_info_invalid_item(client, config):
    with patch('app.db.models.item.WeaponModel') as mock_weapon_model:
        WeaponModel.create_table()
        for weapon in config.mock_items['weapons']:
            WeaponModel(**weapon).save()
        mock_weapon_model = WeaponModel
        response = client.get("/item/get/weapon/INVALID")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}