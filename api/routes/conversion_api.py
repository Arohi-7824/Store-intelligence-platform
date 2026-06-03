from fastapi import APIRouter

from analytics.conversion import (
    get_conversion_metrics
)

router = APIRouter()


@router.get("/conversion")
def conversion():

    return get_conversion_metrics(
        "data/events/events.jsonl",
        "data/pos/transactions.csv"
    )