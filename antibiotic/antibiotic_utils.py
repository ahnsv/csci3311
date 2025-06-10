import pandas as pd
import requests
import streamlit as st

def load_burtin_data(url: str = "https://cdn.jsdelivr.net/npm/vega-datasets@1/data/burtin.json") -> pd.DataFrame:
    """
    Load the Burtin antibiotic dataset from the given URL and return as a pandas DataFrame.
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    return df

def get_antibiotics():
    """
    Return the list of antibiotics in the dataset.
    """
    return ["Penicillin", "Streptomycin", "Neomycin"]

def get_gram_types():
    """
    Return the list of Gram stain types in the dataset.
    """
    return ["positive", "negative"]

def show_sidebar_footer():
    st.sidebar.markdown("""
    ---
    <sub>
    Built by <a href="https://github.com/ahnsv" target="_blank">@ahnsv</a> |
    <a href="https://www.linkedin.com/in/humphrey-ahn" target="_blank">LinkedIn</a>
    </sub>
    """, unsafe_allow_html=True) 