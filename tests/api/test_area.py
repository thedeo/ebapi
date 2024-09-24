from moto import mock_aws
from unittest.mock import patch
from app.db.models.area import AreaModel

@mock_aws
def test_area_list_all(client, config):
    with patch('app.db.models.area.AreaModel') as mock_model:
        AreaModel.create_table()
        for area in config.mock_areas:
            AreaModel(**area).save()
        mock_model = AreaModel
        response = client.get("/area/list/all")

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.__len__() == 9
    assert response_json[0]['id'] == "mock_giant_step"

