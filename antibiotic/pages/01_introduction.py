# Page Title: Introduction
import streamlit as st
import altair as alt
import pandas as pd
from antibiotic_utils import show_sidebar_footer

st.set_page_config(page_title="Burtin Antibiotic Dataset: Introduction", layout="wide")

st.title("01. Introduction")

st.markdown("""
### Welcome!
This interactive app explores **Burtin's Antibiotic Dataset**, which records the minimum inhibitory concentration (MIC) of three antibiotics—Penicillin, Streptomycin, and Neomycin—against 16 bacterial species.

**Key Concepts:**
- **MIC (Minimum Inhibitory Concentration):** The lowest concentration of an antibiotic that prevents visible growth of a bacterium. Lower MIC = more effective antibiotic.
- **Gram Staining:** Bacteria are classified as **Gram-positive** or **Gram-negative** based on their cell wall structure. This affects how they respond to antibiotics.

**How to Use This App:**
- Use the sidebar to navigate between pages.
- Interact with tables and charts to filter, highlight, and explore the data.
- Look for annotations and color cues to guide your interpretation.

---
""")

# Infographic: Antibiotics and Gram Types
st.markdown("### Antibiotics and Gram Types")
st.write("This diagram shows the three antibiotics studied in the dataset and the two main Gram stain types of bacteria. These categories are central to the analysis throughout this app.")
antibiotics = ["Penicillin", "Streptomycin", "Neomycin"]
gram_types = ["Gram-positive", "Gram-negative"]
info_data = []
for g in gram_types:
    for a in antibiotics:
        info_data.append({"Gram Type": g, "Antibiotic": a, "Value": 1})
info_df = pd.DataFrame(info_data)
info_chart = (
    alt.Chart(info_df)
    .mark_text(fontSize=18, fontWeight="bold")
    .encode(
        x=alt.X("Antibiotic:N", axis=alt.Axis(title=None)),
        y=alt.Y("Gram Type:N", axis=alt.Axis(title=None)),
        text=alt.Text("Antibiotic:N"),
        color=alt.Color("Gram Type:N", scale=alt.Scale(domain=gram_types, range=["#4CAF50", "#2196F3"]), legend=None)
    )
    .properties(width=500, height=400, title="Antibiotics and Gram Types")
)
st.altair_chart(info_chart, use_container_width=False)

st.markdown("""
---
**Ready?** Use the sidebar to start exploring the data!
""")

show_sidebar_footer()
