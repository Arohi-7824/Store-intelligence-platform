import json
import pandas as pd

BILLING_ZONE = "BILLING_ZONE"  # Later change to CASH_COUNTER


def get_funnel_metrics(
    events_file,
    transactions_file
):
    visitors = set()
    engaged_visitors = set()
    billing_visitors = set()

    with open(events_file, "r") as f:

        for line in f:

            event = json.loads(line)

            visitor_id = event["visitor_id"]

            visitors.add(visitor_id)

            # Engaged visitor = stayed in a zone for >= 5 seconds
            if (
                event["event_type"] == "ZONE_DWELL"
                and event["dwell_ms"] >= 5000
            ):
                engaged_visitors.add(visitor_id)

            # Billing area visit
            if (
                event["event_type"] == "ZONE_ENTER"
                and event["zone_id"] == BILLING_ZONE
            ):
                billing_visitors.add(visitor_id)

    transactions = pd.read_csv(transactions_file)

    purchasers = transactions["invoice_number"].nunique()

    total_visitors = len(visitors)

    engagement_rate = (
        len(engaged_visitors) / total_visitors * 100
        if total_visitors else 0
    )

    billing_rate = (
        len(billing_visitors) / total_visitors * 100
        if total_visitors else 0
    )

    conversion_rate = (
        purchasers / total_visitors * 100
        if total_visitors else 0
    )

    return {
        "total_visitors": total_visitors,
        "engaged_visitors": len(engaged_visitors),
        "engagement_rate": round(engagement_rate, 2),

        "billing_zone_visitors": len(billing_visitors),
        "billing_zone_rate": round(billing_rate, 2),

        "purchasers": int(purchasers),
        "conversion_rate": round(conversion_rate, 2)
    }