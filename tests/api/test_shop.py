from moto import mock_aws
from unittest.mock import patch
from app.db.models.shop import ShopModel, ShopItemModel

@mock_aws
def test_shop_list_all(client, config):
    with patch('app.db.models.shop.ShopModel') as mock_shop_model:
        ShopModel.create_table()
        for shop in config.mock_shops:
            ShopModel(**shop).save()
        mock_shop_model = ShopModel
        response = client.get("/shop/list/all")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json.__len__() == 60
    assert response_json[0]['id'] == "burglin_park_bakery"
    assert response_json[0]['name'] == "Burglin Park Bakery"

@mock_aws
def test_shop_list_by_area(client, config):
    with patch('app.db.models.shop.ShopModel') as mock_shop_model:
        ShopModel.create_table()
        for shop in config.mock_shops:
            ShopModel(**shop).save()
        for shop_item in config.mock_shop_items:
            ShopItemModel(**shop_item).save()
        mock_shop_model = ShopModel
        mock_item_model = ShopItemModel
        response = client.get("/shop/list/by_area/Twoson")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json.__len__() == 10
    assert response_json[0]['id'] == "burglin_park_bakery"
    assert response_json[0]['name'] == "Burglin Park Bakery"

@mock_aws
def test_shop_get(client, config):
    with patch('app.db.models.shop.ShopItemModel') as mock_model:
        ShopItemModel.create_table()
        for shop_item in config.mock_shop_items:
            ShopItemModel(**shop_item).save()
        mock_model = ShopItemModel
        response = client.get("/shop/burglin_park_bakery?detail=true")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json.__len__() == 6
    assert response_json[0]['id'] == "bread_roll"
    assert response_json[0]['name'] == "Bread Roll"
    assert response_json[0]['price'] == 12
    assert response_json[1]['id'] == "can_of_fruit_juice"
    assert response_json[1]['name'] == "Can of Fruit Juice"
    assert response_json[1]['price'] == 4

@mock_aws
def test_shop_get_not_found(client, config):
    with patch('app.db.models.shop.ShopItemModel') as mock_model:
        ShopItemModel.create_table()
        for shop_item in config.mock_shop_items:
            ShopItemModel(**shop_item).save()
        mock_model = ShopItemModel
        response = client.get("/shop/trashcan")

    response_json = response.json()
    print(response_json)
    assert response.status_code == 404
    assert response_json['detail'] == "Shop not found"