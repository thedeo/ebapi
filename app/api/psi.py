# logic for the psi api
from typing import List, Optional
from fastapi import APIRouter, HTTPException

from app.db.models.response import DynamicResponse
from app.db.models.psi import PsiModel, PSI_TYPES, PSI_CLASS_TYPE_MAP
from app.common import extract_attributes, replace_greek_letters

router = APIRouter(
    tags=["psi"]
)

async def fetch_psi(
    by_attribute: str = None,
    detail: Optional[bool] = False
) -> List[DynamicResponse]:
    """
    Fetch PSI based on the given attribute
    
    :param str by_attribute: The attribute to filter by
    :param bool detail: Whether to include detailed information
    """
    query_results = None
    if by_attribute == 'all':
        query_results = PsiModel.query('psi')

    result = []
    for psi in query_results:
        psi_response = DynamicResponse(id=psi.sk, name=psi.name)
        if detail:
            psi_response.__dict__.update(extract_attributes(psi))
        result.append(psi_response)
    return result

@router.get("/psi/list/all", response_model=List[DynamicResponse])
async def list_all_psi(detail: Optional[bool] = False):
    return await fetch_psi(by_attribute='all', detail=detail)

@router.get("/psi/list/classes", response_model=List[str])
def list_psi_classes():
    return list(PSI_CLASS_TYPE_MAP.values())

@router.get("/psi/list/by_class/{class_name}", response_model=List[DynamicResponse])
async def list_psi_by_class(class_name: str, detail: Optional[bool] = False):
    """
    List all PSI by class name

    Handles different symbols and spaces in class name
    
    :param str class_name: The class name to filter by
    :param bool detail: Whether to include detailed information
    """
    try:
        class_name = replace_greek_letters(class_name).replace(' ', '_').strip().lower()
        if class_name not in PSI_CLASS_TYPE_MAP.values():
            raise KeyError("Invalid PSI class name")

        psi_by_class = PsiModel.by_psi_class_index.query(class_name)

        result = []
        for psi in psi_by_class:
            psi_response = DynamicResponse(id=psi.sk, name=psi.name)
            if detail:
                psi_response.__dict__.update(extract_attributes(psi))
            result.append(psi_response)
        return result
    except KeyError:
        raise HTTPException(status_code=404, detail='PSI class not found')

@router.get("/psi/list/types", response_model=List[str])
async def list_psi_types():
    return PSI_TYPES

@router.get("/psi/{name}", response_model=DynamicResponse)
async def get_psi(name: str):
    """
    Get details of a PSI
    
    :param str name: The name of the PSI to get details of
    """
    try:
        name = replace_greek_letters(name).replace(' ', '_').strip().lower()
        psi = PsiModel.get('psi', name)
        if not psi:
            raise HTTPException(status_code=404, detail="Psi not found")
        psi_response = DynamicResponse(id=psi.sk, name=psi.name)
        psi_response.__dict__.update(extract_attributes(psi))
        return psi_response
    except PsiModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="PSI not found. Try listing all PSI to find the correct name.")
