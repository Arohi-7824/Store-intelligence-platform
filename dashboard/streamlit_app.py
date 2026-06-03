import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Store Intelligence Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ---------------------------
# Header
# ---------------------------

st.title(" Store Intelligence Dashboard")

if st.button("🔄 Refresh Dashboard"):
    st.rerun()

# ---------------------------
# Load Data
# ---------------------------

try:
    metrics = requests.get(
        f"{API_URL}/metrics"
    ).json()

    conversion = requests.get(
        f"{API_URL}/conversion"
    ).json()

    brands = requests.get(
        f"{API_URL}/brands"
    ).json() 

    funnel = requests.get(
        f"{API_URL}/funnel"
    ).json()

except Exception as e:
    st.error(
        f"Could not connect to API: {e}"
    )
    st.stop()

# ---------------------------
# KPI Cards
# ---------------------------

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

# ---------------------------
# Funnel Analytics
# ---------------------------

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

# ---------------------------
# Zone Analytics
# ---------------------------

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
        use_container_width=True
    )

# ---------------------------
# Top Brands
# ---------------------------

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
    use_container_width=True
)

# ---------------------------
# Top Categories
# ---------------------------

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
    use_container_width=True
)

# ---------------------------
# Top Products
# ---------------------------

st.subheader("⭐ Top Products")

product_df = pd.DataFrame(
    list(brands["top_products"].items()),
    columns=["Product", "Revenue"]
)

st.dataframe(
    product_df,
    use_container_width=True,
    hide_index=True
)

# ---------------------------
# Heatmap
# ---------------------------

st.subheader(" Customer Heatmap")

try:
    st.image(
        "heatmap.png",
        width="stretch"
    )
except:
    st.warning(
        "Heatmap image not found. Run heatmap generation first."
    )

# ---------------------------
# Download Metrics
# ---------------------------

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

# ---------------------------
# Footer
# ---------------------------

st.divider()

st.caption(
    "Store Intelligence Platform • YOLOv8 + ByteTrack + FastAPI + Streamlit"
)