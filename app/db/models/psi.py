from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.attributes import MapAttribute, ListAttribute

from app.db.models.base import BaseModel
from app.db.models.common import UsedByMapAttribute

PSI_TYPES = [
    'offense',
    'defense',
    'recovery',
    'teleport',
]

PSI_CLASS_TYPE_MAP = {
    'α': 'alpha',
    'β': 'beta',
    'γ': 'gamma',
    'Σ': 'sigma',
    'Ω': 'omega',
}

class PointsRange(MapAttribute):
    """Represents a range of damage points with start and end values."""
    start = NumberAttribute(null=True)
    end = NumberAttribute(null=True)

class PsiModel(BaseModel):
    """
    Model representing PSI abilities with various attributes.
    """
    class Meta(BaseModel.Meta):
        pass

    psi_type = UnicodeAttribute(null=True)
    psi_class = UnicodeAttribute(null=True)
    used_by = ListAttribute(of=UsedByMapAttribute, null=True)
    target = UnicodeAttribute(null=True)
    pp_cost = NumberAttribute(null=True)
    aoe = UnicodeAttribute(null=True)
    points = PointsRange(null=True)
    effects = UnicodeAttribute(null=True)
