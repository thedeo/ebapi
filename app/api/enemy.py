from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException

from app.db.models.enemy import EnemyAbilityModel, EnemyResistanceModel
from app.db.models.response import DynamicResponse
from app.db.models.enemy import EnemyModel, EnemyByAreaModel
from app.common import extract_attributes, normalize_name

router = APIRouter(
    tags=["enemy"]
)

async def fetch_enemies(
    by_attribute: str = None,
    detail: Optional[bool] = Query(False, alias="detail")
) -> List[DynamicResponse]:
    """
    Fetch enemies based on the given attribute

    :param str by_attribute: The attribute to filter by
    :param bool detail: Whether to include detailed information
    """
    query_results = None
    if by_attribute == 'profile':
        query_results = EnemyModel.by_data_type_index.query(by_attribute)
    elif by_attribute.startswith('is_boss'):
        query_results = EnemyModel.by_is_boss_index.query(by_attribute.split('#')[1].upper())
    elif by_attribute.startswith('enemy_type'):
        query_results = EnemyModel.by_enemy_type_index.query(by_attribute.split('#')[1].lower())
    
    result = []
    for enemy in query_results:
        enemy_id = enemy.sk.split('#')[0]
        enemy_response = DynamicResponse(id=enemy_id, name=enemy.name)
        if detail:
            enemy_response.__dict__.update(extract_attributes(enemy))

        result.append(enemy_response)
    return result


@router.get("/enemy/list/all", response_model=List[DynamicResponse])
async def list_all_enemies(detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_enemies(by_attribute='profile', detail=detail,)


@router.get("/enemy/list/plain", response_model=List[DynamicResponse])
async def list_all_plain_enemies(detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_enemies(by_attribute='is_boss#false', detail=detail)


@router.get("/enemy/list/bosses", response_model=List[DynamicResponse])
async def list_all_boss_enemies(detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_enemies(by_attribute='is_boss#true', detail=detail)


@router.get("/enemy/list/types", response_model=List[str])
async def list_enemy_types():
    return list(EnemyModel.ENEMY_TYPES)


@router.get("/enemy/list/by_type/{enemy_type}", response_model=List[DynamicResponse])
async def list_enemies_by_type(enemy_type: str, detail: Optional[bool] = Query(False, alias="detail")):
    return await fetch_enemies(by_attribute=f'enemy_type#{enemy_type}', detail=detail)


@router.get("/enemy/list/by_area/{area}", response_model=List[DynamicResponse])
async def list_enemies_by_area(area: str):
    """
    List all enemies in a given area
    
    :param str area: The area to search for enemies in
    """
    query_results = EnemyByAreaModel.query('enemy', EnemyByAreaModel.sk.startswith(f"area#{normalize_name(area)}#"))
    result = []
    for enemy in query_results:
        enemy_id = enemy.sk.split('#')[2]
        enemy_response = DynamicResponse(id=enemy_id, name=enemy.name)
        result.append(enemy_response)
    return result


@router.get("/enemy/{name}")
async def get_enemy_info(name: str):
    """
    Get detailed information about an enemy

    :param str name: The name of the enemy to get information about
    """
    try:
        name = normalize_name(name).lower()
        enemy_detail = EnemyModel.get('enemy', f'{name}#detail')

        enemy_dict = {'profile': extract_attributes(enemy_detail)}
        enemy_dict['profile']['id'] = enemy_detail.sk.split('#')[0]
        enemy_abilities = EnemyAbilityModel.query(
            'enemy',
            EnemyAbilityModel.sk.startswith(f"{name}#ability#")
        )
        enemy_resistances = EnemyResistanceModel.query(
            'enemy',
            EnemyResistanceModel.sk.startswith(f"{name}#resistance#")
        )
        enemy_dict['abilities'] = [extract_attributes(item) for item in enemy_abilities]
        enemy_dict['resistances'] = [extract_attributes(item) for item in enemy_resistances]

        return enemy_dict
    except EnemyModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Enemy not found")
