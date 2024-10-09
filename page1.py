import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import random
import warnings
warnings.filterwarnings("ignore")
from typing import ValuesView
import Functions 

def app():

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    df =  pd.read_excel(
        io="psdp.xlsx",
        engine='openpyxl',
        sheet_name='data',
        skiprows= 0,
        usecols='A:L',
        nrows=50000,
    )

    st.title(":bar_chart: PSDP (12) on Going Projects ( Budget Execution) FY 2023-24")
    st.markdown("#")

    total_budget = df['Original Budget'].sum() / 1000000
    released_budget = df['Released Budget'].sum() / 1000000
    total_expenditure = df['Expenditure'].sum() / 1000000
    
    st.markdown("---")
    Functions.printinfo(total_budget, released_budget, total_expenditure)
    st.markdown("---")
    st.markdown("##")

    left_column, right_column = st.columns(2)

    with left_column:
        labels = 'Total Budget', 'Released Budget'
        sizes = [total_budget - released_budget, released_budget]
        explode = (0, 0.1)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.01f%%',
                shadow=False, startangle=60)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("Allocated Budget vs. Actual Release %")
        st.pyplot(fig1)

    with right_column:
        labels = 'Released Budget', 'Expenditure'
        expenditure_percentage = (total_expenditure / released_budget) * 100

        # Check if expenditure exceeds released budget
        if total_expenditure > released_budget:
            expenditure_percentage = 100  # Expenditure exceeds or equals release
            remaining_percentage = 0      # No remaining budget
        else:
            remaining_percentage = 100 - expenditure_percentage  # Remaining budget percentage

        sizes = [remaining_percentage, expenditure_percentage]
        explode = (0, 0.1)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.01f%%',
                shadow=False, startangle=60)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("Expenditure vs. Budget Released %")
        st.pyplot(fig1)

    st.markdown("##")
    st.markdown("---")
    st.markdown("##")
