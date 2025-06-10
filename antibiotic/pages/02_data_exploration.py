# Page Title: Data Exploration
import streamlit as st
import pandas as pd
from antibiotic_utils import (
    load_burtin_data,
    get_antibiotics,
    get_gram_types,
    show_sidebar_footer,
)
import altair as alt

st.set_page_config(
    page_title="Data Exploration - Burtin Antibiotic Dataset", layout="wide"
)
st.title("02. Data Exploration")


# Load data
@st.cache_data
def get_data():
    return load_burtin_data()


df = get_data()

# Sidebar filters
st.sidebar.header("Filter Data")
gram_types = get_gram_types()
selected_gram = st.sidebar.multiselect(
    "Gram Staining Type", options=gram_types, default=gram_types
)

antibiotics = get_antibiotics()
selected_antibiotic = st.sidebar.selectbox("Antibiotic (for MIC filter)", antibiotics)

mic_min = int(df[selected_antibiotic].min())
mic_max = int(df[selected_antibiotic].max())
selected_mic = st.sidebar.slider(
    f"MIC Range for {selected_antibiotic}", mic_min, mic_max, (mic_min, mic_max)
)

# Filter data
filtered_df = df[
    df["Gram_Staining"].isin(selected_gram)
    & df[selected_antibiotic].between(*selected_mic)
]

st.markdown(f"### Filtered Data Table ({len(filtered_df)} of {len(df)} rows)")
st.dataframe(filtered_df, use_container_width=True)

st.markdown("""
- **Tip:** Use the sidebar to filter by Gram type and MIC range for the selected antibiotic.
- **Explore:** Click column headers to sort, and use the table search to find specific bacteria.
""")

show_sidebar_footer() 