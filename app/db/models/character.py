from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute
from app.db.models.base import BaseModel

class CharacterModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass


class PCModel(CharacterModel):
    age = NumberAttribute(null=True)
    bio = UnicodeAttribute(null=True)
    hometown = UnicodeAttribute(null=True)


class NPCModel(CharacterModel):
    areas = ListAttribute(null=True)
    role = UnicodeAttribute(null=True)
