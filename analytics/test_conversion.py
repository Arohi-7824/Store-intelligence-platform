from conversion import get_conversion_metrics

print(
    get_conversion_metrics(
        "data/events/events.jsonl",
        "data/pos/transactions.csv"
    )
)
