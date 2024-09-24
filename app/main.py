import os
from fastapi import FastAPI

from app.api.character import router as characters_router
from app.api.item import router as items_router
from app.api.enemy import router as enemies_router
from app.api.psi import router as psi_router
from app.api.shop import router as shop_router
from app.api.area import router as area_router

app = FastAPI(
    title="EBapi",
    description="EarthBound (Mother 2) data",
    version="0.1.0",
    swagger_ui_parameters={
        "defaultModelRendering": "model",
    }
)

app.include_router(characters_router)
app.include_router(items_router)
app.include_router(enemies_router)
app.include_router(psi_router)
app.include_router(shop_router)
app.include_router(area_router)

if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    from mangum import Mangum
    app.openapi_url = "/openapi.json"
    lambda_handler = Mangum(app, lifespan="off")
