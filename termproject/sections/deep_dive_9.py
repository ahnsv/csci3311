import pandas as pd
import altair as alt
import streamlit as st


def deep_dive_9(figure_counter: int):
    """Section 9 – Interactive deep-dive tabs."""
    tab1, tab2, tab3 = st.tabs(["Tuition", "Enrollment", "Debt"])

    with tab1:
        st.write("Explore tuition data.")
        st.dataframe(
            pd.DataFrame(
                {
                    "Institution": ["A", "B", "C"],
                    "In-State Tuition": [12_000, 15_000, 18_000],
                    "Out-of-State Tuition": [22_000, 25_000, 28_000],
                }
            )
        )
        st.caption(
            f"Figure {figure_counter}: Sample tuition data for selected institutions."
        )
        figure_counter += 1

    with tab2:
        st.write("Explore enrollment data.")
        st.dataframe(
            pd.DataFrame(
                {"Institution": ["A", "B", "C"], "Enrollment": [10_000, 15_000, 20_000]}
            )
        )
        st.caption(
            f"Figure {figure_counter}: Sample enrollment data for selected institutions."
        )
        figure_counter += 1

    with tab3:
        st.write("Explore debt data.")
        st.dataframe(
            pd.DataFrame(
                {"Institution": ["A", "B", "C"], "Avg Debt": [25_000, 30_000, 35_000]}
            )
        )
        st.caption(
            f"Figure {figure_counter}: Sample student-debt data for selected institutions."
        )
        figure_counter += 1

    st.info("Additional interactive charts can be added here once live data is available.") 