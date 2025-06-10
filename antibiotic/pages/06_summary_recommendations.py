# Page Title: Summary & Recommendations
import streamlit as st
import altair as alt
import pandas as pd
from antibiotic_utils import show_sidebar_footer

st.set_page_config(page_title="06. Summary & Recommendations", layout="wide")
st.title("06. Summary & Recommendations")

st.markdown("""
## Key Findings

- **Antibiotic Effectiveness:**
    - Penicillin is generally less effective (higher MIC) against Gram-negative bacteria.
    - Streptomycin and Neomycin show broader effectiveness, but some bacteria remain resistant.
- **Gram Staining:**
    - Gram-negative bacteria tend to be more resistant overall.
    - Gram-positive bacteria are more susceptible to Penicillin.
- **Outliers:**
    - Some bacteria (e.g., Salmonella, Proteus) are highly resistant to all antibiotics.
    - Others (e.g., Pneumococcus, Streptococcus) are highly susceptible, especially to Penicillin.
""")

# Traffic light summary diagram
st.markdown("### Antibiotic Recommendations by Gram Type (Traffic Light)")
st.write("This diagram summarizes which antibiotics are recommended, conditional, or should be avoided for Gram-positive and Gram-negative bacteria, using a traffic light color scheme.")
data = [
    {"Gram Type": "Gram-positive", "Antibiotic": "Penicillin", "Recommendation": "Recommended", "Color": "green"},
    {"Gram Type": "Gram-positive", "Antibiotic": "Streptomycin", "Recommendation": "Conditional", "Color": "yellow"},
    {"Gram Type": "Gram-positive", "Antibiotic": "Neomycin", "Recommendation": "Conditional", "Color": "yellow"},
    {"Gram Type": "Gram-negative", "Antibiotic": "Penicillin", "Recommendation": "Avoid", "Color": "red"},
    {"Gram Type": "Gram-negative", "Antibiotic": "Streptomycin", "Recommendation": "Recommended", "Color": "green"},
    {"Gram Type": "Gram-negative", "Antibiotic": "Neomycin", "Recommendation": "Recommended", "Color": "green"},
]
df = pd.DataFrame(data)
chart = (
    alt.Chart(df)
    .mark_circle(size=400)
    .encode(
        x=alt.X("Antibiotic:N", title=None),
        y=alt.Y("Gram Type:N", title=None),
        color=alt.Color("Color:N", scale=alt.Scale(domain=["green", "yellow", "red"], range=["#4CAF50", "#FFEB3B", "#F44336"]), legend=None),
        tooltip=["Gram Type", "Antibiotic", "Recommendation"]
    )
    .properties(width=500, height=400, title="Antibiotic Recommendations by Gram Type (Traffic Light)")
)
st.altair_chart(chart, use_container_width=False)

st.markdown("""
## Recommendations

- **For Gram-positive infections:** Penicillin is often effective, but always check susceptibility.
- **For Gram-negative infections:** Consider Streptomycin or Neomycin, as Penicillin is usually ineffective.
- **Always consult susceptibility data** for the specific bacterial species before choosing an antibiotic.

---
This concludes the interactive exploration of Burtin's Antibiotic Dataset. Use the sidebar to revisit any page or explore the data further!
""")

show_sidebar_footer() 