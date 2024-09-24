from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

class ByAreaIndex(GlobalSecondaryIndex):
    class Meta():
        index_name = 'by-area'
        projection = AllProjection()

    area = UnicodeAttribute(hash_key=True)

class ByItemTypeIndex(GlobalSecondaryIndex):
    class Meta():
        index_name = 'by-item-type'
        projection = AllProjection()

    item_type = UnicodeAttribute(hash_key=True)

class ByDataTypeIndex(GlobalSecondaryIndex):
    class Meta():
        index_name = 'by-data-type'
        projection = AllProjection()

    data_type = UnicodeAttribute(hash_key=True)

class ByEnemyTypeIndex(GlobalSecondaryIndex):
    class Meta():
        index_name = 'by-enemy-type'
        projection = AllProjection()

    enemy_type = UnicodeAttribute(hash_key=True)

class ByIsBossIndex(GlobalSecondaryIndex):
    class Meta():
        index_name = 'by-is-boss'
        projection = AllProjection()

    is_boss = UnicodeAttribute(hash_key=True)

class ByPsiTypeIndex(GlobalSecondaryIndex):
    class Meta():
        index_name = 'by-psi-type'
        projection = AllProjection()

    psi_type = UnicodeAttribute(hash_key=True)

class ByPsiClassIndex(GlobalSecondaryIndex):
    class Meta():
        index_name = 'by-psi-class'
        projection = AllProjection()

    psi_class = UnicodeAttribute(hash_key=True)
