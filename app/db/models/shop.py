from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from app.db.models.base import BaseModel

class ShopModel(BaseModel):
    """
    Base model for shops in a database.
    """
    class Meta(BaseModel.Meta):
        pass
    
    area = UnicodeAttribute(null=False)

class ShopItemModel(ShopModel):
    """
    Model for items within shops, inheriting from ShopModel.
    """
    class Meta(ShopModel.Meta):
        pass
    
    price = NumberAttribute(null=True)
