# Page Title: Antibiotic Effectiveness
import streamlit as st
import pandas as pd
from antibiotic_utils import load_burtin_data, get_antibiotics, show_sidebar_footer
import altair as alt

st.set_page_config(page_title="03. Antibiotic Effectiveness", layout="wide")
st.title("03. Antibiotic Effectiveness")

# Load data
@st.cache_data
def get_data():
    return load_burtin_data()

df = get_data()

# Sidebar: select antibiotics to compare
antibiotics = get_antibiotics()
selected_antibiotics = st.sidebar.multiselect(
    "Select Antibiotics to Compare", antibiotics, default=antibiotics
)

# Melt data for Altair
melted = df.melt(
    id_vars=["Bacteria", "Gram_Staining"],
    value_vars=selected_antibiotics,
    var_name="Antibiotic",
    value_name="MIC"
)

# Bar chart: lower MIC = more effective
st.markdown("### Antibiotic Effectiveness Across Bacteria")
st.write("This bar chart compares the effectiveness (MIC values) of the selected antibiotics for each bacterial species. Lower MIC values indicate higher effectiveness.")
chart = (
    alt.Chart(melted)
    .mark_bar()
    .encode(
        x=alt.X("Bacteria:N", sort="-y", title="Bacterial Species"),
        y=alt.Y("MIC:Q", title="MIC (lower = more effective)"),
        color=alt.Color("Antibiotic:N", legend=alt.Legend(title="Antibiotic")),
        tooltip=["Bacteria", "Antibiotic", "MIC", "Gram_Staining"]
    )
    .properties(width=800, height=400)
    .interactive()
)
st.altair_chart(chart, use_container_width=True)

# Heatmap: MIC values for all bacteria/antibiotic pairs
st.markdown("### MIC Heatmap for All Bacteria and Antibiotics")
st.write("This heatmap provides a quick overview of MIC values for all bacteria/antibiotic pairs. Darker green means more effective (lower MIC), while red means less effective.")
heatmap = (
    alt.Chart(melted)
    .mark_rect()
    .encode(
        x=alt.X("Antibiotic:N", title="Antibiotic"),
        y=alt.Y("Bacteria:N", sort="-x", title="Bacterial Species"),
        color=alt.Color("MIC:Q", scale=alt.Scale(scheme="redyellowgreen", reverse=True), legend=alt.Legend(title="MIC (lower = better)")),
        tooltip=["Bacteria", "Antibiotic", "MIC"]
    )
    .properties(width=400, height=400, title="MIC Heatmap (Lower = More Effective)")
)
st.altair_chart(heatmap, use_container_width=False)

st.markdown("""
- **Tip:** Select one or more antibiotics in the sidebar to compare their effectiveness across all bacteria. Lower MIC values indicate higher effectiveness.
""") 
show_sidebar_footer()