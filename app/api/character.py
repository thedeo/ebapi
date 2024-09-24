from typing import List, Dict
from fastapi import APIRouter, HTTPException

from app.db.models.character import PCModel, NPCModel
from app.common import extract_attributes, normalize_name

router = APIRouter(
    tags=["character"]
)

# Define constants for item types and their respective models
CHARACTER_TYPES = {
    'pc': PCModel,
    'npc': NPCModel,
}

# Route to get a list of all characters
@router.get("/character/list/all", response_model=List[Dict], description="Get a list of all characters")
def get_all_characters():
    characters = []

    # Query each character type separately
    for character_type, model in CHARACTER_TYPES.items():
        query_results = model.query('character', model.sk.startswith(f"{character_type}#"))
        for character in query_results:
            # Dynamically extract attributes from each character model
            character_data = extract_attributes(character)
            character_data["type"] = character_type  # Include the character type
            characters.append(character_data)

    return characters

# Route to list just pc characters
@router.get("/character/list/pc", response_model=List[Dict], description="Get a list of all player characters")
def list_pc_characters():
    characters = []
    character_type = 'pc'

    # Query each character type separately
    model = CHARACTER_TYPES[character_type]
    query_results = model.query('character', model.sk.startswith(f"{character_type}#"))
    for character in query_results:
        # Dynamically extract attributes from each character model
        character_data = extract_attributes(character)
        character_data["type"] = character_type
        characters.append(character_data)
    
    return characters

# Route to list just npc characters
@router.get("/character/list/npc", response_model=List[Dict], description="Get a list of all non-player characters")
def list_npc_characters():
    characters = []
    character_type = 'npc'

    # Query each character type separately
    model = CHARACTER_TYPES[character_type]
    query_results = model.query('character', model.sk.startswith(f"{character_type}#"))
    for character in query_results:
        # Dynamically extract attributes from each character model
        character_data = extract_attributes(character)
        character_data["type"] = character_type
        characters.append(character_data)
    
    return characters

# Route to list just npc characters
@router.get("/character/list/npc/{area}", response_model=List[Dict], description="Get a list of all non-player characters by area")
def list_npc_characters_by_area(area: str):
    characters = []
    character_type = 'npc'

    # Query each character type separately
    model = CHARACTER_TYPES[character_type]
    query_results = model.query('character', model.sk.startswith(f"{character_type}#"))
    for character in query_results:
        # Dynamically extract attributes from each character model
        character_data = extract_attributes(character)
        character_data["type"] = character_type
        if area.lower() in [area.lower() for area in character_data["areas"]]:
            characters.append(character_data)
    
    return characters

# Route to get detailed information about a player character
@router.get("/character/pc/{name}", description="Get detailed information about a character")
def get_pc_info(name: str):
    try:
        pc = PCModel.get("character", f"pc#{normalize_name(name).lower()}")
        return {
            "name": pc.name,
            "age": pc.age,
            "hometown": pc.hometown,
        }
    except PCModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="PC not found")

# Route to get detailed information about a non-player character
@router.get("/character/npc/{name}", description="Get detailed information about an NPC")
def get_npc_info(name: str):
    try:
        npc = NPCModel.get("character", f"npc#{normalize_name(name).lower()}")
        return {
            "name": npc.name,
            "areas": npc.areas,
            "role": npc.role,
        }
    except NPCModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="NPC not found")
