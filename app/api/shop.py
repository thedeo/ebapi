from typing import List
from fastapi import APIRouter, HTTPException

from app.common import extract_attributes, normalize_name
from app.db.models.shop import ShopModel, ShopItemModel

router = APIRouter(
    tags=["shop"]
)


@router.get("/shop/list/all", response_model=List[dict], description="Get a list of all shops")
def list_all_shops():
    """
    List all shops
    """
    shops = []
    query_results = ShopModel.query('shop', ShopModel.sk.startswith('shop#'))
    for shop in query_results:
        shop_id = shop.sk.split('#')[1]
        shops.append({ 'id': shop_id, 'name': shop.name })
    return shops


@router.get("/shop/list/by_area/{area}", response_model=List[dict], description="Get a list of shops by area")
def list_shops_by_area(area: str):
    """
    List all shops in a given area

    :param str area: The area to search for shops in
    """
    shops = []
    area = normalize_name(area).capitalize().strip()
    print(f'Area: {area}')
    query_results = ShopModel.by_area_index.query(area)
    for shop in query_results:
        if shop.sk.startswith('shop#'):
            shop_id = shop.sk.split('#')[1]
            shops.append({ 'id': shop_id, 'name': shop.name })
    return shops


@router.get("/shop/{shop_id}", response_model=List[dict], description="Get details of a shop")
def get_shop(shop_id: str, detail: bool = False):
    """
    Get details of a shop
    
    :param str shop_id: The ID of the shop to get details of
    :param bool detail: Whether to include item details
    """
    try:
        items = []
        shop_id = normalize_name(shop_id).lower().strip()
        shop_items = ShopItemModel.query('shop', ShopModel.sk.startswith(f'{shop_id}#item#'))
        for item in shop_items:
            item_id = item.sk.split('#')[2]
            items.append({ 'id': item_id, 'name': item.name })
            if detail:
                items[-1].update(extract_attributes(item))
        if not items:
            raise HTTPException(status_code=404, detail="Shop not found")
        return items
    except KeyError:
        raise HTTPException(status_code=404, detail="Shop not found")
    except ShopModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Shop not found")
