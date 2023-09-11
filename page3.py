import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import matplotlib.patches as patches
import plotly.graph_objects as go
import Functions as tp
from streamlit_option_menu import option_menu
import Functions as objFun

larger_font_size = "50px"

def styled_box(icon, title, value):
        return f"""
            <div style='background-color: #F0F8FF;
                        padding: 20px;
                        border: 2px solid #1E90FF;
                        border-radius: 10px;
                        text-align: center;
                        box-shadow: 5px 5px 5px grey;'>
                <span style='font-size: 30px;'>{icon}</span>
                <p style='font-size: 24px; margin: 5px;'>{title}</p>
                <p style='font-size: 30px;'>{value}</p>
            </div>
        """
        
df = pd.read_excel(
    io="psdp.xlsx",
    engine='openpyxl',
    sheet_name='Umbrella',
    skiprows=0,
    usecols='A:F',
    nrows=50000,
)

def app():
    
    df = pd.read_excel(
        io="psdp.xlsx",
        engine='openpyxl',
        sheet_name='data',
        skiprows=0,
        usecols='A:L',
        nrows=50000,
    )
     
    
    selected_option = option_menu(None, ["Budget Execution (2023-24)", "Physical & Financial Detail", 'Monitoring Report'], 
        icons=['house', "list-task", 'gear'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green"},
        }
    )

    # Depending on the selected option, run different code and display different results
    if selected_option == "Budget Execution (2023-24)":
        # Add your code for the 'Budget Execution (2023-24)' option here
        project_names = df["projectname"].unique()
        selected_project = st.selectbox('Select the Project', project_names)

        # Filter the DataFrame based on the selected project
        df_selection = df[df["projectname"] == selected_project]

        total_budget = df_selection ['Original Budget'].sum() / 1000000
        released_budget = df_selection ['Released Budget'].sum() / 1000000
        total_expenditure = df_selection ['Expenditure'].sum() / 1000000
        

        st.markdown("---")
        objFun.projectInfoCard(total_budget,released_budget,total_expenditure )

        st.markdown("---")
        

        objFun.circulechart(total_budget,released_budget,total_expenditure,selected_project)
        

        st.markdown("---")

    ##################
        df_grouped = df_selection.groupby('head')[['Expenditure', 'Released Budget']].sum().reset_index()

        # Plot Bars
        #plt.figure(figsize=(16, 10), dpi=80)
        plt.figure(figsize=(20, 10))
        bar_width = 0.35
        bar_positions = range(len(df_grouped))

        plt.bar(bar_positions, df_grouped['Expenditure'], color='skyblue', width=bar_width, label='Expenditure')
        plt.bar([pos + bar_width for pos in bar_positions], df_grouped['Released Budget'], color='lightgreen', width=bar_width, label='Released Budget')

        # Add data labels
        for i, (exp_val, rel_val) in enumerate(zip(df_grouped['Expenditure'].values, df_grouped['Released Budget'].values)):
            plt.text(i, exp_val, int(exp_val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight': 500, 'size': 12})
            plt.text(i + bar_width, rel_val, int(rel_val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight': 500, 'size': 12})

        # Decoration
        plt.gca().set_xticks([pos + bar_width / 2 for pos in bar_positions])
        plt.gca().set_xticklabels(df_grouped['head'], rotation=60, horizontalalignment='right')
        plt.title(f"Expenditure vs Released Budget for {selected_project} (Head-Wise)", fontsize=22, pad=40)
        plt.legend()
        plt.ylim(0, max(df_grouped['Expenditure'].max(), df_grouped['Released Budget'].max()) + 500)

        # Display the plot in Streamlit
        st.pyplot(plt)
            # You can add your charts, data, or any other content specific to this option here.

    elif selected_option == "Physical & Financial Detail":
        # Add your code for the 'Physical & Financial Detail' option here
        st.write("Displaying Physical & Financial Detail data")
        # You can add your charts, data, or any other content specific to this option here.

    elif selected_option == 'Monitoring Report':
        # Add your code for the 'Monitoring Report' option here
        st.write("Displaying Monitoring Report data")
        # You can add your charts, data, or any other content specific to this option here.

    # You can add an 'else' block for handling unexpected options if needed.
