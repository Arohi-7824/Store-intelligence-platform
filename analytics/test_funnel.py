from funnel import get_funnel_metrics

print(
    get_funnel_metrics(
        "data/events/events.jsonl",
        "data/pos/transactions.csv"
    )
)