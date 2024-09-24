import unittest
from pydantic import ValidationError
from app.db.models.shop import ShopModel, ShopItemModel

class TestShopModels(unittest.TestCase):

    def test_shop_model_creation(self):
        # Create an instance of ShopModel
        shop = ShopModel(area='Main Town')

        # Assertions for the ShopModel
        self.assertEqual(shop.area, 'Main Town')

    def test_shop_item_model_creation(self):
        # Create an instance of ShopItemModel
        shop_item = ShopItemModel(area='Main Town', price=150)

        # Assertions for the ShopItemModel
        self.assertEqual(shop_item.area, 'Main Town')
        self.assertEqual(shop_item.price, 150)

    def test_shop_item_model_with_null_price(self):
        # Create an instance of ShopItemModel with null price
        shop_item = ShopItemModel(area='Main Town', price=None)

        # Assertions for null price
        self.assertEqual(shop_item.area, 'Main Town')
        self.assertIsNone(shop_item.price)

if __name__ == '__main__':
    unittest.main()
