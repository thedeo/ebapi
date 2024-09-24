from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from app.db.models.indexes import ByAreaIndex
from app.db.models.indexes import ByItemTypeIndex
from app.db.models.indexes import ByDataTypeIndex
from app.db.models.indexes import ByEnemyTypeIndex
from app.db.models.indexes import ByIsBossIndex
from app.db.models.indexes import ByPsiTypeIndex
from app.db.models.indexes import ByPsiClassIndex

from app.settings import API_DATA_TABLE, AWS_REGION

class BaseModel(Model):
    class Meta:
        table_name = API_DATA_TABLE
        region = AWS_REGION

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()

    # Indexes
    by_area_index = ByAreaIndex()
    by_item_type_index = ByItemTypeIndex()
    by_data_type_index = ByDataTypeIndex()
    by_enemy_type_index = ByEnemyTypeIndex()
    by_is_boss_index = ByIsBossIndex()
    by_psi_type_index = ByPsiTypeIndex()
    by_psi_class_index = ByPsiClassIndex()
