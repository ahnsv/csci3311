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
