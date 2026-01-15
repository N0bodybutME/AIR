import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# -------------------------------------------------
def aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 200:
        return "Poor"
    elif aqi <= 300:
        return "Very Poor"
    elif aqi <= 400:
        return "Severe"
    else:
        return "Hazardous"

# -------------------------------------------------
st.title("Air Quality Index (AQI) Analysis App")
st.write("Analyze air pollution data and classify cities based on AQI levels.")
# -------------------------------------------------
df = pd.read_csv("air_quality_latest_by_city.csv")

st.subheader("Dataset Preview")
st.dataframe(df.head())

# -------------------------------------------------
st.sidebar.header("Filters")

# State
state = st.sidebar.selectbox(
    "Select State",
    options=["All"] + sorted(df["state"].dropna().unique().tolist())
)

if state != "All":
    df = df[df["state"] == state]

# City
city = st.sidebar.selectbox(
    "Select City",
    options=["All"] + sorted(df["location"].dropna().unique().tolist())
)

if city != "All":
    df = df[df["location"] == city]

# -------------------------------------------------
st.subheader("AQI Category Distribution")

if df.empty:
    st.warning("No AQI data available for the selected filters.")
else:
    aqi_counts = df["AQI_Range"].value_counts()
    total = aqi_counts.sum()

    aqi_labels = ["Good", "Moderate", "Poor", "Very Poor", "Severe", "Hazardous"]
    aqi_colors = [
        "green",
        "yellow",
        "orange",
        "red",
        (0.722, 0.153, 0.153),  
        "black"
    ]

    present_labels = aqi_counts.index.tolist()
    slice_colors = [
        aqi_colors[aqi_labels.index(label)]
        for label in present_labels
    ]

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.pie(
        aqi_counts.values,
        colors=slice_colors,
        startangle=90,
        wedgeprops={"width": 0.4}
    )

    title_suffix = f" ({city})" if city != "All" else ""
    ax.set_title(f"Distribution of Cities Across AQI Categories{title_suffix}")
    legend_elements = []

    for label in present_labels:
        pct = (aqi_counts[label] / total) * 100
        legend_elements.append(
            Patch(
                facecolor=aqi_colors[aqi_labels.index(label)],
                label=f"{label} ({pct:.1f}%)"
            )
        )

    ax.legend(
        handles=legend_elements,
        title="AQI Categories",
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        frameon=False
    )

    st.pyplot(fig)
# -------------------------------------------------
st.subheader("City-wise AQI Data")
st.dataframe(df[["location", "AQI", "AQI_Range"]].head(20))
# -------------------------------------------------
st.subheader("Check Air Quality by AQI Value")

user_aqi = st.number_input(
    "Enter AQI value",
    min_value=0,
    max_value=600,
    value=150,
    step=1
)

category = aqi_category(user_aqi)

color_map = {
    "Good": "green",
    "Moderate": "yellow",
    "Poor": "orange",
    "Very Poor": "darkred",
    "Severe": "purple",
    "Hazardous": "black"
}

st.markdown(
    f"<h4 style='color:{color_map.get(category, 'black')}'>Air Quality: {category}</h4>",
    unsafe_allow_html=True
)
# -------------------------------------------------
tolerance = 20

nearby_cities = df[
    (df["AQI"] >= user_aqi - tolerance) &
    (df["AQI"] <= user_aqi + tolerance)
][["location", "AQI", "AQI_Range"]]

st.subheader("Cities with Similar AQI Levels")

if nearby_cities.empty:
    st.warning("No cities found with similar AQI values.")
else:
    st.dataframe(nearby_cities.sort_values("AQI"))
# -------------------------------------------------
st.info(
    "AQI classification helps identify cities with unhealthy air quality "
    "and supports sustainable environmental planning."
)
