"""Streamlit app: Interactive remake of Moseley's X‑ray law (1913)
Two designs built with Altair & Vega‑Lite.
Run with: streamlit run moseley_streamlit.py
Author: ChatGPT demo
"""

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Moseley X‑ray Redesign", layout="centered")


# ---------------------------------------------------------------------
# 1  Data handling helpers
# ---------------------------------------------------------------------
@st.cache_data
def load_sample() -> pd.DataFrame:
    """Tiny illustrative dataset (remove once you have the full CSV)."""
    records = [
        #   element  Z  series   sqrt_freq    wavelength(Å)  year
        ("Ca", 20, "Kα", 7.0, 3.47, 1913),
        ("Ca", 20, "Kβ", 7.6, 3.05, 1913),
        ("Sc", 21, "Kα", 7.4, 3.25, 1913),
        ("Sc", 21, "Kβ", 8.0, 2.93, 1913),
        ("Ti", 22, "Kα", 7.8, 3.05, 1913),
        ("Ti", 22, "Kβ", 8.3, 2.78, 1913),
        ("V", 23, "Kα", 8.1, 2.90, 1913),
        ("V", 23, "Kβ", 8.6, 2.64, 1913),
        ("Cr", 24, "Kα", 8.4, 2.75, 1913),
        ("Cr", 24, "Kβ", 9.0, 2.53, 1913),
        ("Mn", 25, "Kα", 8.8, 2.60, 1913),
        ("Mn", 25, "Kβ", 9.3, 2.41, 1913),
        # L-series sample
        ("Ta", 73, "Lα", 15.2, 0.83, 1914),
        ("Ta", 73, "Lβ", 16.8, 0.75, 1914),
        ("W", 74, "Lα", 15.5, 0.80, 1914),
        ("W", 74, "Lβ", 17.1, 0.73, 1914),
    ]
    cols = ["element", "Z", "series", "sqrt_freq", "wavelength", "year"]
    return pd.DataFrame.from_records(records, columns=cols)


def get_data() -> pd.DataFrame:
    """Always load data from redesign/data/Moseley Data.csv."""
    return pd.read_csv("redesign/data/Moseley Data.csv")


# ---------------------------------------------------------------------
# 2  Periodic table helper (for Design B)
# ---------------------------------------------------------------------
@st.cache_data
def periodic_table_layout() -> pd.DataFrame:
    """Returns period+group positions for Z 1‑79 (up to Au)."""
    layout = [
        # period 1
        ("H", 1, 1, 1), ("He", 2, 1, 18),
        # period 2
        ("Li", 3, 2, 1), ("Be", 4, 2, 2), ("B", 5, 2, 13), ("C", 6, 2, 14), ("N", 7, 2, 15), ("O", 8, 2, 16), ("F", 9, 2, 17), ("Ne", 10, 2, 18),
        # period 3
        ("Na", 11, 3, 1), ("Mg", 12, 3, 2), ("Al", 13, 3, 13), ("Si", 14, 3, 14), ("P", 15, 3, 15), ("S", 16, 3, 16), ("Cl", 17, 3, 17), ("Ar", 18, 3, 18),
        # period 4
        ("K", 19, 4, 1), ("Ca", 20, 4, 2), ("Sc", 21, 4, 3), ("Ti", 22, 4, 4), ("V", 23, 4, 5), ("Cr", 24, 4, 6), ("Mn", 25, 4, 7), ("Fe", 26, 4, 8), ("Co", 27, 4, 9), ("Ni", 28, 4, 10), ("Cu", 29, 4, 11), ("Zn", 30, 4, 12), ("Ga", 31, 4, 13), ("Ge", 32, 4, 14), ("As", 33, 4, 15), ("Se", 34, 4, 16), ("Br", 35, 4, 17), ("Kr", 36, 4, 18),
        # period 5
        ("Rb", 37, 5, 1), ("Sr", 38, 5, 2), ("Y", 39, 5, 3), ("Zr", 40, 5, 4), ("Nb", 41, 5, 5), ("Mo", 42, 5, 6), ("Tc", 43, 5, 7), ("Ru", 44, 5, 8), ("Rh", 45, 5, 9), ("Pd", 46, 5, 10), ("Ag", 47, 5, 11), ("Cd", 48, 5, 12), ("In", 49, 5, 13), ("Sn", 50, 5, 14), ("Sb", 51, 5, 15), ("Te", 52, 5, 16), ("I", 53, 5, 17), ("Xe", 54, 5, 18),
        # period 6
        ("Cs", 55, 6, 1), ("Ba", 56, 6, 2), ("La", 57, 6, 3), ("Hf", 72, 6, 4), ("Ta", 73, 6, 5), ("W", 74, 6, 6), ("Re", 75, 6, 7), ("Os", 76, 6, 8), ("Ir", 77, 6, 9), ("Pt", 78, 6, 10), ("Au", 79, 6, 11), ("Hg", 80, 6, 12), ("Tl", 81, 6, 13), ("Pb", 82, 6, 14), ("Bi", 83, 6, 15), ("Po", 84, 6, 16), ("At", 85, 6, 17), ("Rn", 86, 6, 18),
        # period 7 (up to Z=79, so only Fr, Ra, Ac, and some transition elements)
        ("Fr", 87, 7, 1), ("Ra", 88, 7, 2), ("Ac", 89, 7, 3),
        # Lanthanides (period 6, group 3)
        ("Ce", 58, 8, 4), ("Pr", 59, 8, 5), ("Nd", 60, 8, 6), ("Pm", 61, 8, 7), ("Sm", 62, 8, 8), ("Eu", 63, 8, 9), ("Gd", 64, 8, 10), ("Tb", 65, 8, 11), ("Dy", 66, 8, 12), ("Ho", 67, 8, 13), ("Er", 68, 8, 14), ("Tm", 69, 8, 15), ("Yb", 70, 8, 16), ("Lu", 71, 8, 17),
    ]
    return pd.DataFrame(layout, columns=["element", "Z", "period", "group"])


# ---------------------------------------------------------------------
# 3  Design A – Scatter + regression lines
# ---------------------------------------------------------------------
def design_A(df: pd.DataFrame):
    st.header("Design A · Scatter with regression fit lines")
    # Interactive selection for unit (√freq vs wavelength)
    unit = st.radio(
        "Y-axis variable",
        options=["sqrt_freq", "wavelength"],
        index=0,
        format_func=lambda s: "√ frequency (×10⁸ √Hz)"
        if s == "sqrt_freq"
        else "Wavelength (Å)",
    )
    y_title = "√ frequency (×10⁸ √Hz)" if unit == "sqrt_freq" else "Wavelength (Å)"

    base = alt.Chart(df).encode(
        x=alt.X("Z:Q", title="Atomic number (Z)"),
        y=alt.Y(f"{unit}:Q", title=y_title),
        color=alt.Color("series:N", legend=alt.Legend(title="X‑ray series")),
        tooltip=[
            "element:N",
            "Z:Q",
            "series:N",
            "sqrt_freq:Q",
            "wavelength:Q",
            "year:Q",
        ],
    )

    points = base.mark_circle(size=80)
    reg_lines = base.transform_regression("Z", unit, groupby=["series"]).mark_line(size=2)

    chart = (reg_lines + points).interactive()
    st.altair_chart(chart, use_container_width=True)


# ---------------------------------------------------------------------
# 4  Design B – Small‑multiple slope charts + linked periodic table
# ---------------------------------------------------------------------
def design_B(df: pd.DataFrame):
    st.header("Design B · Small multiples & linked periodic table")

    # Build selection that links both views
    sel = alt.selection_single(fields=["element"], empty="none")
    # Periodic table layout
    pt = periodic_table_layout()
    pt_chart = (
        alt.Chart(pt)
        .mark_rect(strokeWidth=1)
        .encode(
            x=alt.X("group:O", title="Group"),
            y=alt.Y("period:O", title="Period", sort="descending"),
            color=alt.condition(sel, alt.value("goldenrod"), alt.value("lightgray")),
            tooltip=["element", "Z"],
        )
        .add_selection(sel)
        .properties(width=350, height=250)
    )

    # Add element symbols as text overlay
    text = (
        alt.Chart(pt)
        .mark_text(baseline="middle", align="center", fontSize=10)
        .encode(
            x="group:O",
            y="period:O",
            text="element",
            color=alt.condition(sel, alt.value("black"), alt.value("dimgray")),
        )
    )
    pt_chart = pt_chart + text

    # Create the faceted chart first
    slope_chart = (
        alt.Chart(df)
        .mark_circle(size=70)
        .encode(
            x=alt.X("Z:Q", title="Z"),
            y=alt.Y("sqrt_freq:Q", title="√ frequency", scale=alt.Scale(zero=False)),
            color=alt.Color("series:N", legend=None),
            opacity=alt.condition(sel, alt.value(1), alt.value(0.15)),
            tooltip=["element", "series", "sqrt_freq"],
        )
    )

    lines = (
        alt.Chart(df)
        .transform_regression("Z", "sqrt_freq", groupby=["series"])
        .mark_line(size=2)
        .encode(
            x="Z:Q",
            y="sqrt_freq:Q",
            color="series:N",
            opacity=alt.condition(sel, alt.value(1), alt.value(0.15)),
        )
    )

    # Create the faceted chart
    faceted_chart = (
        (lines + slope_chart)
        # .facet(
        #     row=alt.Row(
        #         "series:N",
        #         title="X‑ray series",
        #         sort=alt.EncodingSortField("series", order="ascending"),
        #     )
        # )
        .resolve_scale(x="shared", y="independent")
        .properties(width=350, height=120)
    )

    # Concatenate the charts
    final_chart = alt.hconcat(pt_chart, faceted_chart)
    st.altair_chart(final_chart, use_container_width=True)


# ---------------------------------------------------------------------
# 5  Main body
# ---------------------------------------------------------------------
df = get_data()

design = st.sidebar.radio("Choose a design", ("Design A", "Design B"), index=0)
if design == "Design A":
    design_A(df)
else:
    design_B(df)

st.caption(
    """**Tip**: upload a full Moseley dataset to explore; hover & click elements to see links between the periodic table and X‑ray trends."""
)
