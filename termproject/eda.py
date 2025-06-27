# %%
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import altair as alt
import streamlit as st
import numpy as np

from collegescore import CollegeScorecardClient

# %%
client = CollegeScorecardClient()

# %%
import os
from data import fetch_tuition_by_year

os.environ["COLLEGE_SCORECARD_API_KEY"] = "VQQNGo4ffzEGIwWQxfhdRGei643ryph5VkciCmlM"
results = fetch_tuition_by_year(2022)

results.head()
# %%

results.to_csv("./tuition_by_year_2022.csv", index=False)


# %%

for year in range(2017, 2022):
    results = fetch_tuition_by_year(year)
    results.to_csv(f"./tuition_by_year_{year}.csv", index=False)

# %%
# data = []
# years = list(range(2017, 2022))

# for year in years:
year = 2019
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
    f"{year}.cost.booksupply",
    f"{year}.cost.roomboard.oncampus",
    f"{year}.cost.roomboard.offcampus",
    f"{year}.cost.transportation",
    f"{year}.cost.otherexpense.offcampus",
    f"{year}.cost.otherexpense.oncampus",
    f"{year}.aid.median_debt.completers.overall",
    f"{year}.aid.median_debt.noncompleters",
    f"{year}.aid.median_debt.income.0_30000",
    f"{year}.aid.median_debt.income.30001_75000",
    f"{year}.aid.median_debt.income.greater_than_75000",
    f"{year}.aid.median_debt.dependent_students",
    f"{year}.aid.median_debt.independent_students",
    f"{year}.aid.median_debt.pell_grant",
    f"{year}.aid.median_debt.no_pell_grant",
    f"{year}.aid.median_debt.female_students",
    f"{year}.aid.median_debt.male_students",
    f"{year}.aid.median_debt.first_generation_students",
    f"{year}.aid.median_debt.non_first_generation_students",
    f"{year}.aid.median_debt.number.overall",
    f"{year}.aid.median_debt.number.completers",
    f"{year}.aid.median_debt.number.noncompleters",
    f"{year}.aid.median_debt.number.income.0_30000",
    f"{year}.aid.median_debt.number.income.30001_75000",
    f"{year}.aid.median_debt.number.income.greater_than_75000",
    f"{year}.aid.median_debt.number.dependent_students",
    f"{year}.aid.median_debt.number.independent_students",
    f"{year}.aid.median_debt.number.pell_grant",
    f"{year}.aid.median_debt.number.no_pell_grant",
    f"{year}.aid.median_debt.number.female_students",
    f"{year}.aid.median_debt.number.male_students",
    f"{year}.aid.median_debt.number.first_generation_students",
    f"{year}.aid.median_debt.number.non_first_generation_students",
    f"{year}.aid.median_debt.completers.monthly_payments",
    *[
        f"{year}.earnings.{i}_yrs_after_entry.median_earnings_lowest_tercile"
        for i in range(6, 13)
    ],
    *[
        f"{year}.earnings.{i}_yrs_after_entry.median_earnings_highest_tercile"
        for i in range(6, 13)
    ],
    *[
        f"{year}.earnings.{i}_yrs_after_entry.median_earnings_middle_tercile"
        for i in range(6, 13)
    ],
    *[
        f"{year}.earnings.{i}_yrs_after_entry.median_earnings_independent"
        for i in range(6, 13)
    ],
    *[
        f"{year}.earnings.{i}_yrs_after_entry.median_earnings_dependent"
        for i in range(6, 13)
    ],
    *[
        f"{year}.earnings.{i}_yrs_after_entry.median_earnings_non_male"
        for i in range(6, 13)
    ],
    *[
        f"{year}.earnings.{i}_yrs_after_entry.median_earnings_male"
        for i in range(6, 13)
    ],
    "school.name",
    "school.state",
    "school.control",
    "school.region_id",
    "school.ownership",
]
filters = {}
client = CollegeScorecardClient(api_key=os.getenv("COLLEGE_SCORECARD_API_KEY"))
data = client.get_institutions(fields=fields, filters=filters, per_page=100)

results_df = pd.DataFrame(data["results"]).dropna(
    subset=[f"{year}.aid.median_debt.completers.overall"]
)
results_df
# %%
data = pd.concat(data)
data.to_csv("./tuition_by_year_2017_2021.csv", index=False)

# %%
from concurrent.futures import ThreadPoolExecutor

dfs: list[pd.DataFrame] = []
for year in range(2017, 2022):
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
        f"{year}.cost.booksupply",
        f"{year}.cost.roomboard.oncampus",
        f"{year}.cost.roomboard.offcampus",
        f"{year}.cost.transportation",
        f"{year}.cost.otherexpense.offcampus",
        f"{year}.cost.otherexpense.oncampus",
        f"{year}.aid.median_debt.completers.overall",
        f"{year}.aid.median_debt.noncompleters",
        f"{year}.aid.median_debt.income.0_30000",
        f"{year}.aid.median_debt.income.30001_75000",
        f"{year}.aid.median_debt.income.greater_than_75000",
        f"{year}.aid.median_debt.dependent_students",
        f"{year}.aid.median_debt.independent_students",
        f"{year}.aid.median_debt.pell_grant",
        f"{year}.aid.median_debt.no_pell_grant",
        f"{year}.aid.median_debt.female_students",
        f"{year}.aid.median_debt.male_students",
        f"{year}.aid.median_debt.first_generation_students",
        f"{year}.aid.median_debt.non_first_generation_students",
        f"{year}.aid.median_debt.number.overall",
        f"{year}.aid.median_debt.number.completers",
        f"{year}.aid.median_debt.number.noncompleters",
        f"{year}.aid.median_debt.number.income.0_30000",
        f"{year}.aid.median_debt.number.income.30001_75000",
        f"{year}.aid.median_debt.number.income.greater_than_75000",
        f"{year}.aid.median_debt.number.dependent_students",
        f"{year}.aid.median_debt.number.independent_students",
        f"{year}.aid.median_debt.number.pell_grant",
        f"{year}.aid.median_debt.number.no_pell_grant",
        f"{year}.aid.median_debt.number.female_students",
        f"{year}.aid.median_debt.number.male_students",
        f"{year}.aid.median_debt.number.first_generation_students",
        f"{year}.aid.median_debt.number.non_first_generation_students",
        f"{year}.aid.median_debt.completers.monthly_payments",
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_lowest_tercile"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_highest_tercile"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_middle_tercile"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_independent"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_dependent"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_non_male"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_male"
            for i in range(6, 13)
        ],
        "school.name",
        "school.state",
        "school.control",
        "school.region_id",
        "school.ownership",
    ]
    client = CollegeScorecardClient(api_key=os.getenv("COLLEGE_SCORECARD_API_KEY"))
    # concurrent requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(
                client.get_institutions,
                fields=fields,
                filters=filters,
                per_page=100,
                page=page,
            )
            for page in range(1, 20)
        ]
        results = [future.result() for future in futures]
    results_df_2 = pd.concat([pd.DataFrame(result["results"]) for result in results])
    # add column for year and rename all columns except school.name and school.state to remove the year from the column name

    rest_page = 20
    while True:
        response = client.get_institutions(
            fields=fields, filters=filters, per_page=100, page=rest_page
        )
        page_results = response.get("results", [])
        if not page_results:
            break
        results_df_2 = pd.concat([results_df_2, pd.DataFrame(page_results)])
        rest_page += 1

    results_df_2["year"] = year
    results_df_2 = results_df_2.rename(
        columns={
            col: col.replace(f"{year}.", "")
            for col in results_df_2.columns
            if col != "school.name" and col != "school.state"
        },
        inplace=True,
    )

    if len(dfs) != 0:
        assert results_df_2.shape[1] == dfs[-1].shape[1], (
            f"Shape mismatch: {results_df_2.shape[1]} != {dfs[-1].shape[1]}"
        )
    dfs.append(results_df_2)


pd.concat(dfs).head()
# %%
all_df = pd.concat(dfs)
all_df.to_csv("./tuition_debt_cost_2017_2021_2.csv", index=False)

# %%
import numpy as np
# Prepare data for cost_1.py visualizations

# 1. Historical tuition trends
tuition_trends = all_df.groupby(['year', 'school.ownership'])[['cost.tuition.in_state', 'cost.tuition.out_of_state']].mean().reset_index()

# Map school.control to institution types
control_map = {
    1: 'Public',
    2: 'Private Nonprofit',
    3: 'Private For-Profit'
}
tuition_trends['Institution Type'] = tuition_trends['school.ownership'].map(control_map)

# Create separate rows for in-state and out-of-state tuition at public institutions
public_tuition = tuition_trends[tuition_trends['Institution Type'] == 'Public'].copy()
public_tuition_in = public_tuition.copy()
public_tuition_in['Institution Type'] = 'Public In-State'
public_tuition_in['Tuition'] = public_tuition_in['cost.tuition.in_state']
public_tuition_out = public_tuition.copy()
public_tuition_out['Institution Type'] = 'Public Out-of-State'
public_tuition_out['Tuition'] = public_tuition_out['cost.tuition.out_of_state']

private_tuition = tuition_trends[tuition_trends['Institution Type'] != 'Public'].copy()
private_tuition['Tuition'] = private_tuition['cost.tuition.in_state']  # Use in-state as private institutions typically have one rate

historical_tuition = pd.concat([
    public_tuition_in[['year', 'Institution Type', 'Tuition']],
    public_tuition_out[['year', 'Institution Type', 'Tuition']],
    private_tuition[['year', 'Institution Type', 'Tuition']]
])

# 2. Sticker Price vs Net Price by year
cost_comparison = all_df.groupby(['year', 'school.ownership']).agg({
    'cost.attendance.academic_year': 'mean',  # Sticker Price
    'cost.avg_net_price.public': 'mean',     # Net Price for public
    'cost.avg_net_price.private': 'mean'     # Net Price for private
}).reset_index()

cost_comparison['Institution Type'] = cost_comparison['school.ownership'].map(control_map)
cost_comparison['Net Price'] = np.where(
    cost_comparison['school.ownership'] == 1,
    cost_comparison['cost.avg_net_price.public'],
    cost_comparison['cost.avg_net_price.private']
)
cost_comparison['Sticker Price'] = cost_comparison['cost.attendance.academic_year']
cost_comparison['Average Aid'] = cost_comparison['Sticker Price'] - cost_comparison['Net Price']

# 3. Cost Breakdown by year
cost_breakdown = all_df.groupby(['year', 'school.ownership']).agg({
    'cost.tuition.in_state': 'mean',          # Tuition
    'cost.roomboard.oncampus': 'mean',        # Room & Board
    'cost.booksupply': 'mean',                # Books & Supplies
    'cost.otherexpense.oncampus': 'mean'      # Other Expenses
}).reset_index()

cost_breakdown['Institution Type'] = cost_breakdown['school.ownership'].map(control_map)

# Save processed data for cost_1.py
historical_tuition.to_csv('./historical_tuition.csv', index=False)
cost_comparison.to_csv('./cost_comparison.csv', index=False)
cost_breakdown.to_csv('./cost_breakdown.csv', index=False)

# %%

cost_breakdown

# %%

# Prepare data for roi_5.py visualizations

# Get the most recent year's data for the latest earnings information

earnings_history = []
for year in range(2010, 2016):
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
        f"{year}.cost.booksupply",
        f"{year}.cost.roomboard.oncampus",
        f"{year}.cost.roomboard.offcampus",
        f"{year}.cost.transportation",
        f"{year}.cost.otherexpense.offcampus",
        f"{year}.cost.otherexpense.oncampus",
        f"{year}.aid.median_debt.completers.overall",
        f"{year}.aid.median_debt.noncompleters",
        f"{year}.aid.median_debt.income.0_30000",
        f"{year}.aid.median_debt.income.30001_75000",
        f"{year}.aid.median_debt.income.greater_than_75000",
        f"{year}.aid.median_debt.dependent_students",
        f"{year}.aid.median_debt.independent_students",
        f"{year}.aid.median_debt.pell_grant",
        f"{year}.aid.median_debt.no_pell_grant",
        f"{year}.aid.median_debt.female_students",
        f"{year}.aid.median_debt.male_students",
        f"{year}.aid.median_debt.first_generation_students",
        f"{year}.aid.median_debt.non_first_generation_students",
        f"{year}.aid.median_debt.number.overall",
        f"{year}.aid.median_debt.number.completers",
        f"{year}.aid.median_debt.number.noncompleters",
        f"{year}.aid.median_debt.number.income.0_30000",
        f"{year}.aid.median_debt.number.income.30001_75000",
        f"{year}.aid.median_debt.number.income.greater_than_75000",
        f"{year}.aid.median_debt.number.dependent_students",
        f"{year}.aid.median_debt.number.independent_students",
        f"{year}.aid.median_debt.number.pell_grant",
        f"{year}.aid.median_debt.number.no_pell_grant",
        f"{year}.aid.median_debt.number.female_students",
        f"{year}.aid.median_debt.number.male_students",
        f"{year}.aid.median_debt.number.first_generation_students",
        f"{year}.aid.median_debt.number.non_first_generation_students",
        f"{year}.aid.median_debt.completers.monthly_payments",
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_lowest_tercile"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_highest_tercile"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_middle_tercile"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_independent"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_dependent"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_non_male"
            for i in range(6, 13)
        ],
        *[
            f"{year}.earnings.{i}_yrs_after_entry.median_earnings_male"
            for i in range(6, 13)
        ],
        "school.name",
        "school.state",
        "school.control",
        "school.region_id",
        "school.ownership",
    ]
    client = CollegeScorecardClient(api_key=os.getenv("COLLEGE_SCORECARD_API_KEY"))
    # concurrent requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(
                client.get_institutions,
                fields=fields,
                filters=filters,
                per_page=100,
                page=page,
            )
            for page in range(1, 20)
        ]
        results = [future.result() for future in futures]
    earnings_df = pd.concat([pd.DataFrame(result["results"]) for result in results])
    # add column for year and rename all columns except school.name and school.state to remove the year from the column name

    rest_page = 20
    while True:
        response = client.get_institutions(
            fields=fields, filters=filters, per_page=100, page=rest_page
        )
        page_results = response.get("results", [])
        if not page_results:
            break
        earnings_df = pd.concat([earnings_df, pd.DataFrame(page_results)])
        rest_page += 1

    earnings_df["year"] = year
    earnings_df.rename(
        columns={
            col: col.replace(f"{year}.", "")
            for col in earnings_df.columns
            if col != "school.name" and col != "school.state"
        },
        inplace=True,
    )
    earnings_history.append(earnings_df)

earnings_history_df = pd.concat(earnings_history)

earnings_history_df.head()
# %%
latest_data = earnings_history_df[earnings_history_df['year'] == 2014]

# Calculate median earnings 10 years after entry (most mature earnings data)
earnings_cols = [col for col in latest_data.columns if '10_yrs_after_entry.median_earnings' in col]
debt_cols = [
    'aid.median_debt.completers.overall',
    'aid.median_debt.completers.monthly_payments'
]

# Aggregate earnings and debt data
roi_data = latest_data.groupby('school.ownership').agg({
    **{col: 'median' for col in earnings_cols},
    **{col: 'median' for col in debt_cols}
}).reset_index()

# Rename columns for clarity
roi_data = roi_data.rename(columns={
    'aid.median_debt.completers.overall': 'Median Debt',
    'aid.median_debt.completers.monthly_payments': 'Monthly Payments',
    'earnings.10_yrs_after_entry.median_earnings_lowest_tercile': 'Lower Tercile Earnings',
    'earnings.10_yrs_after_entry.median_earnings_middle_tercile': 'Middle Tercile Earnings',
    'earnings.10_yrs_after_entry.median_earnings_highest_tercile': 'Higher Tercile Earnings'
})

# Map ownership to institution types
ownership_map = {
    1: 'Public',
    2: 'Private Nonprofit',
    3: 'Private For-Profit'
}
roi_data['Institution Type'] = roi_data['school.ownership'].map(ownership_map)

# Calculate additional ROI metrics
roi_data['Years to Repay'] = roi_data['Median Debt'] / (roi_data['Middle Tercile Earnings'] * 0.1)  # Assuming 10% of income to debt
roi_data['Debt-to-Earnings Ratio'] = roi_data['Median Debt'] / roi_data['Middle Tercile Earnings']

# Save the ROI data
roi_data.to_csv('./roi_data.csv', index=False)

# Also prepare earnings progression data over years
years_after_entry = range(6, 11)  # 6 to 10 years after entry
earnings_progression = []

for year in all_df['year'].unique():
    year_data = all_df[all_df['year'] == year]
    for yrs in years_after_entry:
        col = f'earnings.{yrs}_yrs_after_entry.median_earnings_middle_tercile'
        if col in year_data.columns:
            median_earnings = year_data.groupby('school.ownership')[col].median().reset_index()
            median_earnings['Years After Entry'] = yrs
            median_earnings['Year'] = year
            earnings_progression.append(median_earnings)

earnings_progression_df = pd.concat(earnings_progression)
earnings_progression_df['Institution Type'] = earnings_progression_df['school.ownership'].map(ownership_map)

# Save earnings progression data
earnings_progression_df.to_csv('./earnings_progression.csv', index=False)

# %%

