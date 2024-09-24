from moto import mock_aws
from unittest.mock import patch
from app.db.models.psi import PsiModel, PSI_TYPES, PSI_CLASS_TYPE_MAP

@mock_aws
def test_area_list_all(client, config):
    with patch('app.db.models.psi.PsiModel') as mock_model:
        PsiModel.create_table()
        for psi in config.mock_psi:
            PsiModel(**psi).save()
        mock_model = PsiModel
        response = client.get("/psi/list/all")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 7
    assert response_json[5]['id'] == "fire_beta"

@mock_aws
def test_psi_list_classes(client):
    response = client.get("/psi/list/classes")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 5
    assert response_json[1] == "beta"

@mock_aws
def test_psi_list_by_class(client, config):
    with patch('app.db.models.psi.PsiModel') as mock_model:
        PsiModel.create_table()
        for psi in config.mock_psi:
            PsiModel(**psi).save()
        mock_model = PsiModel
        response = client.get("/psi/list/by_class/alpha")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 3
    assert response_json[0]['id'] == "brainshock_alpha"
    assert response_json[1]['id'] == "defense_up_alpha"
    assert response_json[2]['id'] == "fire_alpha"

@mock_aws
def test_psi_list_by_class_not_found(client, config):
    with patch('app.db.models.psi.PsiModel') as mock_model:
        PsiModel.create_table()
        for psi in config.mock_psi:
            PsiModel(**psi).save()
        mock_model = PsiModel
        response = client.get("/psi/list/by_class/trashcan")

    response_json = response.json()
    assert response.status_code == 404
    assert response_json['detail'] == "PSI class not found"

@mock_aws
def test_psi_list_types(client):
    response = client.get("/psi/list/types")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 4
    assert response_json[1] == "defense"

@mock_aws
def test_psi_get(client, config):
    with patch('app.db.models.psi.PsiModel') as mock_model:
        PsiModel.create_table()
        for psi in config.mock_psi:
            PsiModel(**psi).save()
        mock_model = PsiModel
        response = client.get("/psi/Fire α")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json['id'] == "fire_alpha"
    assert response_json['name'] == "PSI Fire α"
    assert response_json['psi_type'] == "Offense"
    assert response_json['psi_class'] == "alpha"
    assert response_json['used_by'] == [ {'level': 3, 'name': 'paula'} ]
    assert response_json['target'] == "enemy"
    assert response_json['pp_cost'] == 6
    assert response_json['aoe'] == "row"
    assert response_json['points'] == { "start": 60, "end": 100 }
    assert response_json['effects'] == "Damage"

@mock_aws
def test_psi_get_not_found(client, config):
    with patch('app.db.models.psi.PsiModel') as mock_model:
        PsiModel.create_table()
        for psi in config.mock_psi:
            PsiModel(**psi).save()
        mock_model = PsiModel
        response = client.get("/psi/Trashcan")

    response_json = response.json()
    assert response.status_code == 404
    assert response_json['detail'] == "PSI not found. Try listing all PSI to find the correct name."