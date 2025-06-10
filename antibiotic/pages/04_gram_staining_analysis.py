# Page Title: Gram Staining Analysis
import streamlit as st
import pandas as pd
from antibiotic_utils import load_burtin_data, get_antibiotics, show_sidebar_footer
import altair as alt

st.set_page_config(page_title="04. Gram Staining Analysis", layout="wide")
st.title("04. Gram Staining Analysis")

# Load data
@st.cache_data
def get_data():
    return load_burtin_data()

df = get_data()

# Sidebar: select antibiotics
antibiotics = get_antibiotics()
selected_antibiotics = st.sidebar.multiselect(
    "Select Antibiotics", antibiotics, default=antibiotics
)

# Melt data for Altair
melted = df.melt(
    id_vars=["Bacteria", "Gram_Staining"],
    value_vars=selected_antibiotics,
    var_name="Antibiotic",
    value_name="MIC"
)

# Boxplot: MIC by Gram type and antibiotic
st.markdown("### MIC Distribution by Gram Type and Antibiotic")
st.write("This boxplot shows the distribution of MIC values for each antibiotic, separated by Gram-positive and Gram-negative bacteria. Use it to compare how each group responds to different antibiotics.")
chart = (
    alt.Chart(melted)
    .mark_boxplot()
    .encode(
        x=alt.X("Gram_Staining:N", title="Gram Staining Type"),
        y=alt.Y("MIC:Q", title="MIC (lower = more effective)"),
        color=alt.Color("Antibiotic:N", legend=alt.Legend(title="Antibiotic")),
        tooltip=["Antibiotic", "Gram_Staining", "MIC"]
    )
    .properties(width=600, height=400)
)
st.altair_chart(chart, use_container_width=True)

# Grouped bar chart: mean MIC by Gram type and antibiotic
st.markdown("### Mean MIC by Gram Type and Antibiotic")
st.write("This grouped bar chart summarizes the average MIC for each antibiotic, split by Gram-positive and Gram-negative bacteria. Lower bars indicate more effective antibiotics for that group.")
grouped = (
    melted.groupby(["Gram_Staining", "Antibiotic"]).MIC.mean().reset_index()
)
grouped_chart = (
    alt.Chart(grouped)
    .mark_bar()
    .encode(
        x=alt.X("Antibiotic:N", title="Antibiotic"),
        y=alt.Y("MIC:Q", title="Mean MIC (lower = more effective)"),
        color=alt.Color("Gram_Staining:N", legend=alt.Legend(title="Gram Type")),
        column=alt.Column("Gram_Staining:N", title=None),
        tooltip=["Antibiotic", "Gram_Staining", alt.Tooltip("MIC", format=".2f")]
    )
    .properties(width=120, height=300, title="Mean MIC by Gram Type and Antibiotic")
)
st.altair_chart(grouped_chart, use_container_width=True)

st.markdown("""
- **Tip:** Select antibiotics in the sidebar to compare their effectiveness for Gram-positive vs. Gram-negative bacteria. Lower MIC values indicate higher effectiveness.
""") 
show_sidebar_footer()

# Footer with contact info
st.markdown("""
---
<div style='text-align: right;'>
    <sub>
        Built by <a href="https://github.com/ahnsv" target="_blank">@ahnsv</a> | 
        <a href="https://www.linkedin.com/in/humphrey-ahn" target="_blank">LinkedIn</a>
    </sub>
</div>
""", unsafe_allow_html=True) 