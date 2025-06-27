import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
import sys

# Add the parent directory to sys.path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from collegescore import CollegeScorecardClient

# Set page config
st.set_page_config(
    page_title="Tuition Trends - College Data Appendix",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .back-link {
        margin-top: 2rem;
        display: block;
        text-align: center;
    }
    .nav-button {
        padding: 0.5rem 1rem;
        background-color: #7c3aed;
        color: white;
        border-radius: 0.25rem;
        text-decoration: none;
        font-weight: 500;
        margin-right: 0.5rem;
        display: inline-block;
    }
    .nav-button:hover {
        background-color: #6d28d9;
    }
    .insight-box {
        background-color: #f0f9ff;
        border-left: 4px solid #0ea5e9;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Tuition Trends Analysis</h1>', unsafe_allow_html=True)
st.markdown("Explore how college tuition has changed over time across different institution types and states.")

# Helper function to fetch tuition data for multiple years
def fetch_tuition_data(years, state=None, ownership=None, per_page=100):
    """Fetch tuition data for multiple years with optional filters.
    
    Args:
        years (list): List of years to fetch data for
        state (str, optional): State abbreviation to filter by
        ownership (int, optional): School ownership code (1=Public, 2=Private nonprofit, 3=Private for-profit)
        per_page (int, optional): Number of results per page
        
    Returns:
        pd.DataFrame: Processed tuition data
    """
    all_data = []
    
    for year in years:
        fields = [
            f"{year}.cost.tuition.in_state",
            f"{year}.cost.tuition.out_of_state",
            f"{year}.cost.attendance.academic_year",
            f"{year}.cost.avg_net_price.public",
            f"{year}.cost.avg_net_price.private",
            "school.name",
            "school.state",
            "school.ownership",
            "id"
        ]
        
        filters = {}
        if state:
            filters["school.state"] = state
        if ownership:
            filters["school.ownership"] = ownership
            
        client = CollegeScorecardClient(api_key=os.getenv("COLLEGE_SCORECARD_API_KEY"))
        try:
            response = client.get_institutions(fields=fields, filters=filters, per_page=per_page)
            
            for school in response.get("results", []):
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
                        "3": "Private for-profit"
                    }.get(str(school.get("school.ownership")), "Unknown"),
                    "tuition_in_state": pd.to_numeric(school.get(f"{year}.cost.tuition.in_state"), errors="coerce"),
                    "tuition_out_of_state": pd.to_numeric(school.get(f"{year}.cost.tuition.out_of_state"), errors="coerce"),
                    "total_cost": pd.to_numeric(school.get(f"{year}.cost.attendance.academic_year"), errors="coerce"),
                    "net_price_public": pd.to_numeric(school.get(f"{year}.cost.avg_net_price.public"), errors="coerce"),
                    "net_price_private": pd.to_numeric(school.get(f"{year}.cost.avg_net_price.private"), errors="coerce"),
                }
                
                all_data.append(school_data)
        except Exception as e:
            st.error(f"Error fetching data for year {year}: {str(e)}")
    
    return pd.DataFrame(all_data)

# Function to create tuition trend charts
def create_tuition_trend_chart(data, metric, title, y_axis_title):
    """Create a trend chart for the selected tuition metric.
    
    Args:
        data (pd.DataFrame): Processed data
        metric (str): Column name of the metric to visualize
        title (str): Chart title
        y_axis_title (str): Y-axis title
        
    Returns:
        alt.Chart: Altair chart object
    """
    # Group by year and ownership, calculate mean of the metric
    chart_data = data.groupby(['year', 'ownership'])[metric].mean().reset_index()
    
    # Create the chart
    chart = alt.Chart(chart_data).mark_line(point=True).encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y(f'{metric}:Q', title=y_axis_title, scale=alt.Scale(zero=False)),
        color=alt.Color('ownership:N', title='Institution Type'),
        tooltip=['year', 'ownership', alt.Tooltip(metric, title=y_axis_title, format='$,.0f')]
    ).properties(
        title=title,
        width=650,
        height=400
    )
    
    return chart

# Function to calculate tuition growth rates
def calculate_tuition_growth(data, metric):
    """Calculate year-over-year and total growth rates for tuition.
    
    Args:
        data (pd.DataFrame): Processed tuition data
        metric (str): Column name of the tuition metric
        
    Returns:
        tuple: (yearly_growth_df, total_growth_df)
    """
    # Calculate mean tuition by year and ownership
    yearly_mean = data.groupby(['year', 'ownership'])[metric].mean().reset_index()
    
    # Calculate year-over-year growth rates
    yearly_growth = []
    
    for ownership in yearly_mean['ownership'].unique():
        ownership_data = yearly_mean[yearly_mean['ownership'] == ownership].sort_values('year')
        
        for i in range(1, len(ownership_data)):
            prev_year = ownership_data.iloc[i-1]['year']
            curr_year = ownership_data.iloc[i]['year']
            prev_value = ownership_data.iloc[i-1][metric]
            curr_value = ownership_data.iloc[i][metric]
            
            if pd.notnull(prev_value) and pd.notnull(curr_value) and prev_value > 0:
                growth_rate = ((curr_value - prev_value) / prev_value) * 100
                
                yearly_growth.append({
                    'ownership': ownership,
                    'start_year': prev_year,
                    'end_year': curr_year,
                    'period': f"{prev_year}-{curr_year}",
                    'growth_rate': growth_rate
                })
    
    yearly_growth_df = pd.DataFrame(yearly_growth)
    
    # Calculate total growth rate from first to last year
    total_growth = []
    
    for ownership in yearly_mean['ownership'].unique():
        ownership_data = yearly_mean[yearly_mean['ownership'] == ownership].sort_values('year')
        
        if len(ownership_data) >= 2:
            first_year = ownership_data.iloc[0]['year']
            last_year = ownership_data.iloc[-1]['year']
            first_value = ownership_data.iloc[0][metric]
            last_value = ownership_data.iloc[-1][metric]
            
            if pd.notnull(first_value) and pd.notnull(last_value) and first_value > 0:
                total_growth_rate = ((last_value - first_value) / first_value) * 100
                annual_growth_rate = ((last_value / first_value) ** (1 / (last_year - first_year)) - 1) * 100
                
                total_growth.append({
                    'ownership': ownership,
                    'start_year': first_year,
                    'end_year': last_year,
                    'period': f"{first_year}-{last_year}",
                    'total_growth_rate': total_growth_rate,
                    'annual_growth_rate': annual_growth_rate
                })
    
    total_growth_df = pd.DataFrame(total_growth)
    
    return yearly_growth_df, total_growth_df

# Main content
st.subheader("Tuition Data Analysis")

# Filter controls
col1, col2, col3 = st.columns(3)

with col1:
    # Year range selector
    available_years = list(range(2017, 2023))
    start_year = st.selectbox("Start Year", available_years, index=0)
    end_year = st.selectbox("End Year", available_years, index=len(available_years)-1)
    
    if end_year < start_year:
        st.error("End year must be greater than or equal to start year.")
        st.stop()
        
    selected_years = list(range(start_year, end_year + 1))

with col2:
    # State filter
    states = [
        "", "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA", "ID", 
        "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", 
        "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", 
        "UT", "VA", "VT", "WA", "WI", "WV", "WY"
    ]
    selected_state = st.selectbox("Filter by State (optional)", states)
    
with col3:
    # Ownership filter
    ownership_options = {
        "": "All",
        "1": "Public",
        "2": "Private nonprofit",
        "3": "Private for-profit"
    }
    selected_ownership = st.selectbox(
        "Filter by Institution Type (optional)",
        options=list(ownership_options.keys()),
        format_func=lambda x: ownership_options[x]
    )

# Load data button
if st.button("Analyze Tuition Trends"):
    with st.spinner("Fetching tuition data from College Scorecard API..."):
        try:
            # Fetch data based on filters
            df = fetch_tuition_data(
                selected_years,
                state=selected_state if selected_state else None,
                ownership=selected_ownership if selected_ownership else None
            )
            
            if df.empty:
                st.warning("No data found for the selected filters. Please try different criteria.")
                st.stop()
            
            # Store the processed data in session state for reuse
            st.session_state.tuition_data = df
            
            # Display summary statistics
            st.subheader("Summary Statistics")
            total_schools = df['id'].nunique()
            total_states = df['state'].nunique()
            
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            with stats_col1:
                st.metric("Total Institutions", f"{total_schools}")
            with stats_col2:
                st.metric("States Represented", f"{total_states}")
            with stats_col3:
                st.metric("Years of Data", f"{len(selected_years)}")
            
            # Tuition trends visualization
            st.subheader("Tuition Trends Over Time")
            
            tab1, tab2, tab3 = st.tabs(["In-State Tuition", "Out-of-State Tuition", "Net Price"])
            
            with tab1:
                # In-state tuition trend
                in_state_chart = create_tuition_trend_chart(
                    df, 
                    "tuition_in_state", 
                    f"In-State Tuition Trends ({start_year}-{end_year})",
                    "In-State Tuition ($)"
                )
                st.altair_chart(in_state_chart, use_container_width=True)
                
                # Calculate growth rates
                yearly_growth, total_growth = calculate_tuition_growth(df, "tuition_in_state")
                
                if not total_growth.empty:
                    st.subheader("In-State Tuition Growth Analysis")
                    
                    # Display total growth rates
                    st.markdown("#### Total Growth Rate")
                    
                    growth_cols = st.columns(len(total_growth))
                    for i, (_, row) in enumerate(total_growth.iterrows()):
                        with growth_cols[i]:
                            st.metric(
                                f"{row['ownership']} Institutions",
                                f"{row['total_growth_rate']:.1f}%",
                                f"{row['annual_growth_rate']:.1f}% annually"
                            )
                    
                    # Display yearly growth rates
                    if not yearly_growth.empty:
                        st.markdown("#### Year-over-Year Growth Rates")
                        
                        # Create a chart for yearly growth rates
                        yearly_chart = alt.Chart(yearly_growth).mark_bar().encode(
                            x=alt.X('period:N', title='Period'),
                            y=alt.Y('growth_rate:Q', title='Growth Rate (%)'),
                            color=alt.Color('ownership:N', title='Institution Type'),
                            tooltip=['period', 'ownership', alt.Tooltip('growth_rate', format='.1f')]
                        ).properties(
                            title="Year-over-Year Tuition Growth Rates",
                            width=600,
                            height=300
                        )
                        
                        st.altair_chart(yearly_chart, use_container_width=True)
                
                # Insights
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("#### Key Insights: In-State Tuition")
                
                # Calculate average growth rates by ownership
                if not yearly_growth.empty:
                    avg_growth = yearly_growth.groupby('ownership')['growth_rate'].mean().reset_index()
                    max_growth = yearly_growth.loc[yearly_growth['growth_rate'].idxmax()]
                    
                    st.markdown(f"""
                    - Average annual growth rates: {', '.join([f"{row['ownership']}: {row['growth_rate']:.1f}%" for _, row in avg_growth.iterrows()])}
                    - Highest growth observed: {max_growth['growth_rate']:.1f}% for {max_growth['ownership']} institutions ({max_growth['period']})
                    - Private institutions generally show {'higher' if avg_growth[avg_growth['ownership'] == 'Private nonprofit']['growth_rate'].values[0] > avg_growth[avg_growth['ownership'] == 'Public']['growth_rate'].values[0] else 'lower'} growth rates than public institutions
                    """)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                # Out-of-state tuition trend
                out_state_chart = create_tuition_trend_chart(
                    df, 
                    "tuition_out_of_state", 
                    f"Out-of-State Tuition Trends ({start_year}-{end_year})",
                    "Out-of-State Tuition ($)"
                )
                st.altair_chart(out_state_chart, use_container_width=True)
                
                # Calculate growth rates
                yearly_growth, total_growth = calculate_tuition_growth(df, "tuition_out_of_state")
                
                if not total_growth.empty:
                    st.subheader("Out-of-State Tuition Growth Analysis")
                    
                    # Display total growth rates
                    st.markdown("#### Total Growth Rate")
                    
                    growth_cols = st.columns(len(total_growth))
                    for i, (_, row) in enumerate(total_growth.iterrows()):
                        with growth_cols[i]:
                            st.metric(
                                f"{row['ownership']} Institutions",
                                f"{row['total_growth_rate']:.1f}%",
                                f"{row['annual_growth_rate']:.1f}% annually"
                            )
                    
                    # Display yearly growth rates
                    if not yearly_growth.empty:
                        st.markdown("#### Year-over-Year Growth Rates")
                        
                        # Create a chart for yearly growth rates
                        yearly_chart = alt.Chart(yearly_growth).mark_bar().encode(
                            x=alt.X('period:N', title='Period'),
                            y=alt.Y('growth_rate:Q', title='Growth Rate (%)'),
                            color=alt.Color('ownership:N', title='Institution Type'),
                            tooltip=['period', 'ownership', alt.Tooltip('growth_rate', format='.1f')]
                        ).properties(
                            title="Year-over-Year Tuition Growth Rates",
                            width=600,
                            height=300
                        )
                        
                        st.altair_chart(yearly_chart, use_container_width=True)
                
                # Insights
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("#### Key Insights: Out-of-State Tuition")
                
                # Calculate average growth rates by ownership
                if not yearly_growth.empty:
                    avg_growth = yearly_growth.groupby('ownership')['growth_rate'].mean().reset_index()
                    max_growth = yearly_growth.loc[yearly_growth['growth_rate'].idxmax()]
                    
                    st.markdown(f"""
                    - Average annual growth rates: {', '.join([f"{row['ownership']}: {row['growth_rate']:.1f}%" for _, row in avg_growth.iterrows()])}
                    - Highest growth observed: {max_growth['growth_rate']:.1f}% for {max_growth['ownership']} institutions ({max_growth['period']})
                    - The gap between in-state and out-of-state tuition continues to widen for public institutions
                    """)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                # Net price comparison (public vs private)
                df_public = df[df['ownership'] == 'Public'].copy()
                df_private = df[df['ownership'] == 'Private nonprofit'].copy()
                
                # Create net price comparison chart
                if not df_public.empty and not df_private.empty:
                    # Prepare data for public institutions
                    public_data = df_public.groupby('year')['net_price_public'].mean().reset_index()
                    public_data['price_type'] = 'Public Net Price'
                    public_data = public_data.rename(columns={'net_price_public': 'price'})
                    
                    # Prepare data for private institutions
                    private_data = df_private.groupby('year')['net_price_private'].mean().reset_index()
                    private_data['price_type'] = 'Private Net Price'
                    private_data = private_data.rename(columns={'net_price_private': 'price'})
                    
                    # Combine data
                    combined_data = pd.concat([public_data, private_data])
                    
                    # Create chart
                    net_price_chart = alt.Chart(combined_data).mark_line(point=True).encode(
                        x=alt.X('year:O', title='Year'),
                        y=alt.Y('price:Q', title='Net Price ($)', scale=alt.Scale(zero=False)),
                        color=alt.Color('price_type:N', title='Institution Type'),
                        tooltip=['year', 'price_type', alt.Tooltip('price', title='Net Price', format='$,.0f')]
                    ).properties(
                        title=f"Net Price Comparison: Public vs Private ({start_year}-{end_year})",
                        width=650,
                        height=400
                    )
                    
                    st.altair_chart(net_price_chart, use_container_width=True)
                    
                    # Calculate net price gap
                    if not public_data.empty and not private_data.empty:
                        merged_data = public_data.merge(private_data, on='year', suffixes=('_public', '_private'))
                        merged_data['price_gap'] = merged_data['price_private'] - merged_data['price_public']
                        merged_data['gap_percentage'] = (merged_data['price_gap'] / merged_data['price_public']) * 100
                        
                        # Display gap analysis
                        st.subheader("Net Price Gap Analysis")
                        
                        # Calculate average gap
                        avg_gap = merged_data['price_gap'].mean()
                        avg_gap_pct = merged_data['gap_percentage'].mean()
                        
                        # Calculate gap trend
                        first_gap = merged_data.iloc[0]['price_gap']
                        last_gap = merged_data.iloc[-1]['price_gap']
                        gap_change = ((last_gap - first_gap) / first_gap) * 100 if first_gap > 0 else 0
                        
                        st.metric(
                            "Average Price Gap (Private vs Public)",
                            f"${avg_gap:,.0f}",
                            f"{avg_gap_pct:.1f}% premium"
                        )
                        
                        # Gap trend chart
                        gap_chart = alt.Chart(merged_data).mark_bar().encode(
                            x=alt.X('year:O', title='Year'),
                            y=alt.Y('price_gap:Q', title='Price Gap ($)'),
                            tooltip=['year', alt.Tooltip('price_gap', format='$,.0f'), alt.Tooltip('gap_percentage', format='.1f%')]
                        ).properties(
                            title="Net Price Gap Between Private and Public Institutions",
                            width=600,
                            height=300
                        )
                        
                        st.altair_chart(gap_chart, use_container_width=True)
                        
                        # Insights
                        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                        st.markdown("#### Key Insights: Net Price")
                        st.markdown(f"""
                        - The average net price gap between private and public institutions is **${avg_gap:,.0f}**
                        - Private institutions cost on average **{avg_gap_pct:.1f}%** more than public institutions after financial aid
                        - The price gap has {'increased' if gap_change > 0 else 'decreased'} by **{abs(gap_change):.1f}%** from {start_year} to {end_year}
                        - Despite higher sticker prices, the net price difference is smaller than the difference in published tuition rates
                        """)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            # Tuition vs. inflation comparison
            st.subheader("Tuition Growth vs. Inflation")
            
            # Inflation data (approximate CPI annual % change)
            inflation_data = pd.DataFrame({
                'year': list(range(2017, 2023)),
                'inflation_rate': [2.1, 2.4, 1.8, 1.2, 4.7, 8.0]  # Approximate inflation rates
            })
            
            # Calculate average tuition growth rates by year
            tuition_growth = []
            
            for ownership in df['ownership'].unique():
                ownership_data = df[df['ownership'] == ownership].copy()
                yearly_means = ownership_data.groupby('year')['tuition_in_state'].mean()
                
                for i in range(1, len(yearly_means)):
                    year = yearly_means.index[i]
                    prev_year = yearly_means.index[i-1]
                    curr_value = yearly_means.iloc[i]
                    prev_value = yearly_means.iloc[i-1]
                    
                    if pd.notnull(curr_value) and pd.notnull(prev_value) and prev_value > 0:
                        growth_rate = ((curr_value - prev_value) / prev_value) * 100
                        
                        tuition_growth.append({
                            'year': year,
                            'ownership': ownership,
                            'growth_rate': growth_rate
                        })
            
            tuition_growth_df = pd.DataFrame(tuition_growth)
            
            if not tuition_growth_df.empty:
                # Calculate average growth rate by year across all ownership types
                avg_growth_by_year = tuition_growth_df.groupby('year')['growth_rate'].mean().reset_index()
                avg_growth_by_year = avg_growth_by_year.rename(columns={'growth_rate': 'tuition_growth_rate'})
                
                # Merge with inflation data
                comparison_data = avg_growth_by_year.merge(inflation_data, on='year')
                comparison_data = comparison_data.melt(
                    id_vars=['year'],
                    value_vars=['tuition_growth_rate', 'inflation_rate'],
                    var_name='rate_type',
                    value_name='percentage'
                )
                
                # Create comparison chart
                comparison_chart = alt.Chart(comparison_data).mark_line(point=True).encode(
                    x=alt.X('year:O', title='Year'),
                    y=alt.Y('percentage:Q', title='Rate (%)'),
                    color=alt.Color('rate_type:N', title='Rate Type', scale=alt.Scale(
                        domain=['tuition_growth_rate', 'inflation_rate'],
                        range=['#1f77b4', '#ff7f0e']
                    )),
                    tooltip=['year', alt.Tooltip('percentage', format='.1f%')]
                ).transform_calculate(
                    rate_type="datum.rate_type == 'tuition_growth_rate' ? 'Tuition Growth Rate' : 'Inflation Rate'"
                ).encode(
                    color=alt.Color('rate_type:N', title='Rate Type')
                ).properties(
                    title="Tuition Growth vs. Inflation",
                    width=650,
                    height=400
                )
                
                st.altair_chart(comparison_chart, use_container_width=True)
                
                # Calculate average difference
                avg_diff = (comparison_data[comparison_data['rate_type'] == 'tuition_growth_rate']['percentage'].mean() - 
                           comparison_data[comparison_data['rate_type'] == 'inflation_rate']['percentage'].mean())
                
                st.metric(
                    "Average Annual Difference (Tuition Growth vs. Inflation)",
                    f"{avg_diff:.1f}%",
                    "Higher than inflation" if avg_diff > 0 else "Lower than inflation"
                )
                
                # Insights
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("#### Key Insights: Tuition vs. Inflation")
                st.markdown(f"""
                - Tuition growth has been **{avg_diff:.1f}%** {'higher' if avg_diff > 0 else 'lower'} than inflation on average
                - {'Most' if (comparison_data[comparison_data['rate_type'] == 'tuition_growth_rate']['percentage'] > comparison_data[comparison_data['rate_type'] == 'inflation_rate']['percentage']).mean() > 0.5 else 'Some'} years show tuition growth outpacing inflation
                - This trend suggests that college affordability continues to be a challenge as costs rise faster than general prices
                """)
                st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error analyzing tuition trends: {str(e)}")
else:
    st.info("Select your filters and click 'Analyze Tuition Trends' to explore how college costs have changed over time.")
    
    # Check if we have data from a previous analysis
    if hasattr(st.session_state, 'tuition_data'):
        st.success("Using previously loaded data. Adjust filters and click 'Analyze Tuition Trends' to refresh.")
        
        # Display a sample chart from previous data
        df = st.session_state.tuition_data
        years_range = f"{df['year'].min()}-{df['year'].max()}"
        
        st.subheader(f"Sample Chart (Previous Analysis: {years_range})")
        
        sample_chart = create_tuition_trend_chart(
            df, 
            "tuition_in_state", 
            f"In-State Tuition Trends ({df['year'].min()}-{df['year'].max()})",
            "In-State Tuition ($)"
        )
        st.altair_chart(sample_chart, use_container_width=True)

# Navigation
st.markdown("""
<div class="back-link">
    <a href="/" target="_self" class="nav-button">
        ← Return to Main Application
    </a>
</div>
""", unsafe_allow_html=True) 