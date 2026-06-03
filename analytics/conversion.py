import pandas as pd
import json


def get_conversion_metrics(
    events_file,
    transactions_file
):

    visitors = set()

    with open(events_file, "r") as f:

        for line in f:

            event = json.loads(line)

            visitors.add(event["visitor_id"])

    total_visitors = len(visitors)

    transactions = pd.read_csv(transactions_file)

    unique_bills = transactions["invoice_number"].nunique()

    # ADD THESE LINES HERE
    total_revenue = transactions["total_amount"].sum()

    avg_bill_value = (
        total_revenue / unique_bills
        if unique_bills
        else 0
    )

    conversion_rate = (
        unique_bills / total_visitors * 100
        if total_visitors > 0
        else 0
    )

    return {
        "total_visitors": total_visitors,
        "total_bills": int(unique_bills),
        "conversion_rate": round(conversion_rate, 2),

        # ADD THESE TO RETURN
        "total_revenue": float(round(total_revenue, 2)),
        "avg_bill_value": float(round(avg_bill_value, 2))
    }