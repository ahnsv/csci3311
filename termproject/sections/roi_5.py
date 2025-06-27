import pandas as pd
import altair as alt
import streamlit as st


def roi_5(figure_counter: int):
    """Section 5 – Return-on-investment by degree field."""
    majors = ["Engineering", "Business", "Education", "Arts", "Health"]
    selected_major = st.selectbox("Select major", majors, key="roi_major_select")

    roi_data = pd.DataFrame(
        {
            "Major": majors,
            "Median Earnings": [80_000, 60_000, 45_000, 35_000, 70_000],
            "Median Debt": [25_000, 22_000, 18_000, 16_000, 20_000],
        }
    )

    # Earnings bar
    st.altair_chart(
        alt.Chart(roi_data)
        .transform_filter(alt.FieldEqualPredicate(field="Major", equal=selected_major))
        .mark_bar(color="#1f77b4")
        .encode(x="Major:N", y="Median Earnings:Q", tooltip=["Major", "Median Earnings"])
        .properties(title="Median Earnings by Major", width=400),
        use_container_width=True,
    )
    st.caption(f"Figure {figure_counter}: Median earnings for {selected_major} graduates.")
    figure_counter += 1

    # Debt bar
    st.altair_chart(
        alt.Chart(roi_data)
        .transform_filter(alt.FieldEqualPredicate(field="Major", equal=selected_major))
        .mark_bar(color="orange")
        .encode(x="Major:N", y="Median Debt:Q", tooltip=["Major", "Median Debt"])
        .properties(title="Median Student Debt by Major", width=400),
        use_container_width=True,
    )
    st.caption(f"Figure {figure_counter}: Median debt for {selected_major} graduates.")
    figure_counter += 1

    payoff_years = (roi_data.set_index("Major").loc[selected_major, "Median Debt"] * 1.0) / (
        roi_data.set_index("Major").loc[selected_major, "Median Earnings"] * 0.1
    )

    st.info(
        f"💡 **Quick math**: At a 10 % savings rate, it would take roughly **{payoff_years:.1f} years** to pay off the median debt for a {selected_major} degree."
    ) 