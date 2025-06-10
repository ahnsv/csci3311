import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Burtin Antibiotic Dataset App", layout="wide")

st.title("Burtin's Antibiotic Dataset: Interactive Data Story")

# Menu Overview
st.markdown("""
Welcome to the interactive exploration of Burtin's Antibiotic Dataset!

**Menu Overview:**
- **01. Introduction:** Learn about the dataset, MIC, and Gram staining.
- **02. Data Exploration:** Filter and browse the raw data interactively.
- **03. Antibiotic Effectiveness:** Compare how effective each antibiotic is across bacteria.
- **04. Gram Staining Analysis:** See how Gram-positive and Gram-negative bacteria respond differently.
- **05. Outliers & Exceptions:** Discover bacteria that are unusually resistant or susceptible.
- **06. Summary & Recommendations:** Key findings and practical takeaways.

Use the sidebar to navigate between these pages.
""")

# Add a simple diagram to illustrate the data story
bacteria = ["Gram-positive", "Gram-negative"]
antibiotics = ["Penicillin", "Streptomycin", "Neomycin"]
data = []
for b in bacteria:
    for a in antibiotics:
        data.append({"Bacteria": b, "Antibiotic": a, "Effectiveness": 1 if b == "Gram-positive" and a == "Penicillin" else 0.6 if a != "Penicillin" else 0.3})
diagram_df = pd.DataFrame(data)
diagram = (
    alt.Chart(diagram_df)
    .mark_rect()
    .encode(
        x=alt.X("Antibiotic:N", title=None),
        y=alt.Y("Bacteria:N", title=None),
        color=alt.Color("Effectiveness:Q", scale=alt.Scale(scheme="greens"), legend=alt.Legend(title="Relative Effectiveness")),
        tooltip=["Bacteria", "Antibiotic", alt.Tooltip("Effectiveness", format=".2f")]
    )
    .properties(width=500, height=400, title="Antibiotic Effectiveness by Gram Type (Illustrative)")
)
st.altair_chart(diagram, use_container_width=False)

st.markdown("""
**Start by selecting a page from the sidebar.**
""")

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