import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Add the parent directory to sys.path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collegescore import CollegeScorecardClient

# Set page config
st.set_page_config(
    page_title="College Data Explorer - Appendix",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add CSS for styling
st.markdown("""
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
    .back-link {
        margin-top: 2rem;
        display: block;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">College Data Explorer</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">Interactive Analysis of College Affordability Data</h2>', unsafe_allow_html=True)

# Main content
st.markdown("""
This multi-page application allows you to explore detailed data on college affordability, costs, debt, and outcomes.
Use the navigation in the sidebar to access different analysis tools and visualizations.
""")

# Overview of available pages
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3>Available Analysis Tools</h3>', unsafe_allow_html=True)
st.markdown("""
* **Data Explorer**: Filter and analyze college data by year, state, and institution type
* **Tuition Trends**: Visualize tuition trends over time with interactive charts
* **Debt Analysis**: Explore student debt patterns across different demographics
* **ROI Calculator**: Calculate and compare return on investment for different institutions
""")
st.markdown('</div>', unsafe_allow_html=True)

# Quick stats
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3>Dataset Overview</h3>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Years Available", "2017-2022", "6 years of data")
with col2:
    st.metric("Institutions", "6,000+", "Across the U.S.")
with col3:
    st.metric("Data Points", "50+", "Per institution")
st.markdown('</div>', unsafe_allow_html=True)

# Getting started guide
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3>Getting Started</h3>', unsafe_allow_html=True)
st.markdown("""
1. Use the **sidebar navigation** to select the analysis tool you want to use
2. Apply **filters** to customize your view (year range, state, institution type)
3. **Explore the data** through interactive visualizations and tables
4. **Download** custom datasets for your own analysis
""")
st.markdown('</div>', unsafe_allow_html=True)

# API information
with st.expander("About the Data Source"):
    st.markdown("""
    This application uses data from the **College Scorecard API** provided by the U.S. Department of Education.
    The College Scorecard provides data on institutions of higher education including costs, student outcomes, and more.
    
    Key metrics available include:
    - Tuition and fees (in-state and out-of-state)
    - Total cost of attendance
    - Net price after financial aid
    - Median student debt
    - Earnings after graduation
    - Enrollment demographics
    
    For more information, visit the [College Scorecard website](https://collegescorecard.ed.gov/).
    """)

# Back to main app button
st.markdown("""
<div class="back-link">
    <a href="/" target="_self" class="nav-button">
        ← Return to Main Application
    </a>
</div>
""", unsafe_allow_html=True) 