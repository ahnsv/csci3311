import pandas as pd
import altair as alt
import streamlit as st


def policy_8(figure_counter: int):
    """Section 8 – Policy proposals and public support."""
    policies = [
        "Loan Forgiveness",
        "Free College",
        "Income-Driven Repayment",
        "Online Degrees",
    ]
    selected = st.multiselect(
        "Select policies to display", policies, default=policies, key="policy_select"
    )

    support = pd.DataFrame(
        {"Policy": policies, "Support": [0.60, 0.48, 0.55, 0.35]}
    )
    support = support[support["Policy"].isin(selected)]

    st.altair_chart(
        alt.Chart(support)
        .mark_bar()
        .encode(
            x="Policy:N",
            y=alt.Y("Support:Q", axis=alt.Axis(format="%")),
            color="Policy:N",
            tooltip=["Policy", alt.Tooltip("Support", format=".0%")],
        )
        .properties(title="Public Support for Affordability Policies", width=650),
        use_container_width=True,
    )
    st.caption(
        f"Figure {figure_counter}: Public support levels for selected policy proposals."
    )
    figure_counter += 1

    st.success("60 % of Americans support some form of student-debt relief.") 