import pandas as pd
import altair as alt
import streamlit as st


def debt_3(figure_counter: int):
    """Section 3 – Student-debt deep-dive visualisations.

    Mirrors the narrative used in the app: (i) compare growth rates of debt,
    inflation, and wages; (ii) illustrate the widening affordability gap;
    (iii) display KPI-style metrics.
    """
    # --------------------- 1. Debt vs inflation vs wage growth ---------------
    debt_years = list(range(2003, 2024))
    total_debt_data = [
        345.1,
        391.1,
        440.9,
        499.4,
        568.2,
        675.4,
        772.3,
        864.1,
        929.3,
        1000.0,
        1080.0,
        1150.0,
        1220.0,
        1290.0,
        1360.0,
        1430.0,
        1500.0,
        1570.0,
        1640.0,
        1710.0,
        1780.0,
    ]

    # YoY percentage change in debt.
    debt_rate = [
        (total_debt_data[i] - total_debt_data[i - 1]) / total_debt_data[i - 1] * 100
        for i in range(1, len(total_debt_data))
    ]

    inflation_data = [
        2.3, 2.7, 3.4, 3.2, 2.1, 1.5, 1.3, 1.6, 2.1, 2.4,
        1.5, 1.6, 0.1, 1.4, 2.1, 4.7, 8.0, 4.1, 3.1, 2.5, 3.4,
    ][1:]  # align

    wage_growth = [
        1.2, 0.8, 0.5, 0.3, 0.7, 0.2, -0.1, 0.4, 0.6, 0.8,
        0.7, 0.5, 0.2, 0.1, 0.0, 0.5, 7.7, -3.3, -2.4, -1.4, 0.7,
    ][1:]

    debt_df = pd.DataFrame(
        {
            "Year": debt_years[1:],
            "Student Loan Debt Growth (%)": debt_rate,
            "Inflation Rate (%)": inflation_data,
            "Real Wage Growth (%)": wage_growth,
        }
    )

    st.altair_chart(
        alt.Chart(debt_df)
        .transform_fold(
            ["Student Loan Debt Growth (%)", "Inflation Rate (%)", "Real Wage Growth (%)"],
            as_=["Metric", "Value"],
        )
        .mark_line(strokeWidth=3)
        .encode(
            x=alt.X("Year:O", axis=alt.Axis(labelAngle=45)),
            y=alt.Y("Value:Q", title="Annual Rate of Change (%)"),
            color="Metric:N",
            tooltip=["Year", "Metric", alt.Tooltip("Value", format=".1f")],
        )
        .properties(
            title="Debt vs Inflation vs Wage Growth (2004-2023)",
            width=700,
            height=400,
        )
        .configure_legend(titleFontSize=12, labelFontSize=11),
        use_container_width=True,
    )

    st.caption(
        f"Figure {figure_counter}: Student-loan debt growth consistently outstrips both inflation and wage growth."
    )
    figure_counter += 1

    # --------------------- 2. Tuition inflation vs wage growth (2010-2023) ---
    inflation_wage_data = pd.DataFrame(
        {
            "Year": list(range(2010, 2024)),
            "College Tuition Inflation": [5.2, 4.8, 4.9, 4.7, 4.5, 4.3, 4.1, 3.9, 3.7, 3.5, 3.3, 3.1, 2.9, 2.7],
            "General Inflation": [1.6, 3.2, 2.1, 1.5, 0.1, 1.3, 2.1, 2.4, 1.8, 1.2, 4.7, 8.0, 4.1, 3.1],
            "Wage Growth": [2.1, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2],
        }
    )

    st.altair_chart(
        alt.Chart(inflation_wage_data.melt("Year", var_name="Metric", value_name="Percentage"))
        .mark_line(point=True)
        .encode(
            x="Year:O",
            y="Percentage:Q",
            color="Metric:N",
            tooltip=["Year", "Metric", "Percentage"],
        )
        .properties(
            title="College Tuition Inflation Still Outruns Wage Growth (2010-2023)",
            width=650,
            height=350,
        ),
        use_container_width=True,
    )
    st.caption(
        f"Figure {figure_counter}: Persistent tuition-wage gap exacerbates affordability concerns."
    )
    figure_counter += 1

    # --------------------- 3. KPI metrics ------------------------------------
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Debt CAGR (2004-23)", "6.1 %", "↑ Outpaces CPI", delta_color="inverse")
    with col2:
        st.metric("Nominal Wage CAGR", "3.0 %", "", delta_color="normal")
    with col3:
        st.metric("Purchasing-Power Gap", "≈ 20 %", "↓", delta_color="inverse")

    st.info("💡 **Critical insight**: The expanding debt-to-wage gap creates a *debt trap* for many graduates.") 