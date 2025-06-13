import pandas as pd
from data import fetch_college_data, prepare_cost_data, prepare_enrollment_data
from visuals import cost_bar_chart, demographic_stacked_chart, enrollment_bar_chart

import streamlit as st
import numpy as np
import altair as alt

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
        <a href="#section1" class="toc-item toc-anchor">1. Sticker Shock</a>
        <a href="#section2" class="toc-item toc-anchor">2. Enrollment Patterns</a>
        <a href="#section3" class="toc-item toc-anchor">3. The Debt Question</a>
        <a href="#section4" class="toc-item toc-anchor">4. Alternatives Rising</a>
        <a href="#section5" class="toc-item toc-anchor">5. ROI in 2025</a>
        <a href="#section6" class="toc-item toc-anchor">6. Equity & Access</a>
        <a href="#section7" class="toc-item toc-anchor">7. Cultural Shift</a>
        <a href="#section8" class="toc-item toc-anchor">8. Policy & Future</a>
        <a href="#section9" class="toc-item toc-anchor">9. Data Deep-Dive</a>
        <a href="#conclusion" class="toc-item toc-anchor">10. Conclusion</a>
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

# --- UI Controls ---
years = [f"{y}" for y in range(2017, 2023)]
year = st.selectbox("Select Year", years, index=len(years) - 1)
control_map = {
    "All": None,
    "Public": "1",
    "Private Nonprofit": "2",
    "Private For-Profit": "3",
}
control = st.selectbox("Institution Type", list(control_map.keys()))
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

# --- Data Fetching ---
data = fetch_college_data(
    year, control=control_map[control], state=None if state == "All" else state
)
df = pd.DataFrame(data)

# --- Section 1: Cost Visualizations ---
figure_counter = 1
st.markdown(
    '''
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
    ''',
    unsafe_allow_html=True,
)
st.header("Section 1: College Cost Data Explorer")
if not df.empty:
    cost_data, cost_melted, avg_cost = prepare_cost_data(df, year)
    st.altair_chart(cost_bar_chart(avg_cost, year), use_container_width=True)
    st.caption(f"Figure {figure_counter}: Average college costs by institution type (mock data).")
    figure_counter += 1
    st.subheader("Top 10 Most Expensive Institutions (Total Cost)")
    st.dataframe(
        cost_data.sort_values("Total Cost", ascending=False).head(10)[
            ["Institution", "State", "Type", "Total Cost"]
        ]
    )
    st.caption(f"Figure {figure_counter}: Top 10 most expensive institutions by total cost (mock data).")
    figure_counter += 1
else:
    st.info("No data available for the selected filters.")
st.markdown("</div>", unsafe_allow_html=True)

# --- Section 2: Enrollment Visualizations ---
st.markdown(
    '''
    <div class="nyt-center nyt-section" id="section2">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">2. Who's Deciding Not to Go? Changing Enrollment Patterns</h2>
        <div class="nyt-blockquote">
            "Enrollment in higher education is no longer a given. Rising costs and shifting demographics are changing who goes to college—and who doesn't."
        </div>
        <p style="font-size:1.1em;">
            Enrollment in U.S. colleges has declined for several years, with the sharpest drops among low-income and minority students. The reasons are complex: affordability, changing job markets, and shifting cultural values all play a role.
        </p>
        <ul class="nyt-bullets">
            <li>Declining enrollment numbers</li>
            <li>Demographic differences (race, income, region)</li>
            <li>Who's most affected by rising costs?</li>
        </ul>
    </div>
    ''',
    unsafe_allow_html=True,
)
st.header("Section 2: Enrollment Patterns Explorer")
if not df.empty:
    enroll_data, enroll_by_type, demo_melted = prepare_enrollment_data(df, year)
    st.altair_chart(
        enrollment_bar_chart(enroll_by_type, year), use_container_width=True
    )
    st.caption(f"Figure {figure_counter}: Total enrollment by institution type (mock data).")
    figure_counter += 1
    st.altair_chart(
        demographic_stacked_chart(demo_melted, year), use_container_width=True
    )
    st.caption(f"Figure {figure_counter}: Demographic breakdown of enrollment by institution type (mock data).")
    figure_counter += 1
else:
    st.info("No enrollment data available for the selected filters.")
st.markdown("</div>", unsafe_allow_html=True)

# --- Section 3: The Debt Question ---
st.markdown(
    '''
    <div class="nyt-center nyt-section" id="section3">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">3. The Debt Question: How Loans Shape Life After Graduation</h2>
        <div class="nyt-blockquote">
            "Student debt has become a defining feature of American adulthood, shaping life choices long after graduation."
        </div>
        <p style="font-size:1.1em;">
            The average student now graduates with tens of thousands in debt. For some, repayment is manageable; for others, it's a lifelong burden. Default rates remain stubbornly high, especially among those who don't complete their degrees.
        </p>
        <ul class="nyt-bullets">
            <li>Average student debt levels</li>
            <li>Default rates and repayment struggles</li>
            <li>Stories/case studies of recent grads</li>
        </ul>
    </div>
    ''',
    unsafe_allow_html=True,
)

debt_states = ["All", "CA", "TX", "NY", "FL", "IL"]
selected_debt_state = st.selectbox("Select State for Debt Data", debt_states, key="debt_state")
debt_data = pd.DataFrame({
    "Type": ["Public", "Private Nonprofit", "Private For-Profit"],
    "Avg Debt": [28000, 34000, 39000]
})
st.bar_chart(debt_data.set_index("Type"))
st.caption(f"Figure {figure_counter}: Average student debt by institution type (mock data).")
figure_counter += 1

default_data = pd.DataFrame({
    "Status": ["Defaulted", "Not Defaulted"],
    "Percent": [12, 88]
})
st.altair_chart(
    alt.Chart(default_data).mark_arc().encode(
        theta="Percent",
        color="Status",
        tooltip=["Status", "Percent"]
    ).properties(title="Loan Default Rate (Mock Data)")
)
st.caption(f"Figure {figure_counter}: Proportion of borrowers who default on their student loans (mock data).")
figure_counter += 1
st.info("\"I graduated with $32,000 in debt. My payments are more than my rent.\" – Recent Grad, TX")
st.markdown("</div>", unsafe_allow_html=True)

# --- Section 4: Alternatives on the Rise ---
st.markdown(
    '''
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
    ''',
    unsafe_allow_html=True,
)

alt_types = st.multiselect("Show alternatives:", ["Vocational", "Apprenticeship", "Military", "Gap Year"], default=["Vocational", "Apprenticeship"])
years_alt = list(range(2015, 2023))
alt_data = pd.DataFrame({
    "Year": years_alt,
    "Vocational": np.linspace(100000, 180000, len(years_alt)),
    "Apprenticeship": np.linspace(50000, 90000, len(years_alt)),
    "Military": np.linspace(30000, 35000, len(years_alt)),
    "Gap Year": np.linspace(10000, 25000, len(years_alt)),
})
alt_data_melted = alt_data.melt("Year", var_name="Type", value_name="Enrollment")
alt_data_melted = alt_data_melted[alt_data_melted["Type"].isin(alt_types)]
st.altair_chart(
    alt.Chart(alt_data_melted).mark_area(opacity=0.7).encode(
        x="Year:O", y="Enrollment:Q", color="Type:N", tooltip=["Year", "Type", "Enrollment"]
    ).properties(title="Alternative Pathways Enrollment (Mock Data)", width=600, height=350),
    use_container_width=True
)
st.caption(f"Figure {figure_counter}: Enrollment in alternative pathways such as vocational programs and apprenticeships (mock data).")
figure_counter += 1
st.success("Community college enrollment is up 15% since 2018 (mock stat).")
st.markdown("</div>", unsafe_allow_html=True)

# --- Section 5: Is It Still Worth It? ---
st.markdown(
    '''
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
    ''',
    unsafe_allow_html=True,
)

majors = ["Engineering", "Business", "Education", "Arts", "Health"]
selected_major = st.selectbox("Select Major", majors, key="roi_major")
roi_data = pd.DataFrame({
    "Major": majors,
    "Median Earnings": [80000, 60000, 45000, 35000, 70000],
    "Median Debt": [25000, 22000, 18000, 16000, 20000]
})
st.altair_chart(
    alt.Chart(roi_data).transform_filter(
        alt.FieldEqualPredicate(field="Major", equal=selected_major)
    ).mark_bar().encode(
        x="Major:N", y="Median Earnings:Q", color=alt.value("steelblue"), tooltip=["Major", "Median Earnings"]
    ).properties(title="Median Earnings by Major", width=400),
    use_container_width=True
)
st.caption(f"Figure {figure_counter}: Median earnings for selected major (mock data).")
figure_counter += 1
st.altair_chart(
    alt.Chart(roi_data).transform_filter(
        alt.FieldEqualPredicate(field="Major", equal=selected_major)
    ).mark_bar(color="orange").encode(
        x="Major:N", y="Median Debt:Q", tooltip=["Major", "Median Debt"]
    ).properties(title="Median Debt by Major", width=400),
    use_container_width=True
)
st.caption(f"Figure {figure_counter}: Median student debt for selected major (mock data).")
figure_counter += 1
st.markdown("</div>", unsafe_allow_html=True)

# --- Section 6: Equity and Access ---
st.markdown(
    '''
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
    ''',
    unsafe_allow_html=True,
)

groups = ["White", "Black", "Hispanic", "Asian", "First-Gen", "Low-Income"]
selected_group = st.radio("Select Group", groups, key="equity_group")
equity_data = pd.DataFrame({
    "Group": groups,
    "Attendance Rate": [0.65, 0.45, 0.40, 0.70, 0.35, 0.38]
})
st.altair_chart(
    alt.Chart(equity_data).mark_bar().encode(
        x="Group:N", y="Attendance Rate:Q", color="Group:N", tooltip=["Group", alt.Tooltip("Attendance Rate", format=".0%")]
    ).properties(title="College Attendance Rate by Group (Mock Data)", width=600),
    use_container_width=True
)
st.caption(f"Figure {figure_counter}: College attendance rates by demographic group (mock data).")
figure_counter += 1
st.warning("First-gen students are 30% less likely to graduate (mock stat).")
st.markdown("</div>", unsafe_allow_html=True)

# --- Section 7: The Cultural Shift ---
st.markdown(
    '''
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
    ''',
    unsafe_allow_html=True,
)

importance = st.slider("How important is a college degree for success?", 0, 100, 60)
st.progress(importance)
cultural_data = pd.DataFrame({
    "Value": ["Skills", "Degree", "Experience", "Network", "Entrepreneurship"],
    "Percent": [35, 25, 20, 10, 10]
})
st.altair_chart(
    alt.Chart(cultural_data).mark_bar().encode(
        x="Value:N", y="Percent:Q", color="Value:N", tooltip=["Value", "Percent"]
    ).properties(title="What Americans Value for Success (Mock Poll)", width=600),
    use_container_width=True
)
st.caption(f"Figure {figure_counter}: What Americans say matters most for success in 2025 (mock poll).")
figure_counter += 1
st.info("In 2025, only 25% of young adults say a degree is 'very important' for success (mock poll).")
st.markdown("</div>", unsafe_allow_html=True)

# --- Section 8: Policy and the Future ---
st.markdown(
    '''
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
    ''',
    unsafe_allow_html=True,
)

policies = ["Loan Forgiveness", "Free College", "Income-Driven Repayment", "Online Degrees"]
selected_policies = st.multiselect("Show Policy Support:", policies, default=policies, key="policy_multiselect")
policy_data = pd.DataFrame({
    "Policy": policies,
    "Support": [0.60, 0.48, 0.55, 0.35]
})
policy_data = policy_data[policy_data["Policy"].isin(selected_policies)]
st.altair_chart(
    alt.Chart(policy_data).mark_bar().encode(
        x="Policy:N", y=alt.Y("Support:Q", axis=alt.Axis(format='%')), color="Policy:N", tooltip=["Policy", alt.Tooltip("Support", format='.0%')]
    ).properties(title="Public Support for Policy Proposals (Mock Data)", width=600),
    use_container_width=True
)
st.caption(f"Figure {figure_counter}: Public support for major college affordability policy proposals (mock data).")
figure_counter += 1
st.success("60% of Americans support some form of student debt relief (mock poll).")
st.markdown("</div>", unsafe_allow_html=True)

# --- Section 9: Data Deep-Dive ---
st.markdown(
    '''
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
    ''',
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["Tuition", "Enrollment", "Debt"])
with tab1:
    st.write("Explore tuition data (mock).")
    st.dataframe(pd.DataFrame({
        "Institution": ["A", "B", "C"],
        "In-State Tuition": [12000, 15000, 18000],
        "Out-of-State Tuition": [22000, 25000, 28000]
    }))
    st.caption(f"Figure {figure_counter}: Sample tuition data for selected institutions (mock data).")
    figure_counter += 1
with tab2:
    st.write("Explore enrollment data (mock).")
    st.dataframe(pd.DataFrame({
        "Institution": ["A", "B", "C"],
        "Enrollment": [10000, 15000, 20000]
    }))
    st.caption(f"Figure {figure_counter}: Sample enrollment data for selected institutions (mock data).")
    figure_counter += 1
with tab3:
    st.write("Explore debt data (mock).")
    st.dataframe(pd.DataFrame({
        "Institution": ["A", "B", "C"],
        "Avg Debt": [25000, 30000, 35000]
    }))
    st.caption(f"Figure {figure_counter}: Sample student debt data for selected institutions (mock data).")
    figure_counter += 1
st.markdown("</div>", unsafe_allow_html=True)

# --- Section 10: Conclusion ---
st.markdown(
    '''
    <div class="nyt-center nyt-section" id="conclusion">
        <h2 style="font-size:1.5em; font-weight:600; margin-bottom:0.5em;">10. Conclusion: The Future of College Affordability</h2>
        <div class="nyt-blockquote">
            "The story of college affordability is still being written. The choices we make today will shape the opportunities of tomorrow."
        </div>
        <p style="font-size:1.1em;">
            The data and stories explored here reveal a complex, evolving landscape. While higher education remains a powerful engine of opportunity, its rising costs and shifting value proposition demand new thinking from policymakers, institutions, and families alike.<br><br>
            As you reflect on these trends, consider: What does an affordable, equitable, and effective system of higher education look like? How can we ensure that the promise of college remains within reach for all?
        </p>
        <ul class="nyt-bullets">
            <li>Affordability and access are central to the American Dream</li>
            <li>Data-driven policy and innovation are needed for the future</li>
            <li>Your voice and choices matter in shaping what comes next</li>
        </ul>
        <p style="font-size:1.1em; color:#7c3aed; font-weight:500;">
            Thank you for exploring the college affordability crisis. Share your thoughts, and let's keep the conversation going.
        </p>
    </div>
    ''',
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
