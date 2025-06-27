import pandas as pd
import altair as alt
import streamlit as st


def cost_1(figure_counter: int):
    # Load the prepared data
    historical_tuition = pd.read_csv('./termproject/data/historical_tuition.csv')
    cost_comparison = pd.read_csv('./termproject/data/cost_comparison.csv')
    cost_breakdown = pd.read_csv('./termproject/data/cost_breakdown.csv')

    # Historical trends chart
    st.altair_chart(
        alt.Chart(historical_tuition)
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X('year:O', title='Year'),
            y=alt.Y('Tuition:Q', title='Tuition ($)', scale=alt.Scale(zero=False)),
            color=alt.Color('Institution Type:N', scale=alt.Scale(scheme='category10')),
            tooltip=['year', 'Institution Type', 'Tuition']
        )
        .properties(
            title='College Tuition Growth: 2017-2021',
            width=600,
            height=400
        ),
        use_container_width=True
    )
    st.caption(
        f"Figure {figure_counter}: College tuition trends from 2017 to 2021, showing the differences "
        "between public in-state, public out-of-state, and private institutions."
    )

    
    # Narrative section about tuition growth trends
    st.markdown("##### 📈 The Rising Cost of Higher Education")
    
    # Calculate growth rates for narrative
    public_in_state_growth = (
        (historical_tuition[
            (historical_tuition['Institution Type'] == 'Public In-State') & 
            (historical_tuition['year'] == 2021)
        ]['Tuition'].iloc[0] - 
         historical_tuition[
             (historical_tuition['Institution Type'] == 'Public In-State') & 
             (historical_tuition['year'] == 2017)
         ]['Tuition'].iloc[0]) / 
        historical_tuition[
            (historical_tuition['Institution Type'] == 'Public In-State') & 
            (historical_tuition['year'] == 2017)
        ]['Tuition'].iloc[0] * 100
    )
    
    private_nonprofit_growth = (
        (historical_tuition[
            (historical_tuition['Institution Type'] == 'Private Nonprofit') & 
            (historical_tuition['year'] == 2021)
        ]['Tuition'].iloc[0] - 
         historical_tuition[
             (historical_tuition['Institution Type'] == 'Private Nonprofit') & 
             (historical_tuition['year'] == 2017)
         ]['Tuition'].iloc[0]) / 
        historical_tuition[
            (historical_tuition['Institution Type'] == 'Private Nonprofit') & 
            (historical_tuition['year'] == 2017)
        ]['Tuition'].iloc[0] * 100
    )
    
    # Get current tuition levels for narrative
    current_public_in = historical_tuition[
        (historical_tuition['Institution Type'] == 'Public In-State') & 
        (historical_tuition['year'] == 2021)
    ]['Tuition'].iloc[0]
    
    current_private_nonprofit = historical_tuition[
        (historical_tuition['Institution Type'] == 'Private Nonprofit') & 
        (historical_tuition['year'] == 2021)
    ]['Tuition'].iloc[0]
    
    st.markdown(f"""
    The data reveals a concerning trend in higher education costs from 2017 to 2021. 
    **Private nonprofit institutions** have experienced the most dramatic growth, with tuition 
    increasing by **{private_nonprofit_growth:.1f}%** over this period. This rapid escalation 
    has pushed the average private nonprofit tuition to **${current_private_nonprofit:,.0f}** 
    annually, creating a significant affordability barrier for many families.
    
    In contrast, **public in-state institutions** have seen more moderate growth at 
    **{public_in_state_growth:.1f}%**, maintaining their position as the most accessible 
    option at **${current_public_in:,.0f}** per year. However, even this "moderate" growth 
    represents a substantial financial burden for students and families.
    
    The widening gap between public and private tuition costs raises important questions 
    about educational equity and access. As private nonprofit institutions continue to 
    outpace inflation and wage growth, they risk becoming accessible only to the most 
    affluent families, potentially limiting social mobility and educational opportunity.
    """)
    
    # Add a key insight box
    st.info("""
    💡 **Key Insight**: Private nonprofit institutions are growing tuition costs at a rate 
    that significantly outpaces both public institutions and general economic indicators, 
    creating an increasingly stratified higher education landscape.
    """)

    figure_counter += 1

    # Sticker vs Net Price comparison over time
    price_comparison = pd.melt(
        cost_comparison,
        id_vars=['year', 'Institution Type'],
        value_vars=['Sticker Price', 'Net Price'],
        var_name='Price Type',
        value_name='Amount'
    )

    # Create a faceted chart for each institution type
    price_chart = alt.Chart(price_comparison).mark_line(point=True).encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y('Amount:Q', title='Amount ($)', scale=alt.Scale(zero=False)),
        color=alt.Color('Price Type:N', scale=alt.Scale(domain=['Sticker Price', 'Net Price'], range=['#d62728', '#2ca02c'])),
        tooltip=['year', 'Institution Type', 'Price Type', 'Amount']
    ).properties(
        width=200,
        height=200
    ).facet(
        facet='Institution Type:N',
        columns=3,
        title='Sticker Price vs. Net Price Trends by Institution Type (2017-2021)'
    )

    st.altair_chart(price_chart, use_container_width=True)
    st.caption(
        f"Figure {figure_counter}: Trends in sticker price and net price over time for each institution type, "
        "showing how the gap between listed and actual costs has evolved."
    )
    figure_counter += 1

    
    # Calculate key statistics for the narrative
    latest_year = cost_comparison['year'].max()
    latest_data = cost_comparison[cost_comparison['year'] == latest_year]
    
    # Calculate average sticker vs net price differences
    avg_sticker_net_diff = latest_data['Average Aid'].mean()
    avg_sticker_price = latest_data['Sticker Price'].mean()
    avg_net_price = latest_data['Net Price'].mean()
    
    # Calculate percentage difference
    avg_percentage_diff = (avg_sticker_net_diff / avg_sticker_price) * 100
    
    # Find institution with largest gap
    largest_gap_institution = latest_data.loc[latest_data['Average Aid'].idxmax()]
    largest_gap_amount = largest_gap_institution['Average Aid']
    largest_gap_percentage = (largest_gap_amount / largest_gap_institution['Sticker Price']) * 100
    
    # Calculate trends in the gap over time
    gap_trends = cost_comparison.groupby('year')['Average Aid'].mean()
    gap_growth = ((gap_trends.iloc[-1] - gap_trends.iloc[0]) / gap_trends.iloc[0]) * 100
    
    st.markdown(f"""
    ##### The Hidden Reality: Sticker Price vs. Actual Cost
    
    The data reveals a **staggering disconnect** between what colleges advertise and what students actually pay. 
    On average, students receive **${avg_sticker_net_diff:,.0f}** in financial aid, reducing their actual 
    costs by **{avg_percentage_diff:.1f}%** from the sticker price.
    
    The gap between sticker and net price has grown by **{gap_growth:.1f}%** over the study period, 
    indicating that while colleges continue to raise their published prices, they're also increasing 
    their financial aid packages to maintain enrollment. This creates a **"high-price, high-discount"** 
    model where the sticker price serves more as a marketing tool than an actual cost indicator.
    
    **{largest_gap_institution['Institution Type']}** institutions show the largest average aid gap at 
    **${largest_gap_amount:,.0f}** per year, representing a **{largest_gap_percentage:.1f}%** reduction 
    from their published costs. This suggests that private institutions, despite their high sticker prices, 
    may actually be more accessible than their published costs suggest through generous financial aid programs.
    
    This pricing strategy has significant implications for students and families:
    - **Psychological Impact**: High sticker prices may discourage applications from qualified students
    - **Planning Challenges**: Families struggle to estimate actual costs without detailed financial aid calculations
    - **Transparency Issues**: The true cost of education is obscured by complex pricing structures
    """)
    
    # Add a key insight box
    st.warning("""
    ⚠️ **Critical Finding**: The average student pays **significantly less** than the published sticker price, 
    with financial aid reducing costs by over **{avg_percentage_diff:.0f}%**. This "high-price, high-discount" 
    model creates confusion and may prevent qualified students from applying to institutions they can actually afford.
    """.format(avg_percentage_diff=avg_percentage_diff))

    # Cost breakdown visualization over time
    cost_components = pd.DataFrame({
        'Cost Component': [
            'Tuition',
            'Room & Board',
            'Books & Supplies',
            'Other Expenses'
        ],
        'Column Name': [
            'cost.tuition.in_state',
            'cost.roomboard.oncampus',
            'cost.booksupply',
            'cost.otherexpense.oncampus'
        ]
    })

    # Reshape cost breakdown data
    cost_breakdown_melted = pd.melt(
        cost_breakdown,
        id_vars=['year', 'Institution Type'],
        value_vars=cost_components['Column Name'],
        var_name='Cost Component',
        value_name='Cost ($)'
    )

    # Map column names to friendly names
    component_map = dict(zip(cost_components['Column Name'], cost_components['Cost Component']))
    cost_breakdown_melted['Cost Component'] = cost_breakdown_melted['Cost Component'].map(component_map)

    # Create a faceted chart for cost breakdown trends
    cost_chart = alt.Chart(cost_breakdown_melted).mark_area().encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y('Cost ($):Q', stack='zero'),
        color=alt.Color('Cost Component:N', scale=alt.Scale(scheme='category20')),
        tooltip=['year', 'Institution Type', 'Cost Component', 'Cost ($)']
    ).properties(
        width=200,
        height=200
    ).facet(
        facet='Institution Type:N',
        columns=3,
        title='Cost Components Over Time by Institution Type (2017-2021)'
    )

    st.altair_chart(cost_chart, use_container_width=True)
    st.caption(
        f"Figure {figure_counter}: Evolution of different cost components over time for each institution type, "
        "showing how the composition of college costs has changed."
    )
    figure_counter += 1

    
    # Narrative about cost component growth patterns
    st.subheader("Cost Component Growth Patterns")

    # Calculate growth rates for each cost component
    growth_analysis = cost_breakdown_melted.groupby(['Institution Type', 'Cost Component']).agg({
        'Cost ($)': ['first', 'last']
    }).reset_index()
    growth_analysis.columns = ['Institution Type', 'Cost Component', 'Start_Value', 'End_Value']
    growth_analysis['Growth_Rate'] = ((growth_analysis['End_Value'] - growth_analysis['Start_Value']) / growth_analysis['Start_Value'] * 100)
    
    # Find the highest and lowest growth components
    max_growth = growth_analysis.loc[growth_analysis['Growth_Rate'].idxmax()]
    min_growth = growth_analysis.loc[growth_analysis['Growth_Rate'].idxmin()]
    
    # Create a summary table
    growth_summary = growth_analysis.pivot(index='Cost Component', columns='Institution Type', values='Growth_Rate').round(1)
    
    st.write("""
    **Cost Component Growth Analysis (2017-2021)**
    
    While all cost components have increased over the five-year period, their relative order of magnitude 
    has remained remarkably consistent. Tuition continues to be the largest component, followed by 
    Room & Board, with Books & Supplies and Other Expenses maintaining their positions as smaller 
    but still significant cost factors.
    
    This stability in cost structure suggests that the fundamental economics of higher education 
    haven't shifted dramatically, even as overall costs continue to rise.
    """)
    
    # Display growth summary table
    st.dataframe(growth_summary, use_container_width=True)
    

    # Calculate key metrics for the statistics display
    latest_year = historical_tuition['year'].max()
    earliest_year = historical_tuition['year'].min()
    
    # Calculate total percentage increase over the period
    start_tuition = historical_tuition[historical_tuition['year'] == earliest_year].groupby('Institution Type')['Tuition'].mean()
    end_tuition = historical_tuition[historical_tuition['year'] == latest_year].groupby('Institution Type')['Tuition'].mean()
    total_increase = ((end_tuition - start_tuition) / start_tuition * 100).mean()

    # Calculate the latest public-private gap
    latest_gap = (
        end_tuition['Private Nonprofit'] - end_tuition['Public In-State']
    ) / 1000  # Convert to thousands

    # Calculate average aid coverage across all years
    aid_coverage = (
        (cost_comparison['Sticker Price'] - cost_comparison['Net Price'])
        / cost_comparison['Sticker Price']
    ).mean() * 100

    # Key statistics display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "5-Year Total Increase",
            f"{total_increase:.1f}%",
            "2017-2021 change",
            delta_color="inverse"
        )
    with col2:
        st.metric(
            "Current Public-Private Gap",
            f"${latest_gap:.0f}K",
            "2021 difference",
            delta_color="inverse"
        )
    with col3:
        st.metric(
            "Average Aid Coverage",
            f"{aid_coverage:.1f}%",
            "Across all years",
            delta_color="normal"
        )

    st.info(
        "💡 **Key Insight**: The data from 2017 to 2021 shows persistent gaps between sticker and net prices, "
        "with private institutions maintaining significantly higher costs than public ones. "
        "Financial aid continues to play a crucial role in making college more affordable, "
        "though the effectiveness varies by institution type."
    )
