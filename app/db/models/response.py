from pydantic import BaseModel

class DynamicResponse(BaseModel):
    """
    Flexible response model with additional allowed fields.
    
    Attributes:
        id (str): used to identify the data in the response
        name (str): Friendly name of the data
    """

    id: str
    name: str

    class Config:
        """Allows extra fields in model instances."""
        extra = "allow"
