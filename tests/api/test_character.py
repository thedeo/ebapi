from moto import mock_aws
from unittest.mock import patch
from app.db.models.character import PCModel
from app.db.models.character import NPCModel


@mock_aws
def test_character_list_all(client, config):
    with patch('app.db.models.character.PCModel') as mock_pc_model, \
         patch('app.db.models.character.NPCModel') as mock_npc_model:
        PCModel.create_table()
        NPCModel.create_table()
        for character in config.mock_pc_characters:
            PCModel(**character).save()
        for character in config.mock_npc_characters:
            NPCModel(**character).save()
        mock_pc_model = PCModel
        mock_npc_model = NPCModel
        response = client.get("/character/list/all")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json[1]['name'] == "Mock Ness"
    assert response_json[1]['age'] == 13
    assert response_json[1]['hometown'] == "Onett"
    assert response_json[1]['bio'] == "Loves to eat burgers from trash cans."
    assert 'pk' not in response_json[1]
    assert response_json[5]['name'] == "Mock Buzz Buzz"
    assert response_json[5]['areas'][0] == "Onett"
    assert response_json[5]['role'] == "Quest Giver"
    assert 'pk' not in response_json[5]


@mock_aws
def test_character_list_pc(client, config):
    with patch('app.db.models.character.PCModel') as mock_model:
        PCModel.create_table()
        for character in config.mock_pc_characters:
            PCModel(**character).save()
        mock_model = PCModel
        response = client.get("/character/list/pc")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json[1]['name'] == "Mock Ness"
    assert response_json[1]['age'] == 13
    assert response_json[1]['hometown'] == "Onett"
    assert response_json[1]['bio'] == "Loves to eat burgers from trash cans."
    assert 'pk' not in response_json[1]


@mock_aws
def test_character_list_npc(client, config):
    with patch('app.db.models.character.NPCModel') as mock_model:
        NPCModel.create_table()
        for character in config.mock_npc_characters:
            NPCModel(**character).save()
        mock_model = NPCModel
        response = client.get("/character/list/npc")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json[1]['name'] == "Mock Buzz Buzz"
    assert response_json[1]['areas'][0] == "Onett"
    assert response_json[1]['role'] == "Quest Giver"
    assert 'pk' not in response_json[1]


@mock_aws
def test_list_npc_characters_by_area(client, config):
    with patch('app.db.models.character.NPCModel') as mock_model:
        NPCModel.create_table()
        for character in config.mock_npc_characters:
            NPCModel(**character).save()
        mock_model = NPCModel
        response = client.get("/character/list/npc/Onett")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 4
    assert response_json[0]['name'] == "Mock Buzz Buzz"
    assert response_json[0]['areas'][0] == "Onett"
    assert response_json[0]['role'] == "Quest Giver"
    assert 'pk' not in response_json[0]


@mock_aws
def test_get_pc_info(client, config):
    with patch('app.db.models.character.PCModel') as mock_model:
        PCModel.create_table()
        for character in config.mock_pc_characters:
            PCModel(**character).save()
        mock_model = PCModel
        response = client.get("/character/pc/mockness")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json['name'] == "Mock Ness"
    assert response_json['age'] == 13
    assert response_json['hometown'] == "Onett"
    assert 'pk' not in response_json


@mock_aws
def test_get_npc_info(client, config):
    with patch('app.db.models.character.NPCModel') as mock_model:
        NPCModel.create_table()
        for character in config.mock_npc_characters:
            NPCModel(**character).save()
        mock_model = NPCModel
        response = client.get("/character/npc/mockbuzzbuzz")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json['name'] == "Mock Buzz Buzz"
    assert response_json['areas'][0] == "Onett"
    assert response_json['role'] == "Quest Giver"
    assert 'pk' not in response_json


@mock_aws
def test_get_pc_info_not_found(client, config):
    with patch('app.db.models.character.PCModel') as mock_model:
        PCModel.create_table()
        for character in config.mock_pc_characters:
            PCModel(**character).save()
        mock_model = PCModel
        response = client.get("/character/pc/notfound")

    assert response.status_code == 404
    assert response.json() == {"detail": "PC not found"}


@mock_aws
def test_get_npc_info_not_found(client, config):
    with patch('app.db.models.character.NPCModel') as mock_model:
        NPCModel.create_table()
        for character in config.mock_npc_characters:
            NPCModel(**character).save()
        mock_model = NPCModel
        response = client.get("/character/npc/notfound")

    assert response.status_code == 404
    assert response.json() == {"detail": "NPC not found"}
