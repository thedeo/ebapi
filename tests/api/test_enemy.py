from moto import mock_aws
from unittest.mock import patch
from app.db.models.enemy import EnemyModel
from app.db.models.enemy import EnemyResistanceModel
from app.db.models.enemy import EnemyAbilityModel
from app.db.models.enemy import EnemyByAreaModel

@mock_aws
def test_enemy_list_all(client, config):
    with patch('app.db.models.enemy.EnemyModel') as mock_model:
        EnemyModel.create_table()
        for enemy in config.mock_enemies:
            EnemyModel(**enemy).save()
        mock_model = EnemyModel
        response = client.get("/enemy/list/all")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 3
    assert response_json[0]['id'] == "mock_abstract_art"

@mock_aws
def test_enemy_list_plain(client, config):
    with patch('app.db.models.enemy.EnemyModel') as mock_model:
        EnemyModel.create_table()
        for enemy in config.mock_enemies:
            EnemyModel(**enemy).save()
        mock_model = EnemyModel
        response = client.get("/enemy/list/plain?detail=true")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 2
    for enemy in response_json:
        assert enemy['is_boss'] == "FALSE"

@mock_aws
def test_enemy_list_bosses(client, config):
    with patch('app.db.models.enemy.EnemyModel') as mock_model:
        EnemyModel.create_table()
        for enemy in config.mock_enemies:
            EnemyModel(**enemy).save()
        mock_model = EnemyModel
        response = client.get("/enemy/list/bosses?detail=true")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 1
    for enemy in response_json:
        assert enemy['is_boss'] == "TRUE"

@mock_aws
def test_enemy_list_types(client):
    response = client.get("/enemy/list/types")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 3
    assert response_json[1] == "insect"

@mock_aws
def test_enemy_list_by_type(client, config):
    with patch('app.db.models.enemy.EnemyModel') as mock_model:
        EnemyModel.create_table()
        for enemy in config.mock_enemies:
            EnemyModel(**enemy).save()
        mock_model = EnemyModel
        response = client.get("/enemy/list/by_type/insect?detail=true")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 1
    assert response_json[0]['enemy_type'] == "insect"
    assert response_json[0]['id'] == "mock_annoying_reveler"

@mock_aws
def test_enemy_list_by_area(client, config):
    with patch('app.db.models.enemy.EnemyByAreaModel') as mock_model:
        EnemyByAreaModel.create_table()
        for enemy in config.mock_enemy_areas:
            EnemyByAreaModel(**enemy).save()
        mock_model = EnemyByAreaModel
        response = client.get("/enemy/list/by_area/Cave of the Past")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 7
    assert response_json[0]['id'] == "bionic_kraken"

@mock_aws
def test_enemy_get(client, config):
    with patch('app.db.models.enemy.EnemyModel') as mock_model:
        EnemyModel.create_table()
        for enemy in config.mock_enemies:
            EnemyModel(**enemy).save()
        mock_model = EnemyModel
        response = client.get("/enemy/Mock Abstract Art")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json['profile']['id'] == "mock_abstract_art"
    assert response_json['profile']['name'] == "Mock Abstract Art"

@mock_aws
def test_enemy_get_detail(client, config):
    with patch('app.db.models.enemy.EnemyModel') as mock_model, \
         patch('app.db.models.enemy.EnemyAbilityModel') as mock_ability, \
         patch('app.db.models.enemy.EnemyResistanceModel') as mock_resistance:
        EnemyModel.create_table()
        for enemy in config.mock_enemies:
            EnemyModel(**enemy).save()
        for ability in config.mock_enemy_abilities:
            EnemyAbilityModel(**ability).save()
        for resistance in config.mock_enemy_resistances:
            EnemyResistanceModel(**resistance).save()
        mock_model = EnemyModel
        response = client.get("/enemy/Mock Abstract Art?detail=true")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json['abilities'].__len__() == 2
    assert response_json['resistances'].__len__() == 1
    assert response_json['abilities'][0]['name'] == "Confuse"
    assert response_json['resistances'][0]['name'] == "Confusion"
    assert response_json['profile']['name'] == "Mock Abstract Art"

@mock_aws
def test_enemy_get_not_found(client, config):
    with patch('app.db.models.enemy.EnemyModel') as mock_model:
        EnemyModel.create_table()
        for enemy in config.mock_enemies:
            EnemyModel(**enemy).save()
        mock_model = EnemyModel
        response = client.get("/enemy/Burger King")

    response_json = response.json()
    assert response.status_code == 404
    assert response_json['detail'] == "Enemy not found"
