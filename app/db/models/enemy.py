from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute
from app.db.models.base import BaseModel
from app.db.models.common import StatsMapAttribute, DropItemAttribute

class EnemyModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    ENEMY_TYPES = [
        'normal',
        'insect',
        'metallic',
    ]
    
    areas = ListAttribute(null=True)
    is_boss = UnicodeAttribute(null=True)
    data_type = UnicodeAttribute()
    enemy_type = UnicodeAttribute(null=True)
    initial_status = UnicodeAttribute(null=True)
    stats = StatsMapAttribute(null=True)
    exp_reward = NumberAttribute(null=True)
    money_reward = NumberAttribute(null=True)
    drop = DropItemAttribute(null=True)
    battle_tip = UnicodeAttribute(null=True)

class EnemyResistanceModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    data_type = UnicodeAttribute()
    resistance_type = UnicodeAttribute(null=True)
    resistance_value = NumberAttribute(null=True)

class EnemyAbilityModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    data_type = UnicodeAttribute()
    ability_target = UnicodeAttribute(null=True)
    ability_aoe = UnicodeAttribute(null=True)
    ability_effect = UnicodeAttribute(null=True)

class EnemyByAreaModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    area = UnicodeAttribute(null=False)
