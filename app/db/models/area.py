from pynamodb.attributes import UnicodeAttribute
from app.db.models.base import BaseModel

class AreaModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    primary_area = UnicodeAttribute(null=True)
