import pandas as pd
import altair as alt
import streamlit as st


def equity_6(figure_counter: int):
    """Section 6 – Equity and access visualisation."""
    groups = ["White", "Black", "Hispanic", "Asian", "First-Gen", "Low-Income"]
    selected_group = st.radio("Select demographic group", groups, key="equity_group_select")

    data = pd.DataFrame(
        {
            "Group": groups,
            "Attendance Rate": [0.65, 0.45, 0.40, 0.70, 0.35, 0.38],
        }
    )

    st.altair_chart(
        alt.Chart(data)
        .mark_bar()
        .encode(
            x="Group:N",
            y=alt.Y("Attendance Rate:Q", axis=alt.Axis(format=".0%")),
            color="Group:N",
            tooltip=["Group", alt.Tooltip("Attendance Rate", format=".0%")],
        )
        .properties(title="College Attendance Rate by Group", width=650),
        use_container_width=True,
    )
    st.caption(
        f"Figure {figure_counter}: Attendance rates highlight persistent equity gaps."
    )
    figure_counter += 1

    if selected_group in ["First-Gen", "Low-Income"]:
        st.warning("Students in this group are significantly less likely to graduate on time.")
    else:
        st.info("Hover over the bars to compare attendance rates across groups.") 