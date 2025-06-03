import streamlit as st
import pandas as pd
import altair as alt
import os
import json

# --- DATA LOADING ---
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "Airbnb Listings.csv")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    # Clean price column: remove $ and , then convert to float
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )
    # Basic cleaning: remove extreme outliers for price
    df = df[df["price"].between(10, 1000)]
    return df


df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Listings")

neighbourhoods = ["All"] + sorted(df["neighbourhood"].dropna().unique())
room_types = ["All"] + sorted(df["room_type"].dropna().unique())

selected_neighbourhood = st.sidebar.selectbox("Neighbourhood", neighbourhoods)
selected_room_type = st.sidebar.selectbox("Room Type", room_types)
price_min, price_max = int(df["price"].min()), int(df["price"].max())
selected_price = st.sidebar.slider(
    "Price Range", price_min, price_max, (price_min, price_max)
)

# --- FILTER DATA ---
filtered = df.copy()
if selected_neighbourhood != "All":
    filtered = filtered[filtered["neighbourhood"] == selected_neighbourhood]
if selected_room_type != "All":
    filtered = filtered[filtered["room_type"] == selected_room_type]
filtered = filtered[filtered["price"].between(*selected_price)]

# --- MAIN DASHBOARD ---
st.title("San Francisco Airbnb Listings Dashboard")
st.markdown("""
Explore Airbnb listings in San Francisco. Use the filters to interactively explore the data. Charts are coordinated for deeper insights.
""")

# --- 1. MAP OF LISTINGS ---
import json
import os

# Load the GeoJSON file for San Francisco neighborhoods
sf_geojson_path = os.path.join(os.path.dirname(__file__), "data", "sanfrancisco.geo.json")
with open(sf_geojson_path, 'r') as f:
    sf_geojson = json.load(f)

sf_chart = (
    alt.Chart(alt.Data(values=sf_geojson["features"]))
    .mark_geoshape(fillOpacity=0.08, fill="lightgray", stroke="black")
    .encode(tooltip=["properties.name:N"])
    .properties(width=800, height=350)
    .project("mercator")
)

map_chart = (
    sf_chart
    + alt.Chart(filtered)
    .mark_circle(size=50)
    .encode(
        longitude="longitude:Q",
        latitude="latitude:Q",
        color=alt.Color(
            "price:Q",
            scale=alt.Scale(scheme="redyellowgreen"),
            legend=alt.Legend(title="Price ($)"),
        ),
        tooltip=["name:N", "neighbourhood:N", "room_type:N", "price:Q"],
    )
    .interactive()
)

st.markdown("### Listing Locations by Price")
st.altair_chart(map_chart, use_container_width=True)

st.markdown("---")  # Horizontal divider

# --- 2. PRICE DISTRIBUTION & 3. REVIEWS VS. PRICE ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### Price Distribution")
    price_hist = (
        alt.Chart(filtered)
        .mark_bar()
        .encode(
            alt.X("price:Q", bin=alt.Bin(maxbins=40), title="Price ($)"),
            y=alt.Y("count()", title="Count of Records"),
            color=alt.Color("room_type:N", legend=alt.Legend(title="Room Type")),
            tooltip=["count()"],
        )
        .properties(width=350, height=250)
    )
    st.altair_chart(price_hist, use_container_width=True)

with col2:
    st.markdown("### Reviews vs. Price")
    scatter = (
        alt.Chart(filtered)
        .mark_circle(size=60, opacity=0.6)
        .encode(
            x=alt.X("price:Q", title="Price ($)"),
            y=alt.Y("number_of_reviews:Q", title="Number of Reviews"),
            color=alt.Color("room_type:N", legend=alt.Legend(title="Room Type")),
            tooltip=["name:N", "price:Q", "number_of_reviews:Q", "room_type:N"],
        )
        .properties(width=350, height=250)
        .interactive()
    )
    st.altair_chart(scatter, use_container_width=True)

# --- DISCUSSION PROMPTS ---
st.header("Discussion")
with st.expander(
    "Interaction: What interactive components did you include in your dashboard, and how do these features facilitate data exploration?"
):
    st.markdown("""
- **Filters**: Sidebar dropdowns and sliders allow users to focus on specific neighbourhoods, room types, and price ranges.
- **Coordinated Charts**: All visualizations update together, helping users see how filters affect spatial, price, and review patterns.
- **Tooltips & Zoom**: Hovering reveals details; map and scatterplot are zoomable for deeper exploration.
""")

with st.expander(
    "Design Decisions: What were the main design decisions behind your dashboard layout and interactivity?"
):
    st.markdown("""
- **Simplicity**: Clean sidebar for filters, main area for charts.
- **Coordination**: Filters apply to all charts for consistent exploration.
- **Color**: Price and room type are color-encoded for quick visual cues.
- **Responsiveness**: Layout adapts to screen size.
""")

with st.expander(
    "Challenges & Solutions: What challenges did you encounter during the dashboard creation process, and how did you overcome them?"
):
    st.markdown("""
- **Data Quality**: Outliers and missing values required cleaning for meaningful visuals.
- **Performance**: Used Streamlit caching to speed up data loading.
- **Coordination**: Ensured all charts respond to filter changes for a seamless experience.
""")
