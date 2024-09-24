from pynamodb.attributes import MapAttribute, NumberAttribute, UnicodeAttribute

class StatsMapAttribute(MapAttribute):
    """
    Map attribute for enemy stats.
    """
    hp = NumberAttribute(null=True)
    pp = NumberAttribute(null=True)
    offense = NumberAttribute(null=True)
    defense = NumberAttribute(null=True)
    speed = NumberAttribute(null=True)
    guts = NumberAttribute(null=True)

class DropItemAttribute(MapAttribute):
    """
    Map attribute for enemy drop items.
    """
    item = UnicodeAttribute(null=True)
    chance = UnicodeAttribute(null=True)

class UsedByMapAttribute(MapAttribute):
    """
    Map attribute for items, enemies, etc. that use a PSI ability.
    """
    name = UnicodeAttribute(null=True)
    level = NumberAttribute(null=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if not isinstance(other, UsedByMapAttribute):
            return NotImplemented
        return self.name == other.name and self.level == other.level

    def __hash__(self):
        return hash((self.name, self.level))
