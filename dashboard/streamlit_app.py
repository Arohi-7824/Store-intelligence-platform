import streamlit as st
import pandas as pd
import plotly.express as px
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from analytics.metrics import get_metrics as get_store_metrics
from analytics.conversion import get_conversion_metrics
from analytics.brand_analytics import get_brand_metrics as get_brand_analytics
from analytics.funnel import get_funnel_metrics

st.set_page_config(
    page_title="Store Intelligence Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# --------------------------------
# Header
# --------------------------------

st.title("🛍️ Store Intelligence Dashboard")

if st.button("🔄 Refresh Dashboard"):
    st.rerun()

# --------------------------------
# Load Analytics Directly
# --------------------------------

try:

    metrics = get_store_metrics(
        "data/events/events.jsonl"
    )

    conversion = get_conversion_metrics(
        "data/events/events.jsonl",
        "data/transactions/transactions.csv"
    )

    brands = get_brand_analytics(
        "data/transactions/transactions.csv"
    )

    funnel = get_funnel_metrics(
        "data/events/events.jsonl",
        "data/transactions/transactions.csv"
    )

except Exception as e:

    st.error(
        f"Error loading analytics: {e}"
    )

    st.stop()

# --------------------------------
# KPI Cards
# --------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Visitors",
        metrics["unique_visitors"]
    )

with col2:
    st.metric(
        "Revenue",
        f"₹{conversion['total_revenue']:,.2f}"
    )

with col3:
    st.metric(
        "Conversion Rate",
        f"{conversion['conversion_rate']}%"
    )

with col4:
    st.metric(
        "Avg Bill Value",
        f"₹{conversion['avg_bill_value']:,.2f}"
    )

st.divider()

# --------------------------------
# Funnel Analytics
# --------------------------------

st.subheader("📊 Customer Funnel")

funnel_df = pd.DataFrame({
    "Stage": [
        "Visitors",
        "Engaged",
        "Billing Area",
        "Purchasers"
    ],
    "Count": [
        funnel["total_visitors"],
        funnel["engaged_visitors"],
        funnel["billing_zone_visitors"],
        funnel["purchasers"]
    ]
})

fig_funnel = px.funnel(
    funnel_df,
    x="Count",
    y="Stage",
    title="Customer Conversion Funnel"
)

st.plotly_chart(
    fig_funnel,
    width="stretch"
)

# --------------------------------
# Zone Analytics
# --------------------------------

st.subheader("🏬 Zone Analytics")

col1, col2 = st.columns([1, 2])

with col1:

    st.metric(
        "Most Visited Zone",
        metrics["most_visited_zone"]
    )

with col2:

    zone_df = pd.DataFrame(
        list(metrics["zone_counts"].items()),
        columns=["Zone", "Visits"]
    )

    fig_zone = px.bar(
        zone_df,
        x="Zone",
        y="Visits",
        title="Zone Traffic"
    )

    st.plotly_chart(
        fig_zone,
        width="stretch"
    )

# --------------------------------
# Top Brands
# --------------------------------

st.subheader("🏷️ Top Brands")

brand_df = pd.DataFrame(
    list(brands["top_brands"].items()),
    columns=["Brand", "Revenue"]
)

fig_brand = px.bar(
    brand_df,
    x="Brand",
    y="Revenue",
    title="Revenue by Brand"
)

st.plotly_chart(
    fig_brand,
    width="stretch"
)

# --------------------------------
# Top Categories
# --------------------------------

st.subheader("📦 Top Categories")

cat_df = pd.DataFrame(
    list(brands["top_categories"].items()),
    columns=["Category", "Revenue"]
)

fig_cat = px.pie(
    cat_df,
    names="Category",
    values="Revenue",
    title="Category Contribution"
)

st.plotly_chart(
    fig_cat,
    width="stretch"
)

# --------------------------------
# Top Products
# --------------------------------

st.subheader("⭐ Top Products")

product_df = pd.DataFrame(
    list(brands["top_products"].items()),
    columns=["Product", "Revenue"]
)

st.dataframe(
    product_df,
    width="stretch",
    hide_index=True
)

# --------------------------------
# Heatmap
# --------------------------------

st.subheader("🔥 Customer Heatmap")

try:

    st.image(
        "heatmap.png",
        width="stretch"
    )

except Exception:

    st.warning(
        "Heatmap image not found."
    )

# --------------------------------
# Export Report
# --------------------------------

st.subheader("📥 Export")

report = {
    "metrics": metrics,
    "conversion": conversion,
    "funnel": funnel,
    "brands": brands
}

st.download_button(
    label="Download Analytics Report",
    data=json.dumps(report, indent=4),
    file_name="store_analytics_report.json",
    mime="application/json"
)

# --------------------------------
# Footer
# --------------------------------

st.divider()

st.caption(
    "Store Intelligence Platform • YOLOv8 • ByteTrack • Streamlit"
)