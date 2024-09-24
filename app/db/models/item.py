from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute
from app.db.models.base import BaseModel


class ItemModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass
    
    item_type = UnicodeAttribute(null=True)
    areas = ListAttribute(null=True)
    used_by = UnicodeAttribute(null=True)
    buy_price = NumberAttribute(null=True)
    sell_price = NumberAttribute(null=True)


class WeaponModel(ItemModel):
    """
    Model for weapon items.
    """
    weapon_type = UnicodeAttribute(null=True)
    offense = NumberAttribute(null=True)
    effects = UnicodeAttribute(null=True)


class ArmorModel(ItemModel):
    """
    Model for armor items.
    """
    armor_type = UnicodeAttribute(null=True)
    equip_slot = UnicodeAttribute(null=True)
    defense = NumberAttribute(null=True)
    luck = NumberAttribute(null=True)
    speed = NumberAttribute(null=True)
    protects = ListAttribute(null=True)


class EdibleModel(ItemModel):
    """
    Model for edible items (e.g., food, healing)
    """
    edible_type = UnicodeAttribute(null=True)
    healing = NumberAttribute(null=True)
    effect_type = UnicodeAttribute(null=True)
    effects = UnicodeAttribute(null=True)
    condiment = UnicodeAttribute(null=True)


class BattleItemModel(ItemModel):
    """
    Model for battle items (e.g., bombs, bottlerockets)
    """
    battle_item_type = UnicodeAttribute(null=True)
    target = UnicodeAttribute(null=True)
    aoe = UnicodeAttribute(null=True)
    effects = UnicodeAttribute(null=True)


class KeyItemModel(ItemModel):
    """
    Model for key items.
    """
    key_item_type = UnicodeAttribute(null=True)
    used_for = UnicodeAttribute(null=True)
