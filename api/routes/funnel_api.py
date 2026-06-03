from fastapi import APIRouter

from analytics.funnel import (
    get_funnel_metrics
)

router = APIRouter()


@router.get("/funnel")
def funnel():

    return get_funnel_metrics(
        "data/events/events.jsonl",
        "data/pos/transactions.csv"
    )