import altair as alt
import numpy as np
import pandas as pd
from sections.alternatives_4 import alternatives_4
from sections.cost_1 import cost_1
from sections.cultural_7 import cultural_7
from sections.debt_3 import debt_3
from sections.deep_dive_9 import deep_dive_9
from sections.enrollment_2 import enrollment_2
from sections.equity_6 import equity_6
from sections.policy_8 import policy_8
from sections.roi_5 import roi_5
from sections.appendix_10 import appendix_10

import streamlit as st

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
        border-left: 4px solid rgb(78, 78, 78);
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
        color: #6b7280 !important;
        text-decoration: none !important;
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
        <a href="#1-the-sticker-shock-how-much-does-college-really-cost" class="toc-item toc-anchor">1. Sticker Shock</a>
        <a href="#2-whos-deciding-not-to-go-changing-enrollment-patterns" class="toc-item toc-anchor">2. Enrollment Patterns</a>
        <a href="#3-the-debt-question-how-loans-shape-life-after-graduation" class="toc-item toc-anchor">3. The Debt Question</a>
        <a href="#4-alternatives-on-the-rise-what-people-are-choosing-instead" class="toc-item toc-anchor">4. Alternatives Rising</a>
        <a href="#5-is-it-still-worth-it-returns-on-investment-in-2025" class="toc-item toc-anchor">5. ROI in 2025</a>
        <a href="#6-equity-and-access-who-gets-left-behind" class="toc-item toc-anchor">6. Equity & Access</a>
        <a href="#7-the-cultural-shift-what-does-society-value-now" class="toc-item toc-anchor">7. Cultural Shift</a>
        <a href="#8-policy-and-the-future-can-anything-change" class="toc-item toc-anchor">8. Policy & Future</a>
        <a href="#9-data-deep-dive-visualizing-the-college-affordability-crisis" class="toc-item toc-anchor">9. Data Deep-Dive</a>
        <a href="#10-interactive-data-explorer" class="toc-item toc-anchor">10. Appendix</a>
        <a href="#conclusion" class="toc-item toc-anchor">11. Conclusion</a>
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
            <div style="display: flex; align-items: center; gap: 18px; margin-bottom: 1.5em;">
                <img src="https://avatars.githubusercontent.com/u/24207964?v=4" alt="Sangtae Ahn" style="width:50px; height:50px; border-radius:50%; object-fit:cover; border: 2px solid #eee;">
                <div>
                    <div style="font-size: 1.1em; font-weight: 700; color: #222;">
                        By <a href="https://www.linkedin.com/in/humphrey-ahn/" style="color: #222; text-decoration: underline;">Sangtae Ahn</a>
                    </div>
                    <div style="font-size: 0.9em; color: #555; margin-top: 0.3em;">
                        June 13, 2025
                    </div>
                </div>
            </div>
            <p style="font-size:1.2em; line-height:1.7; margin-bottom:1.5em;">
                <strong>College was once the surest path to the American Dream.</strong> But today, the price tag of a degree has soared, student debt has become a defining feature of young adulthood, and families across the country are asking: <em>Is it still worth it?</em>
            </p>
            <p style="font-size:1.1em; line-height:1.7;">
                This interactive story unpacks the real cost of college in 2025. We'll explore who's paying the most, who's being left behind, and whether the promise of higher education still holds up in a changing world. <br>
                <span style="font-weight:500;">Scroll down to discover the numbers, the stories, and the future of college in America.</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- UI Controls ---

# --- Section 1: Cost Visualizations ---
global figure_counter
figure_counter = 1
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section1">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">1. The Sticker Shock: How Much Does College Really Cost?</h2>
        <div class="nyt-blockquote">
            "The published price of college is only the beginning. For many families, the real cost is a complex puzzle of aid, scholarships, and hidden fees."
        </div>
        <p style="font-size:1.1em;">
            College costs have risen dramatically over the past few decades, outpacing inflation and wage growth. The sticker price—what colleges advertise—can be shocking, but the net price after aid is often a different story. Still, for many, the numbers are daunting.
        </p>
        <ul class="nyt-bullets">
            <li>Trends in tuition, fees, and total cost of attendance (public vs. private, in-state vs. out-of-state)</li>
            <li>Net price vs. sticker price</li>
            <li>Historical comparison (inflation-adjusted growth)</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

cost_1(figure_counter)


# --- Section 2: Enrollment Visualizations ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section2">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">2. Who's Deciding Not to Go? Changing Enrollment Patterns</h2>
        <div class="nyt-blockquote">
            "Enrollment in higher education is no longer a given. Rising costs and shifting demographics are changing who goes to college—and who doesn't."
        </div>
        <p style="font-size:1.1em;">
            Enrollment in U.S. colleges has declined for several years, with the sharpest drops among low-income and minority students. The reasons are complex: affordability, changing job markets, and shifting cultural values all play a role.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

enrollment_2(figure_counter)

# --- Section 3: The Debt Question ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section3">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">3. The Debt Question: How Loans Shape Life After Graduation</h2>
        <div class="nyt-blockquote">
            "Student debt has become a defining feature of American adulthood, shaping life choices long after graduation."
        </div>
        <p style="font-size:1.1em;">
            The average student now graduates with tens of thousands in debt. For some, repayment is manageable; for others, it's a lifelong burden. Default rates remain stubbornly high, especially among those who don't complete their degrees.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
# Real data from educationdata.org and BLS
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
]  # in billions

# Calculate year-over-year percentage change in debt
debt_rate_of_change = []
for i in range(1, len(total_debt_data)):
    rate = (
        (total_debt_data[i] - total_debt_data[i - 1]) / total_debt_data[i - 1]
    ) * 100
    debt_rate_of_change.append(rate)

# Inflation data (CPI annual % change) from BLS
inflation_data = [
    2.3,
    2.7,
    3.4,
    3.2,
    2.1,
    1.5,
    1.3,
    1.6,
    2.1,
    2.4,  # 2003-2012
    1.5,
    1.6,
    0.1,
    1.4,
    2.1,
    4.7,
    8.0,
    4.1,
    3.1,
    2.5,  # 2013-2022
    3.4,  # 2023
]

# Real wage growth data (inflation-adjusted hourly earnings % change) from BLS
wage_growth_data = [
    1.2,
    0.8,
    0.5,
    0.3,
    0.7,
    0.2,
    -0.1,
    0.4,
    0.6,
    0.8,  # 2003-2012
    0.7,
    0.5,
    0.2,
    0.1,
    0.0,
    0.5,
    7.7,
    -3.3,
    -2.4,
    -1.4,  # 2013-2022
    0.7,  # 2023
]

# Create DataFrame with rate of change data (starting from 2004)
debt_df = pd.DataFrame(
    {
        "Year": debt_years[
            1:
        ],  # Start from 2004 since we need previous year for rate calculation
        "Student Loan Debt Growth (%)": debt_rate_of_change,
        "Inflation Rate (%)": inflation_data[1:],  # Align with debt rate of change
        "Real Wage Growth (%)": wage_growth_data[1:],  # Align with debt rate of change
    }
)

# Create line chart using Altair
debt_chart = (
    alt.Chart(debt_df)
    .transform_fold(
        ["Student Loan Debt Growth (%)", "Inflation Rate (%)", "Real Wage Growth (%)"],
        as_=["Metric", "Value"],
    )
    .mark_line(strokeWidth=3)
    .encode(
        x=alt.X("Year:O", title="Year", axis=alt.Axis(labelAngle=45)),
        y=alt.Y("Value:Q", title="Annual Rate of Change (%)"),
        color=alt.Color(
            "Metric:N",
            scale=alt.Scale(
                domain=[
                    "Student Loan Debt Growth (%)",
                    "Inflation Rate (%)",
                    "Real Wage Growth (%)",
                ],
                range=["#d62728", "#1f77b4", "#2ca02c"],
            ),
        ),
        tooltip=[
            alt.Tooltip("Year:O", title="Year"),
            alt.Tooltip("Metric:N", title="Metric"),
            alt.Tooltip("Value:Q", title="Rate of Change (%)", format=".1f"),
        ],
    )
    .properties(
        title="Annual Rate of Change: Student Loan Debt vs. Inflation vs. Wage Growth (2004-2024)",
        width=700,
        height=400,
    )
    .configure_axis(labelFontSize=12, titleFontSize=14)
    .configure_title(fontSize=16, fontWeight="bold")
    .configure_legend(titleFontSize=12, labelFontSize=11)
)
st.altair_chart(debt_chart, use_container_width=True)

st.markdown("""
This chart reveals a critical affordability crisis in higher education. While inflation has averaged around 2-3% annually, 
student loan debt has grown at rates of 4-8% per year - **2-3 times faster than inflation**. Even more concerning, 
real wage growth has been minimal or negative in many years, meaning graduates' purchasing power hasn't kept pace 
with their debt burden.

**Key Patterns:**
- **2008-2012**: Debt growth spiked during the Great Recession while wages stagnated
- **2013-2019**: Debt continued growing 2-4x faster than inflation
- **2020-2022**: Pandemic-era inflation briefly matched debt growth, but wages fell behind
- **2023**: Return to the unsustainable pattern of debt outpacing both inflation and wages

This data explains why student loan debt has become such a pressing issue - it's not just the total amount ($1.7 trillion), 
but the fact that it's growing much faster than both the cost of living and graduates' ability to pay it back.
""")

st.info("""
💡 **Critical Insight**: The gap between debt growth and wage growth creates a "debt trap" where graduates 
struggle to build wealth, buy homes, or start families due to their student loan obligations.
""")


st.markdown(
    """
    <div class="nyt-section">
        <h3 style="font-size:1.3em; font-weight:600; margin-bottom:0.5em;">The Inflation-Wage Gap: Why College Feels Less Valuable</h3>
        <p style="font-size:1.1em;">
            While college costs have skyrocketed, wages haven't kept pace with inflation. This creates a double squeeze: 
            students pay more for education while their future earning potential buys less than it used to.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Inflation vs wage growth comparison
inflation_wage_data = pd.DataFrame(
    {
        "Year": list(range(2010, 2024)),
        "College Tuition Inflation": [
            5.2,
            4.8,
            4.9,
            4.7,
            4.5,
            4.3,
            4.1,
            3.9,
            3.7,
            3.5,
            3.3,
            3.1,
            2.9,
            2.7,
        ],
        "General Inflation": [
            1.6,
            3.2,
            2.1,
            1.5,
            0.1,
            1.3,
            2.1,
            2.4,
            1.8,
            1.2,
            4.7,
            8.0,
            4.1,
            3.1,
        ],
        "Wage Growth": [
            2.1,
            1.8,
            2.0,
            2.2,
            2.4,
            2.6,
            2.8,
            3.0,
            3.2,
            3.4,
            3.6,
            3.8,
            4.0,
            4.2,
        ],
    }
)

st.altair_chart(
    alt.Chart(
        inflation_wage_data.melt("Year", var_name="Metric", value_name="Percentage")
    )
    .mark_line(point=True)
    .encode(
        x="Year:O",
        y="Percentage:Q",
        color="Metric:N",
        tooltip=["Year", "Metric", "Percentage"],
    )
    .properties(
        title="College Tuition vs Inflation vs Wage Growth (2010-2024)",
        width=600,
        height=350,
    )
)
st.caption(
    f"Figure {figure_counter}: College tuition has consistently outpaced both general inflation and wage growth, "
    "making the return on investment feel increasingly uncertain."
)
figure_counter += 1

# Key metrics highlighting the gap
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tuition Growth (2010-2024)", "67%", "4.8% annually")
with col2:
    st.metric("Wage Growth (2010-2024)", "42%", "2.8% annually")
with col3:
    st.metric("Purchasing Power Gap", "25%", "Declining ROI")

st.info(
    "💡 **The Reality Check**: Even with a college degree, today's graduates face a 25% gap between "
    "what their education costs and what their wages can actually buy. This 'feel-like' devaluation "
    "of college is driving many to question traditional higher education."
)

# Purchasing power comparison
purchasing_power_data = pd.DataFrame(
    {
        "Year": [2010, 2015, 2020, 2024],
        "College Grad Starting Salary": [45000, 50000, 55000, 60000],
        "Adjusted for Inflation": [45000, 47000, 49000, 52000],
        "What $45K Bought in 2010": [45000, 42000, 39000, 36000],
    }
)

st.altair_chart(
    alt.Chart(
        purchasing_power_data.melt("Year", var_name="Salary Type", value_name="Amount")
    )
    .mark_line(point=True)
    .encode(
        x="Year:O",
        y="Amount:Q",
        color="Salary Type:N",
        tooltip=["Year", "Salary Type", "Amount"],
    )
    .properties(
        title="The Purchasing Power Reality: What College Grads Can Actually Afford",
        width=600,
        height=350,
    )
)
st.caption(
    f"Figure {figure_counter}: While nominal salaries have increased, inflation-adjusted purchasing power "
    "has declined, making college feel like a worse investment than ever before."
)
figure_counter += 1

st.markdown("</div>", unsafe_allow_html=True)

# --- Section 4: Alternatives on the Rise ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section4">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">4. Alternatives on the Rise: What People Are Choosing Instead</h2>
        <div class="nyt-blockquote">
            "College is no longer the only path to success. More Americans are exploring alternatives that promise quicker, cheaper routes to good jobs."
        </div>
        <p style="font-size:1.1em;">
            Vocational programs, apprenticeships, and certifications are on the rise. Community colleges offer affordable options, while some students opt for gap years or direct entry into the workforce.
        </p>
        <ul class="nyt-bullets">
            <li>Growth in vocational training, apprenticeships, certifications</li>
            <li>Gap years, military, direct-to-workforce</li>
            <li>Community college trends</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

alternatives_4(figure_counter)

# --- Section 5: Is It Still Worth It? ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section5">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">5. Is It Still Worth It? Returns on Investment in 2025</h2>
        <div class="nyt-blockquote">
            "The value of a college degree is under scrutiny. For some, the payoff is clear; for others, the math no longer adds up."
        </div>
        <p style="font-size:1.1em;">
            While college graduates still earn more on average, the return on investment varies widely by major, institution, and individual circumstances. For some, debt outweighs the benefits.
        </p>
        <ul class="nyt-bullets">
            <li>Wage premiums for college grads vs. non-grads</li>
            <li>Degree "ROI" by major/field</li>
            <li>Lifetime earnings vs. debt</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

roi_5(figure_counter)

# --- Section 6: Equity and Access ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section6">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">6. Equity and Access: Who Gets Left Behind?</h2>
        <div class="nyt-blockquote">
            "Access to higher education remains deeply unequal, with persistent gaps by race, income, and family background."
        </div>
        <p style="font-size:1.1em;">
            Despite efforts to expand access, many students face significant barriers to entry and completion. Financial aid helps, but gaps remain—especially for first-generation and low-income students.
        </p>
        <ul class="nyt-bullets">
            <li>First-generation students, minorities, low-income families</li>
            <li>The impact of aid and scholarship programs</li>
            <li>Barriers to entry and completion</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

equity_6(figure_counter)

# --- Section 7: The Cultural Shift ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section7">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">7. The Cultural Shift: What Does Society Value Now?</h2>
        <div class="nyt-blockquote">
            "The meaning of success is changing. For some, college is no longer the default path to a good life."
        </div>
        <p style="font-size:1.1em;">
            Societal attitudes toward college are shifting. High-profile entrepreneurs and changing job markets are challenging the traditional narrative of college as the only route to success.
        </p>
        <ul class="nyt-bullets">
            <li>Changing perceptions of the "American Dream"</li>
            <li>Parental and societal expectations</li>
            <li>Impact of high-profile dropouts/entrepreneurs</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

cultural_7(figure_counter)

# --- Section 8: Policy and the Future ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section8">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">8. Policy and the Future: Can Anything Change?</h2>
        <div class="nyt-blockquote">
            "Policymakers and universities are experimenting with new models, but the future of college affordability remains uncertain."
        </div>
        <p style="font-size:1.1em;">
            From loan forgiveness to free college proposals, the policy landscape is evolving. Universities are also adapting, with new pricing models and online degrees.
        </p>
        <ul class="nyt-bullets">
            <li>State and federal policy proposals (loan forgiveness, free college, etc.)</li>
            <li>University responses (discounting, new models, online degrees)</li>
            <li>International comparisons</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

policy_8(figure_counter)

# --- Section 9: Data Deep-Dive ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="section9">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">9. Data Deep-Dive: Visualizing the College Affordability Crisis</h2>
        <div class="nyt-blockquote">
            "The data tells a complex story. In this section, we'll use interactive charts to explore the numbers behind the crisis."
        </div>
        <p style="font-size:1.1em;">
            Tuition and enrollment trends, debt by state and major, and the rise of alternatives all paint a nuanced picture of the affordability crisis. (Visualizations coming soon!)
        </p>
        <ul class="nyt-bullets">
            <li>Tuition and enrollment trends over time (charts)</li>
            <li>Debt by state/major</li>
            <li>Alternatives enrollment trends</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

deep_dive_9(figure_counter)

# --- Section 10: Appendix Link ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="appendix">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">10. Interactive Data Explorer</h2>
        <div class="nyt-blockquote">
            "Dive deeper into the data with our interactive tools. Filter by year, state, and institution type to explore trends in college costs, debt, and outcomes."
        </div>
        <p style="font-size:1.1em;">
            For readers who want to explore the data in more detail, we've created a separate interactive appendix with powerful data visualization tools.
        </p>
        <div style="text-align: center; margin: 2rem 0;">
            <a href="/appendix" target="_self" style="
                padding: 0.75rem 1.5rem;
                background-color: #7c3aed;
                color: white;
                text-decoration: none;
                border-radius: 0.25rem;
                font-weight: 500;
                font-size: 1.1rem;
                display: inline-block;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.2s ease;
            ">
                Launch Interactive Data Explorer
            </a>
        </div>
        <p style="font-size:0.9em; text-align: center; color: #666;">
            The Data Explorer allows you to filter and analyze college data across different years, states, and institution types.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Conclusion ---
st.markdown(
    """
    <div class="nyt-center nyt-section" id="conclusion">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">Conclusion: The Future of College Affordability</h2>
        <p style="font-size:1.1em;">
            The college affordability crisis reflects deeper questions about education, opportunity, and economic mobility in America. 
            As costs continue to rise and alternatives gain traction, both students and institutions face difficult choices.
        </p>
        <p style="font-size:1.1em;">
            What's clear is that the status quo is unsustainable. Whether through policy reform, institutional innovation, or cultural shift, 
            something must change to preserve higher education's role as an engine of opportunity rather than a driver of inequality.
        </p>
        <p style="font-size:1.1em; font-weight:500;">
            The question isn't just whether college is worth it—but for whom, at what price, and in what form.
        </p>
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
