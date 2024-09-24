from typing import List, Dict, Optional, Union
from fastapi import APIRouter, Query, HTTPException

from pynamodb.attributes import Attribute
from app.db.models.response import DynamicResponse
from app.db.models.item import WeaponModel, ArmorModel, EdibleModel, BattleItemModel, KeyItemModel
from app.common import normalize_name, extract_attributes

router = APIRouter(
    tags=["item"]
)

# Define constants for item types and their respective models
ITEM_TYPES = {
    'weapon': WeaponModel,
    'armor': ArmorModel,
    'edible': EdibleModel,
    'battle_item': BattleItemModel,
    'key_item': KeyItemModel,
}

async def fetch_items(
    query_type: str,
    item_type: Optional[str] = None,
    detail: Optional[bool] = Query(False, alias="detail")
) -> Union[List[DynamicResponse], Dict[str, List[DynamicResponse]]]:
    """
    Fetch items based on the given query type

    :param str query_type: The type of query to perform
    :param str item_type: The item type to filter by
    :param bool detail: Whether to include detailed information
    """
    if query_type == 'all':
        all_results = []
        for item_type_key, item_model in ITEM_TYPES.items():
            results = item_model.by_item_type_index.query(item_type_key)
            all_results.extend(results)
    elif query_type == 'type':
        item_model = ITEM_TYPES[item_type]
        all_results = item_model.by_item_type_index.query(item_type)
    
    # Extract the attributes of each item
    result = {}
    for item in all_results:
        item_response = DynamicResponse(id=item.sk, name=item.name)
        if detail:
            item_response.__dict__.update(extract_attributes(item))
        result.setdefault(item.item_type, []).append(item_response)
    return result

@router.get("/item/list/all", response_model=Dict[str, List[DynamicResponse]])
async def list_all_items(detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_items('all', detail=detail)

@router.get("/item/list/weapon", response_model=Dict[str, List[DynamicResponse]])
async def list_weapon_items(detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_items("type", "weapon", detail)

@router.get("/item/list/armor", response_model=Dict[str, List[DynamicResponse]])
async def list_armor_items(detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_items("type", "armor", detail)

@router.get("/item/list/edible", response_model=Dict[str, List[DynamicResponse]])
async def list_edible_items(detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_items("type", "edible", detail)

@router.get("/item/list/battle", response_model=Dict[str, List[DynamicResponse]])
async def list_battle_items(detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_items("type", "battle_item", detail)

@router.get("/item/list/key", response_model=Dict[str, List[DynamicResponse]])
async def list_key_items(detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_items("type", "key_item", detail)


@router.get("/item/get/{item_type}/{name}")
def get_item_info(item_type: str, name: str):
    """
    Get detailed information about an item

    :param str name: The name of the item
    """
    try:
        model = ITEM_TYPES.get(item_type)
        if model is None:
            raise KeyError("Item type not found")

        item = model.get("item", normalize_name(name))
        
        item_dict = extract_attributes(item)
        for field in dir(item):
            if not field.startswith('_') and field not in item_dict:
                attr = getattr(item, field)
                if isinstance(attr, Attribute):
                    item_dict[field] = getattr(item, f"_{field}")
        return item_dict
    except KeyError:
        raise HTTPException(status_code=404, detail="Item type not found")
    except model.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")
