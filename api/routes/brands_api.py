from fastapi import APIRouter

from analytics.brand_analytics import (
    get_brand_metrics
)

router = APIRouter()


@router.get("/brands")
def brands():

    return get_brand_metrics(
        "data/pos/transactions.csv"
    )