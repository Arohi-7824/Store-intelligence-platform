import pandas as pd


def get_brand_metrics(transactions_file):

    df = pd.read_csv(transactions_file)

    revenue_by_brand = (
        df.groupby("brand_name")["total_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    top_brands = revenue_by_brand.head(10)

    top_products = (
    df.groupby("product_name")["total_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    )   

    top_categories = (
    df.groupby("sub_category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    )

    return {
        "top_brands": top_brands.to_dict(),
        "top_products": top_products.to_dict(),
        "top_categories": top_categories.to_dict()
    }