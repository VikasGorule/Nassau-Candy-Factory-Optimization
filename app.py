
import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(
    page_title="Nassau Candy Optimization",
    page_icon="🍫",
    layout="wide"
)

st.title("Nassau Candy Distributor")
st.header("Factory Reallocation & Shipping Optimization")

st.warning(
    "Recorded shipping dates produce lead times of approximately "
    "904–1,642 days. Distance is a geographic proxy, not actual "
    "shipping time or cost. Validate the source data before "
    "making operational decisions."
)

@st.cache_data
def load_data():
    data = pd.read_csv("Nassau Candy Distributor.csv")
    data["Order Date"] = pd.to_datetime(
        data["Order Date"], format="%d-%m-%Y", errors="coerce"
    )
    data["Ship Date"] = pd.to_datetime(
        data["Ship Date"], format="%d-%m-%Y", errors="coerce"
    )
    data["Lead Time Days"] = (
        data["Ship Date"] - data["Order Date"]
    ).dt.days
    data["Product Name"] = data["Product Name"].replace({
        "Wonka Bar -Scrumdiddlyumptious":
            "Wonka Bar - Scrumdiddlyumptious",
        "SweeTARTS": "Sweet TARTS"
    })
    return data

df = load_data()

# Product-to-factory mapping from the project instructions
product_factory = pd.DataFrame([
    ["Chocolate", "Wonka Bar - Nutty Crunch Surprise", "Lot's O' Nuts"],
    ["Chocolate", "Wonka Bar - Fudge Mallows", "Lot's O' Nuts"],
    ["Chocolate", "Wonka Bar - Scrumdiddlyumptious", "Lot's O' Nuts"],
    ["Chocolate", "Wonka Bar - Milk Chocolate", "Wicked Choccy's"],
    ["Chocolate", "Wonka Bar - Triple Dazzle Caramel", "Wicked Choccy's"],
    ["Sugar", "Laffy Taffy", "Sugar Shock"],
    ["Sugar", "Sweet TARTS", "Sugar Shock"],
    ["Sugar", "Nerds", "Sugar Shock"],
    ["Sugar", "Runts", "Sugar Shock"],
    ["Other", "Fizzy Lifting Drinks", "Sugar Shock"],
    ["Sugar", "Everlasting Gobstopper", "Secret Factory"],
    ["Sugar", "Hot Toffee", "The Other Factory"],
    ["Other", "Lickable Wallpaper", "Secret Factory"],
    ["Other", "Wonka Gum", "Secret Factory"],
    ["Other", "Kazookles", "The Other Factory"]
], columns=["Division", "Product Name", "Factory"])

factory_coordinates = pd.DataFrame([
    ["Lot's O' Nuts", 32.881893, -111.768036],
    ["Wicked Choccy's", 32.076176, -81.088371],
    ["Sugar Shock", 48.11914, -96.18115],
    ["Secret Factory", 41.446333, -90.565487],
    ["The Other Factory", 35.1175, -89.971107]
], columns=["Factory", "Latitude", "Longitude"])

df_factory = df.merge(
    product_factory[["Product Name", "Factory"]],
    on="Product Name",
    how="left"
)

mapped_df = df_factory.dropna(subset=["Factory"]).copy()

# Sidebar filters
st.sidebar.header("Dashboard Controls")

division_options = ["All"] + sorted(df["Division"].dropna().unique())
selected_division = st.sidebar.selectbox(
    "Product division", division_options
)

priority = st.sidebar.selectbox(
    "Optimization priority", ["Speed", "Profit"]
)

filtered_df = df.copy()
if selected_division != "All":
    filtered_df = filtered_df[
        filtered_df["Division"] == selected_division
    ]

# Overview
c1, c2, c3 = st.columns(3)
c1.metric("Total Records", f"{len(filtered_df):,}")
c2.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
c3.metric("Gross Profit", f"${filtered_df['Gross Profit'].sum():,.2f}")

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Factory Performance",
    "Factory Optimization",
    "Data Quality"
])

with tab1:
    st.subheader("Sales and Gross Profit by Division")
    division_summary = filtered_df.groupby("Division")[
        ["Sales", "Gross Profit"]
    ].sum()
    st.bar_chart(division_summary)

    st.subheader("Orders by Shipping Mode")
    st.bar_chart(filtered_df["Ship Mode"].value_counts())

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head(100), width="stretch")

with tab2:
    st.subheader("Current Factory Performance")

    factory_summary = mapped_df.groupby("Factory").agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum"),
        Unique_Products=("Product Name", "nunique")
    )

    factory_summary["Profit_Margin_Pct"] = (
        factory_summary["Total_Gross_Profit"]
        / factory_summary["Total_Sales"] * 100
    )

    st.dataframe(
        factory_summary.sort_values(
            "Total_Gross_Profit", ascending=False
        ).round(2),
        width="stretch"
    )
    st.bar_chart(factory_summary[["Total_Gross_Profit"]])

def distance_km(lat1, lon1, lat2, lon2):
    radius = 6371
    lat1, lon1, lat2, lon2 = map(
        radians, [lat1, lon1, lat2, lon2]
    )
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )
    return 2 * radius * atan2(sqrt(a), sqrt(1 - a))

with tab3:
    st.subheader("Factory Optimization Simulator")

    product_list = product_factory["Product Name"].tolist()
    selected_product = st.selectbox(
        "Select product", product_list
    )

    current_factory = product_factory.loc[
        product_factory["Product Name"] == selected_product,
        "Factory"
    ].iloc[0]

    st.write("**Current factory:**", current_factory)

    current_location = factory_coordinates[
        factory_coordinates["Factory"] == current_factory
    ].iloc[0]

    options = factory_coordinates[
        factory_coordinates["Factory"] != current_factory
    ].copy()

    options["Distance_km"] = options.apply(
        lambda row: distance_km(
            current_location["Latitude"],
            current_location["Longitude"],
            row["Latitude"],
            row["Longitude"]
        ),
        axis=1
    )

    # Historical product performance, not a prediction of future profit
    product_history = df[df["Product Name"] == selected_product]

    historical_sales = product_history["Sales"].sum()
    historical_profit = product_history["Gross Profit"].sum()
    historical_units = product_history["Units"].sum()

    st.write("**Historical product performance**")
    m1, m2, m3 = st.columns(3)
    m1.metric("Sales", f"${historical_sales:,.2f}")
    m2.metric("Gross Profit", f"${historical_profit:,.2f}")
    m3.metric("Units", f"{historical_units:,.0f}")

    if priority == "Speed":
        options = options.sort_values("Distance_km")
        st.caption(
            "Speed priority ranks alternatives by straight-line "
            "distance from the current factory."
        )
    else:
        current_factory_profit = mapped_df.groupby("Factory")[
            "Gross Profit"
        ].sum()

        options["Current Factory Gross Profit"] = (
            options["Factory"].map(current_factory_profit)
        )
        options = options.sort_values(
            "Current Factory Gross Profit", ascending=False
        )
        st.caption(
            "Profit priority displays historical factory gross profit. "
            "It does not estimate profit after reassignment."
        )

    options["Recommendation Rank"] = range(1, len(options) + 1)

    st.subheader("Ranked Alternative Factories")
    st.dataframe(
        options[
            ["Recommendation Rank", "Factory", "Distance_km"]
        ].round(2),
        width="stretch"
    )

    recommended_factory = st.selectbox(
        "Choose an alternative for what-if comparison",
        options["Factory"].tolist()
    )

    recommended_distance = options.loc[
        options["Factory"] == recommended_factory,
        "Distance_km"
    ].iloc[0]

    current_alternatives = options.copy()
    st.subheader("What-If Scenario")

    st.write("Current assignment:", current_factory)
    st.write("Alternative assignment:", recommended_factory)
    st.metric(
        "Straight-line distance between factories",
        f"{recommended_distance:,.1f} km"
    )

    st.warning(
        "This is a geographic comparison only. Customer-level "
        "coordinates, factory capacity, production costs, and "
        "shipping rates are unavailable. Actual lead-time savings "
        "and profit impact cannot be calculated from these data."
    )

    st.subheader("Risk & Impact")
    st.error(
        "High validation risk: do not execute a reassignment based "
        "on distance or historical factory profit alone."
    )

    st.download_button(
        "Download ranked alternatives",
        options.to_csv(index=False).encode("utf-8"),
        file_name="ranked_factory_recommendations.csv",
        mime="text/csv"
    )

with tab4:
    st.subheader("Data Quality Checks")

    st.write("Missing values by column")
    st.dataframe(df.isnull().sum().rename("Missing Values"))

    st.metric(
        "Unmapped records",
        int(df_factory["Factory"].isna().sum())
    )

    st.write("Recorded shipping lead-time statistics")
    st.dataframe(df["Lead Time Days"].describe())

    st.warning(
        "The recorded lead times are unusually long. Their validity "
        "as actual shipping durations has not been established."
    )
