import os
import streamlit as st
import streamlit_shadcn_ui as ui
import altair as alt
import pandas as pd
import numpy as np

# write a client class for the college scorecard dataset
import requests


class CollegeScorecardClient:
    def __init__(self, api_key=None):
        self.base_url = "https://api.data.gov/ed/collegescorecard/v1/"
        self.api_key = api_key or "your_api_key_here"

    def get_data(self, endpoint, params=None):
        """
        Get data from the College Scorecard API

        Args:
            endpoint (str): API endpoint to query
            params (dict): Query parameters

        Returns:
            dict: JSON response from the API
        """
        if params is None:
            params = {}

        params["api_key"] = self.api_key

        response = requests.get(self.base_url + endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_institutions(self, fields=None, filters=None, page=0, per_page=100):
        """
        Get institution-level data

        Args:
            fields (list): Fields to return
            filters (dict): Filters to apply
            page (int): Page number
            per_page (int): Results per page

        Returns:
            dict: Institution data
        """
        params = {"page": page, "per_page": per_page}

        if fields:
            params["fields"] = ",".join(fields)

        if filters:
            for key, value in filters.items():
                params[key] = value

        return self.get_data("schools", params)


client = CollegeScorecardClient(api_key=os.getenv("COLLEGE_SCORECARD_API_KEY"))

st.set_page_config(
    page_title="The College Affordability Crisis",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# NYT-style centered container with floating TOC
st.markdown(
    """
    <style>
    root {
        font-family: Georgia, 'Times New Roman', Times, serif;
    }
    .nyt-center {
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 24px;
        padding-right: 24px;
        text-align: left;
        word-wrap: break-word;
    }
    .nyt-section {
        margin-top: 2.5em;
        margin-bottom: 2.5em;
    }
    .nyt-badge-row {
        display: flex;
        justify-content: center;
        gap: 0.5em;
        margin-top: 2em;
        margin-bottom: 2em;
    }
    .nyt-blockquote {
        font-style: italic;
        color: #636363;
        margin: 1.5em 0;
        padding: 0.5em 1em;
        border-left: 4px solid #7c3aed;
        background: #f8fafc;
    }
    .nyt-bullets {
        text-align: left;
        margin: 1em auto 1em auto;
        max-width: 600px;
        font-size: 1.05em;
    }
    
    /* Floating TOC Styles */
    .floating-toc {
        position: fixed;
        top: 50%;
        left: 20px;
        transform: translateY(-50%);
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 200px;
        z-index: 1000;
        backdrop-filter: blur(8px);
    }
    
    .toc-title {
        font-size: 0.9em;
        font-weight: 600;
        margin-bottom: 12px;
        color: #374151;
        text-align: center;
    }
    
    .toc-item {
        display: block;
        padding: 6px 8px;
        margin: 2px 0;
        font-size: 0.75em;
        color: #6b7280;
        text-decoration: none;
        border-radius: 4px;
        transition: all 0.2s ease;
        cursor: pointer;
        line-height: 1.3;
    }
    
    .toc-item:hover {
        background: #f3f4f6;
        color: #374151;
    }
    
    .toc-item.active {
        background: #7c3aed;
        color: white;
        font-weight: 500;
    }

    /* TOC Anchor Styles */
    .toc-anchor {
        color: unset;
        text-decoration: unset;
    }
    
    @media (max-width: 1200px) {
        .floating-toc {
            display: none;
        }
    }
    </style>
    
    <!-- Floating TOC -->
    <div class="floating-toc" id="floating-toc">
        <div class="toc-title">Contents</div>
        <a href="#intro" class="toc-item toc-anchor">Introduction</a>
        <a href="#section1" class="toc-item toc-anchor">1. Sticker Shock</a>
        <a href="#section2" class="toc-item toc-anchor">2. Enrollment Patterns</a>
        <a href="#section3" class="toc-item toc-anchor">3. The Debt Question</a>
        <a href="#section4" class="toc-item toc-anchor">4. Alternatives Rising</a>
        <a href="#section5" class="toc-item toc-anchor">5. ROI in 2025</a>
        <a href="#section6" class="toc-item toc-anchor">6. Equity & Access</a>
        <a href="#section7" class="toc-item toc-anchor">7. Cultural Shift</a>
        <a href="#section8" class="toc-item toc-anchor">8. Policy & Future</a>
        <a href="#section9" class="toc-item toc-anchor">9. Data Deep-Dive</a>
    </div>
    
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown(
        """
        <div class="nyt-center nyt-section" id="intro">
            <h1 style="font-size:2.2em; font-weight:700; margin-bottom:0.2em; font-style: italic;">
                The College Affordability Crisis: Is Higher Education Still Worth It?
            </h1>
            <p style="color: #475569; font-size: 1.1em; margin-bottom: 2em;">
                By <a href="https://www.linkedin.com/in/humphrey-ahn/" style="text-decoration: underline; color: unset;">Sangtae Ahn</a> &mdash; <a href="https://github.com/ahnsv" style="text-decoration: underline; color: unset;">GitHub</a> &mdash; June 13, 2025
            </p>
            <p style="font-size:1.2em; line-height:1.7; margin-bottom:1.5em;">
                <strong>College was once the surest path to the American Dream.</strong> But today, the price tag of a degree has soared, student debt has become a defining feature of young adulthood, and families across the country are asking: <em>Is it still worth it?</em>
            </p>
            <p style="font-size:1.1em; line-height:1.7;">
                This interactive story unpacks the real cost of college in 2025. We'll explore who's paying the most, who's being left behind, and whether the promise of higher education still holds up in a changing world. <br>
                <span style="color:#7c3aed; font-weight:500;">Scroll down to discover the numbers, the stories, and the future of college in America.</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 1. The Sticker Shock: How Much Does College Really Cost?
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section1">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">1. The Sticker Shock: How Much Does College Really Cost?</h2>
        <div class="nyt-blockquote">
            "The published price of college is only the beginning. For many families, the real cost is a complex puzzle of aid, scholarships, and hidden fees."
        </div>
        <p style="font-size:1.1em;">College costs have risen dramatically over the past few decades, outpacing inflation and wage growth. The sticker price—what colleges advertise—can be shocking, but the net price after aid is often a different story. Still, for many, the numbers are daunting.</p>
        <ul class="nyt-bullets">
            <li>Trends in tuition, fees, and total cost of attendance (public vs. private, in-state vs. out-of-state)</li>
            <li>Net price vs. sticker price</li>
            <li>Historical comparison (inflation-adjusted growth)</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- College Scorecard API Data Fetching and Caching ---
@st.cache_data(show_spinner=True)
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
        filters["school.ownership"] = (
            control  # 1=Public, 2=Private nonprofit, 3=Private for-profit
        )
    if state:
        filters["school.state"] = state
    data = client.get_institutions(fields=fields, filters=filters, per_page=per_page)
    return data["results"]


# --- UI Controls ---

# Year selection (2017-2023)
years = [f"{y}" for y in range(2017, 2023)]
year = st.selectbox("Select Year", years, index=len(years) - 1)

# Control type selection
control_map = {
    "All": None,
    "Public": "1",
    "Private Nonprofit": "2",
    "Private For-Profit": "3",
}
control = st.selectbox("Institution Type", list(control_map.keys()))

# State selection (top 10 populous states for demo)
states = [
    "All",
    "CA",
    "TX",
    "FL",
    "NY",
    "PA",
    "IL",
    "OH",
    "GA",
    "NC",
    "MI",
    "MA",
]
state = st.selectbox("State", states)

# Fetch data
data = fetch_college_data(
    year, control=control_map[control], state=None if state == "All" else state
)
df = pd.DataFrame(data)

# --- Section 1 Visualizations ---
if not df.empty:
    # Tuition and cost columns
    tuition_cols = [
        f"{year}.cost.tuition.in_state",
        f"{year}.cost.tuition.out_of_state",
        f"{year}.cost.attendance.academic_year",
        f"{year}.cost.avg_net_price.public",
        f"{year}.cost.avg_net_price.private",
    ]
    # Prepare data for bar chart
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
    # Melt for Altair
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
    # Remove NaN/zero
    cost_melted = cost_melted[cost_melted["Cost"] > 0]
    # Bar chart: Average cost by type
    avg_cost = cost_melted.groupby(["Type", "Cost Type"])["Cost"].mean().reset_index()
    chart = (
        alt.Chart(avg_cost)
        .mark_bar()
        .encode(
            x=alt.X("Type:N", title="Institution Type"),
            y=alt.Y("Cost:Q", title="Average Cost ($)"),
            color="Cost Type:N",
            tooltip=["Type", "Cost Type", alt.Tooltip("Cost", format=",.0f")],
        )
        .properties(
            title=f"Average College Costs by Type ({year})", width=600, height=400
        )
    )
    st.altair_chart(chart, use_container_width=True)
    # Table of top 10 most expensive institutions
    st.subheader("Top 10 Most Expensive Institutions (Total Cost)")
    st.dataframe(
        cost_data.sort_values("Total Cost", ascending=False).head(10)[
            ["Institution", "State", "Type", "Total Cost"]
        ]
    )
else:
    st.info("No data available for the selected filters.")

# 2. Enrollment Patterns: Who's Going to College?
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section2">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">2. Enrollment Patterns: Who's Going to College?</h2>
        <div class="nyt-blockquote">
            "The cost of college is only the beginning. For many families, the real cost is a complex puzzle of aid, scholarships, and hidden fees."
        </div>
        <p style="font-size:1.1em;">
            The cost of college is only the beginning. For many families, the real cost is a complex puzzle of aid, scholarships, and hidden fees.
        </p>
        <ul class="nyt-bullets">
            <li>Trends in enrollment by institution type</li>
            <li>Demographic breakdown of enrollment</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Section 2: Enrollment Patterns ---
if not df.empty:
    # Enrollment and demographics
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
    # Remove NaN/zero
    enroll_data = enroll_data[enroll_data["Enrollment"] > 0]
    # Enrollment by type
    enroll_by_type = enroll_data.groupby("Type")["Enrollment"].sum().reset_index()
    chart2 = (
        alt.Chart(enroll_by_type)
        .mark_bar()
        .encode(
            x=alt.X("Type:N", title="Institution Type"),
            y=alt.Y("Enrollment:Q", title="Total Enrollment"),
            color="Type:N",
            tooltip=["Type", alt.Tooltip("Enrollment", format=",")],
        )
        .properties(
            title=f"Total Enrollment by Institution Type ({year})",
            width=500,
            height=350,
        )
    )
    st.altair_chart(chart2, use_container_width=True)
    # Demographic breakdown (stacked bar)
    demo_cols = ["White", "Black", "Hispanic", "Asian", "First Gen"]
    demo_melted = enroll_data.melt(
        id_vars=["Institution", "Type"],
        value_vars=demo_cols,
        var_name="Demographic",
        value_name="Count",
    )
    demo_melted = demo_melted[demo_melted["Count"] > 0]
    demo_chart = (
        alt.Chart(demo_melted)
        .mark_bar()
        .encode(
            x=alt.X("Type:N", title="Institution Type"),
            y=alt.Y("Count:Q", stack="normalize", title="Proportion"),
            color="Demographic:N",
            tooltip=["Type", "Demographic", alt.Tooltip("Count", format=",")],
        )
        .properties(
            title=f"Demographic Breakdown by Institution Type ({year})",
            width=500,
            height=350,
        )
    )
    st.altair_chart(demo_chart, use_container_width=True)
else:
    st.info("No enrollment data available for the selected filters.")

# 3. The Debt Question: How Loans Shape Life After Graduation
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section3">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">3. The Debt Question: How Loans Shape Life After Graduation</h2>
        <div class="nyt-blockquote">
            "Student debt has become a defining feature of American adulthood, shaping life choices long after graduation."
        </div>
        <p style="font-size:1.1em;">The average student now graduates with tens of thousands in debt. For some, repayment is manageable; for others, it's a lifelong burden. Default rates remain stubbornly high, especially among those who don't complete their degrees.</p>
        <ul class="nyt-bullets">
            <li>Average student debt levels</li>
            <li>Default rates and repayment struggles</li>
            <li>Stories/case studies of recent grads</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# 4. Alternatives on the Rise: What People Are Choosing Instead
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section4">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">4. Alternatives on the Rise: What People Are Choosing Instead</h2>
        <div class="nyt-blockquote">
            "College is no longer the only path to success. More Americans are exploring alternatives that promise quicker, cheaper routes to good jobs."
        </div>
        <p style="font-size:1.1em;">Vocational programs, apprenticeships, and certifications are on the rise. Community colleges offer affordable options, while some students opt for gap years or direct entry into the workforce.</p>
        <ul class="nyt-bullets">
            <li>Growth in vocational training, apprenticeships, certifications</li>
            <li>Gap years, military, direct-to-workforce</li>
            <li>Community college trends</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# 5. Is It Still Worth It? Returns on Investment in 2025
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section5">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">5. Is It Still Worth It? Returns on Investment in 2025</h2>
        <div class="nyt-blockquote">
            "The value of a college degree is under scrutiny. For some, the payoff is clear; for others, the math no longer adds up."
        </div>
        <p style="font-size:1.1em;">While college graduates still earn more on average, the return on investment varies widely by major, institution, and individual circumstances. For some, debt outweighs the benefits.</p>
        <ul class="nyt-bullets">
            <li>Wage premiums for college grads vs. non-grads</li>
            <li>Degree "ROI" by major/field</li>
            <li>Lifetime earnings vs. debt</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# 6. Equity and Access: Who Gets Left Behind?
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section6">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">6. Equity and Access: Who Gets Left Behind?</h2>
        <div class="nyt-blockquote">
            "Access to higher education remains deeply unequal, with persistent gaps by race, income, and family background."
        </div>
        <p style="font-size:1.1em;">Despite efforts to expand access, many students face significant barriers to entry and completion. Financial aid helps, but gaps remain—especially for first-generation and low-income students.</p>
        <ul class="nyt-bullets">
            <li>First-generation students, minorities, low-income families</li>
            <li>The impact of aid and scholarship programs</li>
            <li>Barriers to entry and completion</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# 7. The Cultural Shift: What Does Society Value Now?
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section7">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">7. The Cultural Shift: What Does Society Value Now?</h2>
        <div class="nyt-blockquote">
            "The meaning of success is changing. For some, college is no longer the default path to a good life."
        </div>
        <p style="font-size:1.1em;">Societal attitudes toward college are shifting. High-profile entrepreneurs and changing job markets are challenging the traditional narrative of college as the only route to success.</p>
        <ul class="nyt-bullets">
            <li>Changing perceptions of the "American Dream"</li>
            <li>Parental and societal expectations</li>
            <li>Impact of high-profile dropouts/entrepreneurs</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# 8. Policy and the Future: Can Anything Change?
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section8">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">8. Policy and the Future: Can Anything Change?</h2>
        <div class="nyt-blockquote">
            "Policymakers and universities are experimenting with new models, but the future of college affordability remains uncertain."
        </div>
        <p style="font-size:1.1em;">From loan forgiveness to free college proposals, the policy landscape is evolving. Universities are also adapting, with new pricing models and online degrees.</p>
        <ul class="nyt-bullets">
            <li>State and federal policy proposals (loan forgiveness, free college, etc.)</li>
            <li>University responses (discounting, new models, online degrees)</li>
            <li>International comparisons</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# 9. Data Deep-Dive: Visualizing the College Affordability Crisis
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section9">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">9. Data Deep-Dive: Visualizing the College Affordability Crisis</h2>
        <div class="nyt-blockquote">
            "The data tells a complex story. In this section, we'll use interactive charts to explore the numbers behind the crisis."
        </div>
        <p style="font-size:1.1em;">Tuition and enrollment trends, debt by state and major, and the rise of alternatives all paint a nuanced picture of the affordability crisis. (Visualizations coming soon!)</p>
        <ul class="nyt-bullets">
            <li>Tuition and enrollment trends over time (charts)</li>
            <li>Debt by state/major</li>
            <li>Alternatives enrollment trends</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer with shadcn badge and creative callout
st.markdown('<div class="nyt-center nyt-badge-row">', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown(
    """
<div class='nyt-center' style='text-align: right; font-size: 0.9em; color: #888;'>
    <em>Designed for CSCI3311 Data Visualization &mdash; Spring 2025</em>
</div>
""",
    unsafe_allow_html=True,
)
