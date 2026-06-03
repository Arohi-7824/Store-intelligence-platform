from fastapi import FastAPI

from api.routes.metrics_api import router as metrics_router
from api.routes.conversion_api import router as conversion_router
from api.routes.brands_api import router as brands_router
from api.routes.funnel_api import router as funnel_router

app = FastAPI(
    title="Store Intelligence API"
)

app.include_router(metrics_router)
app.include_router(conversion_router)
app.include_router(brands_router)
app.include_router(funnel_router)


@app.get("/")
def root():
    return {
        "message": "Store Intelligence API Running"
    }