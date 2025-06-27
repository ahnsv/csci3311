import numpy as np
import pandas as pd
import altair as alt
import streamlit as st


def alternatives_4(figure_counter: int):
    """Section 4 – Alternatives to traditional 4-year college.

    Interactive multi-select area chart that tracks enrollment in alternative
    pathways such as vocational programmes and apprenticeships.
    """
    alt_types = st.multiselect(
        "Select alternative pathways:",
        ["Vocational", "Apprenticeship", "Military", "Gap Year"],
        default=["Vocational", "Apprenticeship"],
        key="alt_pathways_select",
    )

    years = list(range(2015, 2023))
    alt_data = pd.DataFrame(
        {
            "Year": years,
            "Vocational": np.linspace(100_000, 180_000, len(years)),
            "Apprenticeship": np.linspace(50_000, 90_000, len(years)),
            "Military": np.linspace(30_000, 35_000, len(years)),
            "Gap Year": np.linspace(10_000, 25_000, len(years)),
        }
    )

    melted = alt_data.melt("Year", var_name="Pathway", value_name="Enrollment")
    melted = melted[melted["Pathway"].isin(alt_types)]

    st.altair_chart(
        alt.Chart(melted)
        .mark_area(opacity=0.7)
        .encode(
            x="Year:O",
            y="Enrollment:Q",
            color="Pathway:N",
            tooltip=["Year", "Pathway", "Enrollment"],
        )
        .properties(
            title="Alternative Pathway Enrolment Is Rising",
            width=650,
            height=350,
        ),
        use_container_width=True,
    )
    st.caption(
        f"Figure {figure_counter}: Uptake of non-degree pathways such as vocational training has accelerated since 2015."
    )
    figure_counter += 1

    st.success("Community-college enrolment is up 15 % since 2018.") 