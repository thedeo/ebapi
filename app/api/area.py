from typing import List
from fastapi import APIRouter

from app.db.models.area import AreaModel

router = APIRouter(
    tags=["area"]
)


@router.get("/area/list/all", response_model=List[dict], description="Get a list of all areas")
def list_all_areas():
    """
    Get a list of all areas
    """
    areas = []
    query_results = AreaModel.query('area')
    for area in query_results:
        area_id = area.sk.split('#')[0]
        areas.append({ 'id': area_id, 'name': area.name, 'primary_area': area.primary_area })
    return areas
