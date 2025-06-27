import os
import pandas as pd
import streamlit as st
from collegescore import CollegeScorecardClient


def fetch_college_data(year, control=None, state=None, per_page=100):
    fields = [
        f"{year}.cost.tuition.in_state",
        f"{year}.cost.tuition.out_of_state",
        f"{year}.cost.attendance.academic_year",
        f"{year}.cost.avg_net_price.public",
        f"{year}.cost.avg_net_price.private",
        f"{year}.student.size",
        f"{year}.student.demographics.race_ethnicity.white",
        f"{year}.student.demographics.race_ethnicity.black",
        f"{year}.student.demographics.race_ethnicity.hispanic",
        f"{year}.student.demographics.race_ethnicity.asian",
        f"{year}.student.demographics.race_ethnicity.aian",
        f"{year}.student.demographics.race_ethnicity.nhpi",
        f"{year}.student.demographics.race_ethnicity.two_or_more",
        f"{year}.student.demographics.race_ethnicity.non_resident_alien",
        f"{year}.student.demographics.race_ethnicity.unknown",
        f"{year}.student.demographics.first_generation",
        "school.name",
        "school.state",
        "school.control",
        "school.region_id",
        "school.ownership",
    ]
    filters = {}
    if control:
        filters["school.ownership"] = control
    if state:
        filters["school.state"] = state
    client = CollegeScorecardClient(api_key=os.getenv("COLLEGE_SCORECARD_API_KEY"))
    data = client.get_institutions(fields=fields, filters=filters, per_page=per_page)
    return data["results"]


def prepare_cost_data(df, year):
    cost_data = pd.DataFrame(
        {
            "Institution": df["school.name"],
            "State": df["school.state"],
            "Type": df["school.ownership"].map(
                {1: "Public", 2: "Private Nonprofit", 3: "Private For-Profit"}
            ),
            "In-State Tuition": pd.to_numeric(
                df.get(f"{year}.cost.tuition.in_state", 0), errors="coerce"
            ),
            "Out-of-State Tuition": pd.to_numeric(
                df.get(f"{year}.cost.tuition.out_of_state", 0), errors="coerce"
            ),
            "Total Cost": pd.to_numeric(
                df.get(f"{year}.cost.attendance.academic_year", 0), errors="coerce"
            ),
            "Net Price (Public)": pd.to_numeric(
                df.get(f"{year}.cost.avg_net_price.public", 0), errors="coerce"
            ),
            "Net Price (Private)": pd.to_numeric(
                df.get(f"{year}.cost.avg_net_price.private", 0), errors="coerce"
            ),
        }
    )
    cost_melted = cost_data.melt(
        id_vars=["Institution", "State", "Type"],
        value_vars=[
            "In-State Tuition",
            "Out-of-State Tuition",
            "Total Cost",
            "Net Price (Public)",
            "Net Price (Private)",
        ],
        var_name="Cost Type",
        value_name="Cost",
    )
    cost_melted = cost_melted[cost_melted["Cost"] > 0]
    avg_cost = cost_melted.groupby(["Type", "Cost Type"])["Cost"].mean().reset_index()
    return cost_data, cost_melted, avg_cost


def prepare_enrollment_data(df, year):
    enroll_data = pd.DataFrame(
        {
            "Institution": df["school.name"],
            "State": df["school.state"],
            "Type": df["school.ownership"].map(
                {1: "Public", 2: "Private Nonprofit", 3: "Private For-Profit"}
            ),
            "Enrollment": pd.to_numeric(
                df.get(f"{year}.student.size", 0), errors="coerce"
            ),
            "White": pd.to_numeric(
                df.get(f"{year}.student.demographics.race_ethnicity.white", 0),
                errors="coerce",
            ),
            "Black": pd.to_numeric(
                df.get(f"{year}.student.demographics.race_ethnicity.black", 0),
                errors="coerce",
            ),
            "Hispanic": pd.to_numeric(
                df.get(f"{year}.student.demographics.race_ethnicity.hispanic", 0),
                errors="coerce",
            ),
            "Asian": pd.to_numeric(
                df.get(f"{year}.student.demographics.race_ethnicity.asian", 0),
                errors="coerce",
            ),
            "First Gen": pd.to_numeric(
                df.get(f"{year}.student.demographics.first_generation", 0),
                errors="coerce",
            ),
        }
    )
    enroll_data = enroll_data[enroll_data["Enrollment"] > 0]
    enroll_by_type = enroll_data.groupby("Type")["Enrollment"].sum().reset_index()
    demo_cols = ["White", "Black", "Hispanic", "Asian", "First Gen"]
    demo_melted = enroll_data.melt(
        id_vars=["Institution", "Type"],
        value_vars=demo_cols,
        var_name="Demographic",
        value_name="Count",
    )
    demo_melted = demo_melted[demo_melted["Count"] > 0]
    return enroll_data, enroll_by_type, demo_melted


def fetch_tuition_by_year(year: int, per_page: int = 100) -> pd.DataFrame:
    """Fetch out-of-state tuition for all institutions for a single academic year.

    Args:
        year (int): Academic year (e.g. 2018 for 2018-2019 academic year fields in the API).
        per_page (int): Number of results per API page (College Scorecard maximum is 100).

    Returns:
        pd.DataFrame: DataFrame with ``id``, ``school.name``, ``school.state`` and tuition column.
    """
    client = CollegeScorecardClient(api_key=os.getenv("COLLEGE_SCORECARD_API_KEY"))
    tuition_field = f"{year}.cost.tuition.out_of_state"
    page: int = 0
    records: list[dict] = []

    while True:
        response = client.get_institutions(
            fields=[
                "id",
                "school.name",
                "school.state",
                tuition_field,
            ],
            page=page,
            per_page=per_page,
        )
        page_results = response.get("results", [])
        if not page_results:
            break
        records.extend(page_results)

        # Stop when last page returned fewer than ``per_page`` results to avoid extra API calls
        if len(page_results) < per_page:
            break
        page += 1
    # Create DataFrame and ensure numeric tuition
    df = pd.DataFrame.from_records(records)
    if df.empty:
        return df
    df = df.rename(columns={tuition_field: "tuition"})
    df["tuition"] = pd.to_numeric(df["tuition"], errors="coerce")
    return df.dropna(subset=["tuition"]).reset_index(drop=True)


def find_top_tuition_increase(
    start_year: int, end_year: int, top_n: int = 10
) -> pd.DataFrame:
    """Compute and return the institutions with the largest increase in out-of-state tuition.

    Args:
        start_year (int): Baseline academic year.
        end_year (int): Comparison academic year.
        top_n (int): Number of institutions to return.

    Returns:
        pd.DataFrame: Top ``top_n`` institutions sorted by tuition increase.
    """
    if end_year <= start_year:
        raise ValueError("`end_year` must be greater than `start_year`.")

    start_df = fetch_tuition_by_year(start_year)
    end_df = fetch_tuition_by_year(end_year)

    if start_df.empty or end_df.empty:
        raise RuntimeError("Failed to fetch tuition data for the specified years.")

    merged = start_df.merge(
        end_df[["id", "tuition"]].rename(columns={"tuition": "end_tuition"}),
        on="id",
        how="inner",
    )

    merged = merged.rename(columns={"tuition": "start_tuition"})
    merged["increase"] = merged["end_tuition"] - merged["start_tuition"]

    top = (
        merged.sort_values("increase", ascending=False)
        .head(top_n)
        .loc[
            :,
            ["school.name", "school.state", "start_tuition", "end_tuition", "increase"],
        ]
        .reset_index(drop=True)
    )
    return top
