# Page Title: Outliers & Exceptions
import streamlit as st
import pandas as pd
from antibiotic_utils import load_burtin_data, get_antibiotics, show_sidebar_footer
import altair as alt

st.set_page_config(page_title="05. Outliers & Exceptions", layout="wide")
st.title("05. Outliers & Exceptions")

# Load data
@st.cache_data
def get_data():
    return load_burtin_data()

df = get_data()

# Sidebar: select antibiotic
antibiotics = get_antibiotics()
selected_antibiotic = st.sidebar.selectbox("Select Antibiotic", antibiotics)

# Find outliers: top 2 most resistant (highest MIC) and top 2 most susceptible (lowest MIC)
sorted_df = df.sort_values(selected_antibiotic)
most_susceptible = sorted_df.head(2)
most_resistant = sorted_df.tail(2)

highlight = pd.concat([most_susceptible, most_resistant])

# Bar chart: highlight outliers
st.markdown("### Outlier Bacteria for Selected Antibiotic")
st.write("This bar chart highlights the two most susceptible and two most resistant bacteria (in orange) for the selected antibiotic. These outliers may warrant special attention in clinical decisions.")
chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("Bacteria:N", sort="-y", title="Bacterial Species"),
        y=alt.Y(f"{selected_antibiotic}:Q", title="MIC (lower = more effective)"),
        color=alt.condition(
            alt.FieldOneOfPredicate(field="Bacteria", oneOf=highlight["Bacteria"].tolist()),
            alt.value("orange"),
            alt.value("steelblue")
        ),
        tooltip=["Bacteria", f"{selected_antibiotic}", "Gram_Staining"]
    )
    .properties(width=800, height=400)
    .interactive()
)
st.altair_chart(chart, use_container_width=True)

# Scatter plot: all bacteria, outliers annotated
st.markdown("### Outlier Annotation: Susceptible and Resistant Bacteria")
st.write("This scatter plot shows all bacteria for the selected antibiotic, with outliers labeled in orange. Use this to quickly spot which bacteria are most and least affected by the antibiotic.")
scatter = (
    alt.Chart(df)
    .mark_circle(size=120)
    .encode(
        x=alt.X("Bacteria:N", sort="-y", title="Bacterial Species"),
        y=alt.Y(f"{selected_antibiotic}:Q", title="MIC (lower = more effective)"),
        color=alt.condition(
            alt.FieldOneOfPredicate(field="Bacteria", oneOf=highlight["Bacteria"].tolist()),
            alt.value("orange"),
            alt.value("gray")
        ),
        tooltip=["Bacteria", f"{selected_antibiotic}", "Gram_Staining"]
    )
    .properties(width=800, height=600, title="Outliers Highlighted (Orange)")
)
# Annotate outliers
text = (
    alt.Chart(highlight)
    .mark_text(align="left", dx=5, dy=-10, fontSize=12, fontWeight="bold", color="orange")
    .encode(
        x=alt.X("Bacteria:N", sort="-y"),
        y=alt.Y(f"{selected_antibiotic}:Q"),
        text=alt.Text("Bacteria:N")
    )
)
st.altair_chart(scatter + text, use_container_width=True)

st.markdown("""
- **Highlighted in orange:** The two most susceptible and two most resistant bacteria for the selected antibiotic.
- **Tip:** Use the sidebar to change the antibiotic and see which bacteria are outliers.
""")

show_sidebar_footer() 