import pandas as pd
import altair as alt
import streamlit as st


def cultural_7(figure_counter: int):
    """Section 7 – Cultural perceptions of success visualisation."""
    importance = st.slider("How important is a college degree for success?", 0, 100, 60)
    st.progress(importance)

    poll_data = pd.DataFrame(
        {
            "Value": ["Skills", "Degree", "Experience", "Network", "Entrepreneurship"],
            "Percent": [35, 25, 20, 10, 10],
        }
    )

    st.altair_chart(
        alt.Chart(poll_data)
        .mark_bar()
        .encode(
            x="Value:N",
            y="Percent:Q",
            color="Value:N",
            tooltip=["Value", "Percent"],
        )
        .properties(title="What Americans Value for Success", width=650),
        use_container_width=True,
    )
    st.caption(
        f"Figure {figure_counter}: Poll results show skills outrank degrees as the primary marker of success."
    )
    figure_counter += 1

    st.info("Only 25 % of young adults say a degree is 'very important' for success.") 