from fastapi import APIRouter

from analytics.metrics import get_metrics

router = APIRouter()


@router.get("/metrics")
def metrics():

    return get_metrics(
        "data/events/events.jsonl"
    )