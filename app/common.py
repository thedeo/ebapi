import re

from app.db.models.common import StatsMapAttribute
from app.db.models.common import DropItemAttribute
from app.db.models.common import UsedByMapAttribute
from app.db.models.psi import PointsRange
from app.db.models.psi import PSI_CLASS_TYPE_MAP

def normalize_name(name):
    '''
    Remove special characters and spaces from a name and convert it to lowercase.
    '''
    name = re.sub(r'\s+', ' ', name) # Replace multiple spaces with single space
    return re.sub(r'[^\w\s]', '', name.lower()).replace(' ', '_')

def replace_greek_letters(text):
    '''
    Replace Greek letters with their English equivalents.
    '''
    for char, replacement in PSI_CLASS_TYPE_MAP.items():
        text = text.replace(char, replacement)
    return text

def parse_foe_stats(row):
    '''
    Parse the foe stats from a row in the foe stats CSV file
    '''
    stats = {
        'hp': int(row.get('hp', 0)),
        'pp': int(row.get('pp', 0)),
        'offense': int(row.get('offense', 0)),
        'defense': int(row.get('defense', 0)),
        'speed': int(row.get('spd', 0)),
        'guts': int(row.get('guts', 0))
    }
    areas = row.get('areas', None).split('/') if row.get('areas') else []
    return stats, areas

custom_attribute_types = [StatsMapAttribute, DropItemAttribute, UsedByMapAttribute, PointsRange]
def extract_attributes(item):
    '''
    Extract the attributes of a custom attribute type
    '''
    item_dict = {**item.attribute_values}
    item_dict.pop("pk", None)
    item_dict.pop("sk", None)
    item_dict.pop("data_type", None)

    for key, value in item_dict.items():
        # Check if the value is a custom attribute type
        if isinstance(value, tuple(custom_attribute_types)):
            item_dict[key] = extract_attributes(value)  # Recursively extract attributes
        elif isinstance(value, list) and value \
             and isinstance(value[0], tuple(custom_attribute_types)):
            item_dict[key] = [extract_attributes(v) for v in value]

    return item_dict
