import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
from collegescore import CollegeScorecardClient

# Set page config
st.set_page_config(
    page_title="College Data Explorer - Appendix",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Add CSS for styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
    }
    .nav-button {
        padding: 0.5rem 1rem;
        color: white;
        background-color: #F8F8FF;
        border-radius: 0.25rem;
        text-decoration: none;
        font-weight: 500;
        margin-right: 0.5rem;
        display: inline-block;
    }
    .back-link {
        margin-top: 2rem;
        display: block;
        text-align: center;
    }
    .insight-box {
        background-color: #f0f9ff;
        border-left: 4px solid #0ea5e9;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    '<h1 class="main-header">College Data Explorer</h1>', unsafe_allow_html=True
)
st.markdown(
    '<h2 class="sub-header">Interactive Analysis of College Affordability Data</h2>',
    unsafe_allow_html=True,
)

# Main content
st.markdown("""
### Interactive College Data Explorer
Explore college affordability, costs, debt, and outcomes with our interactive tools.
""")

tool_options = {
    "data_explorer": "📊 Data Explorer",
    "tuition_trends": "📈 Tuition Trends", 
    "debt_analysis": "💰 Debt Analysis",
    "roi_calculator": "📈 ROI Calculator",
}

selected_tool = st.selectbox(
    "Choose your analysis tool:",
    list(tool_options.keys()),
    format_func=lambda x: tool_options[x],
    help="Select a tool to begin exploring college data"
)

# Quick stats
st.markdown("<h3>Dataset Overview</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Years Available", "2017-2022", "6 years of data")
with col2:
    st.metric("Institutions", "6,000+", "Across the U.S.")
with col3:
    st.metric("Data Points", "50+", "Per institution")
st.markdown("</div>", unsafe_allow_html=True)


# Helper functions
def fetch_college_data_for_appendix(years, state=None, ownership=None, per_page=100):
    """Fetch college data for multiple years with filters for state and ownership.

    Args:
        years (list): List of years to fetch data for
        state (str, optional): State abbreviation to filter by
        ownership (int, optional): School ownership code (1=Public, 2=Private nonprofit, 3=Private for-profit)
        per_page (int, optional): Number of results per page

    Returns:
        dict: Dictionary with years as keys and data as values
    """
    all_data = {}

    for year in years:
        fields = [
            f"{year}.cost.tuition.in_state",
            f"{year}.cost.tuition.out_of_state",
            f"{year}.cost.attendance.academic_year",
            f"{year}.cost.avg_net_price.public",
            f"{year}.cost.avg_net_price.private",
            f"{year}.aid.median_debt.completers.overall",
            f"{year}.aid.median_debt.income.0_30000",
            f"{year}.aid.median_debt.income.30001_75000",
            f"{year}.aid.median_debt.income.greater_than_75000",
            f"{year}.earnings.6_yrs_after_entry.median",
            f"{year}.earnings.7_yrs_after_entry.median",
            f"{year}.earnings.8_yrs_after_entry.median",
            f"{year}.student.size",
            "school.name",
            "school.state",
            "school.ownership",
            "id",
        ]

        filters = {}
        if state:
            filters["school.state"] = state
        if ownership:
            filters["school.ownership"] = ownership

        client = CollegeScorecardClient(api_key=os.getenv("COLLEGE_SCORECARD_API_KEY"))
        response = client.get_institutions(
            fields=fields, filters=filters, per_page=per_page
        )
        all_data[year] = response["results"]

    return all_data


def process_data_for_visualization(data_by_year):
    """Process the raw API data into a format suitable for visualization.

    Args:
        data_by_year (dict): Dictionary with years as keys and API response data as values

    Returns:
        pd.DataFrame: Processed data for visualization
    """
    processed_data = []

    for year, schools in data_by_year.items():
        for school in schools:
            # Skip schools with missing key data
            if not school.get("school.name") or not school.get("id"):
                continue

            school_data = {
                "year": year,
                "id": school.get("id"),
                "name": school.get("school.name"),
                "state": school.get("school.state"),
                "ownership_code": school.get("school.ownership"),
                "ownership": {
                    "1": "Public",
                    "2": "Private nonprofit",
                    "3": "Private for-profit",
                }.get(str(school.get("school.ownership")), "Unknown"),
                "tuition_in_state": pd.to_numeric(
                    school.get(f"{year}.cost.tuition.in_state"), errors="coerce"
                ),
                "tuition_out_of_state": pd.to_numeric(
                    school.get(f"{year}.cost.tuition.out_of_state"), errors="coerce"
                ),
                "total_cost": pd.to_numeric(
                    school.get(f"{year}.cost.attendance.academic_year"), errors="coerce"
                ),
                "net_price_public": pd.to_numeric(
                    school.get(f"{year}.cost.avg_net_price.public"), errors="coerce"
                ),
                "net_price_private": pd.to_numeric(
                    school.get(f"{year}.cost.avg_net_price.private"), errors="coerce"
                ),
                "median_debt": pd.to_numeric(
                    school.get(f"{year}.aid.median_debt.completers.overall"),
                    errors="coerce",
                ),
                "median_debt_low_income": pd.to_numeric(
                    school.get(f"{year}.aid.median_debt.income.0_30000"),
                    errors="coerce",
                ),
                "median_debt_mid_income": pd.to_numeric(
                    school.get(f"{year}.aid.median_debt.income.30001_75000"),
                    errors="coerce",
                ),
                "median_debt_high_income": pd.to_numeric(
                    school.get(f"{year}.aid.median_debt.income.greater_than_75000"),
                    errors="coerce",
                ),
                "earnings_6yr": pd.to_numeric(
                    school.get(f"{year}.earnings.6_yrs_after_entry.median"),
                    errors="coerce",
                ),
                "earnings_7yr": pd.to_numeric(
                    school.get(f"{year}.earnings.7_yrs_after_entry.median"),
                    errors="coerce",
                ),
                "earnings_8yr": pd.to_numeric(
                    school.get(f"{year}.earnings.8_yrs_after_entry.median"),
                    errors="coerce",
                ),
                "enrollment": pd.to_numeric(
                    school.get(f"{year}.student.size"), errors="coerce"
                ),
            }

            # Calculate ROI (simple version: 10-year earnings minus debt)
            if school_data["median_debt"] > 0 and school_data["earnings_6yr"] > 0:
                # Estimate 10-year earnings (using 6-year as base)
                estimated_10yr_earnings = school_data["earnings_6yr"] * 10
                school_data["roi"] = (
                    estimated_10yr_earnings - school_data["median_debt"]
                )
            else:
                school_data["roi"] = np.nan

            processed_data.append(school_data)

    return pd.DataFrame(processed_data)


def create_time_series_chart(data, metric, title, y_axis_title):
    """Create a time series chart for the selected metric.

    Args:
        data (pd.DataFrame): Processed data
        metric (str): Column name of the metric to visualize
        title (str): Chart title
        y_axis_title (str): Y-axis title

    Returns:
        alt.Chart: Altair chart object
    """
    # Group by year and ownership, calculate mean of the metric
    chart_data = data.groupby(["year", "ownership"])[metric].mean().reset_index()

    # Create the chart
    chart = (
        alt.Chart(chart_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y(f"{metric}:Q", title=y_axis_title),
            color=alt.Color("ownership:N", title="Institution Type"),
            tooltip=[
                "year",
                "ownership",
                alt.Tooltip(metric, title=y_axis_title, format="$,.0f"),
            ],
        )
        .properties(title=title, width=650, height=400)
    )

    return chart


# Display the selected tool
if selected_tool == "data_explorer":
    st.header("Data Explorer")
    st.markdown("""
    Filter and analyze college data by year, state, and institution type.
    """)

    # --- Filter Controls ---
    st.subheader("Data Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Year range selector
        available_years = list(range(2017, 2023))
        start_year = st.selectbox("Start Year", available_years, index=0)
        end_year = st.selectbox(
            "End Year", available_years, index=len(available_years) - 1
        )

        if end_year < start_year:
            st.error("End year must be greater than or equal to start year.")
            st.stop()

        selected_years = list(range(start_year, end_year + 1))

    with col2:
        # State filter
        states = [
            "",
            "AK",
            "AL",
            "AR",
            "AZ",
            "CA",
            "CO",
            "CT",
            "DC",
            "DE",
            "FL",
            "GA",
            "HI",
            "IA",
            "ID",
            "IL",
            "IN",
            "KS",
            "KY",
            "LA",
            "MA",
            "MD",
            "ME",
            "MI",
            "MN",
            "MO",
            "MS",
            "MT",
            "NC",
            "ND",
            "NE",
            "NH",
            "NJ",
            "NM",
            "NV",
            "NY",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VA",
            "VT",
            "WA",
            "WI",
            "WV",
            "WY",
        ]
        selected_state = st.selectbox("Filter by State (optional)", states)

    with col3:
        # Ownership filter
        ownership_options = {
            "": "All",
            "1": "Public",
            "2": "Private nonprofit",
            "3": "Private for-profit",
        }
        selected_ownership = st.selectbox(
            "Filter by Institution Type (optional)",
            options=list(ownership_options.keys()),
            format_func=lambda x: ownership_options[x],
        )

    # Load data button
    if st.button("Load Data"):
        with st.spinner("Fetching data from College Scorecard API..."):
            try:
                # Fetch data based on filters
                data_by_year = fetch_college_data_for_appendix(
                    selected_years,
                    state=selected_state if selected_state else None,
                    ownership=selected_ownership if selected_ownership else None,
                )

                # Process data for visualization
                df = process_data_for_visualization(data_by_year)

                if df.empty:
                    st.warning(
                        "No data found for the selected filters. Please try different criteria."
                    )
                    st.stop()

                # Store the processed data in session state for reuse
                st.session_state.college_data = df

                # Display summary statistics
                st.subheader("Summary Statistics")
                total_schools = df["id"].nunique()
                total_states = df["state"].nunique()

                stats_col1, stats_col2, stats_col3 = st.columns(3)
                with stats_col1:
                    st.metric("Total Institutions", f"{total_schools}")
                with stats_col2:
                    st.metric("States Represented", f"{total_states}")
                with stats_col3:
                    st.metric("Years of Data", f"{len(selected_years)}")

                # Display the data explorer
                st.subheader("Data Explorer")

                # Metric selector for charts
                metric_options = {
                    "tuition_in_state": "In-State Tuition",
                    "tuition_out_of_state": "Out-of-State Tuition",
                    "total_cost": "Total Cost of Attendance",
                    "median_debt": "Median Student Debt",
                    "earnings_6yr": "Earnings (6 years after entry)",
                    "roi": "Return on Investment (10-year estimate)",
                }

                selected_metrics = st.multiselect(
                    "Select metrics to visualize",
                    options=list(metric_options.keys()),
                    default=["tuition_in_state", "median_debt"],
                    format_func=lambda x: metric_options[x],
                )

                # Create and display charts for selected metrics
                for metric in selected_metrics:
                    chart = create_time_series_chart(
                        df,
                        metric,
                        f"{metric_options[metric]} Trends ({start_year}-{end_year})",
                        metric_options[metric],
                    )
                    st.altair_chart(chart, use_container_width=True)

                # Data table with sorting and filtering
                st.subheader("Detailed Data Table")

                # Year filter for table
                table_year = st.selectbox(
                    "Select Year for Detailed Data",
                    selected_years,
                    index=len(selected_years) - 1,
                )

                # Sort options
                sort_options = {
                    "name": "Institution Name",
                    "tuition_in_state": "In-State Tuition",
                    "tuition_out_of_state": "Out-of-State Tuition",
                    "median_debt": "Median Debt",
                    "earnings_6yr": "Earnings (6 years)",
                    "roi": "Return on Investment",
                }

                sort_by = st.selectbox(
                    "Sort by",
                    options=list(sort_options.keys()),
                    format_func=lambda x: sort_options[x],
                )

                sort_order = st.radio(
                    "Sort Order", ["Ascending", "Descending"], horizontal=True
                )

                # Filter data for the selected year
                year_data = df[df["year"] == table_year].copy()

                # Sort the data
                ascending = sort_order == "Ascending"
                year_data = year_data.sort_values(by=sort_by, ascending=ascending)

                # Select columns for display
                display_cols = [
                    "name",
                    "state",
                    "ownership",
                    "tuition_in_state",
                    "tuition_out_of_state",
                    "median_debt",
                    "earnings_6yr",
                    "roi",
                ]

                display_df = year_data[display_cols].copy()

                # Rename columns for display
                display_df.columns = [
                    "Institution",
                    "State",
                    "Type",
                    "In-State Tuition ($)",
                    "Out-of-State Tuition ($)",
                    "Median Debt ($)",
                    "Earnings - 6yr ($)",
                    "ROI - 10yr Estimate ($)",
                ]

                # Format currency columns
                currency_cols = [
                    "In-State Tuition ($)",
                    "Out-of-State Tuition ($)",
                    "Median Debt ($)",
                    "Earnings - 6yr ($)",
                    "ROI - 10yr Estimate ($)",
                ]

                for col in currency_cols:
                    display_df[col] = display_df[col].apply(
                        lambda x: f"${x:,.0f}" if pd.notnull(x) else "N/A"
                    )

                # Display the table
                st.dataframe(display_df, use_container_width=True)

                # Download link
                csv = year_data.to_csv(index=False)
                st.download_button(
                    label="Download Data as CSV",
                    data=csv,
                    file_name=f"college_data_{table_year}.csv",
                    mime="text/csv",
                )

            except Exception as e:
                st.error(f"Error fetching or processing data: {str(e)}")
    else:
        st.info(
            "Select your filters and click 'Load Data' to explore college affordability metrics."
        )

        # Check if we have data from a previous load
        if hasattr(st.session_state, "college_data"):
            st.success(
                "Using previously loaded data. Adjust filters and click 'Load Data' to refresh."
            )
            df = st.session_state.college_data

            # Display summary from previous data
            st.subheader("Summary Statistics (Previous Data)")
            total_schools = df["id"].nunique()
            total_states = df["state"].nunique()
            years_range = f"{df['year'].min()}-{df['year'].max()}"

            stats_col1, stats_col2, stats_col3 = st.columns(3)
            with stats_col1:
                st.metric("Total Institutions", f"{total_schools}")
            with stats_col2:
                st.metric("States Represented", f"{total_states}")
            with stats_col3:
                st.metric("Years of Data", years_range)

elif selected_tool == "tuition_trends":
    st.header("Tuition Trends Analysis")
    st.markdown("""
    Explore how college tuition has changed over time across different institution types and states.
    """)

    # Filter controls
    col1, col2, col3 = st.columns(3)

    with col1:
        # Year range selector
        available_years = list(range(2017, 2023))
        start_year = st.selectbox("Start Year", available_years, index=0)
        end_year = st.selectbox(
            "End Year", available_years, index=len(available_years) - 1
        )

        if end_year < start_year:
            st.error("End year must be greater than or equal to start year.")
            st.stop()

        selected_years = list(range(start_year, end_year + 1))

    with col2:
        # State filter
        states = [
            "",
            "AK",
            "AL",
            "AR",
            "AZ",
            "CA",
            "CO",
            "CT",
            "DC",
            "DE",
            "FL",
            "GA",
            "HI",
            "IA",
            "ID",
            "IL",
            "IN",
            "KS",
            "KY",
            "LA",
            "MA",
            "MD",
            "ME",
            "MI",
            "MN",
            "MO",
            "MS",
            "MT",
            "NC",
            "ND",
            "NE",
            "NH",
            "NJ",
            "NM",
            "NV",
            "NY",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VA",
            "VT",
            "WA",
            "WI",
            "WV",
            "WY",
        ]
        selected_state = st.selectbox("Filter by State (optional)", states)

    with col3:
        # Ownership filter
        ownership_options = {
            "": "All",
            "1": "Public",
            "2": "Private nonprofit",
            "3": "Private for-profit",
        }
        selected_ownership = st.selectbox(
            "Filter by Institution Type (optional)",
            options=list(ownership_options.keys()),
            format_func=lambda x: ownership_options[x],
        )

    st.info("This tool is coming soon! Check back for updates.")

elif selected_tool == "debt_analysis":
    st.header("Student Debt Analysis")
    st.markdown("""
    Explore student debt patterns across different demographics and institution types.
    """)

    st.info("This tool is coming soon! Check back for updates.")

elif selected_tool == "roi_calculator":
    st.header("ROI Calculator")
    st.markdown("""
    Calculate and compare return on investment for different institutions and majors.
    """)

    st.info("This tool is coming soon! Check back for updates.")

# Back to main app button
st.markdown(
    """
<div class="back-link">
    <a href="/" target="_self" class="nav-button">
        ← Return to Main Article
    </a>
</div>
""",
    unsafe_allow_html=True,
)
