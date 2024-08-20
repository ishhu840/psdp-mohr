import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import Functions as objFun
from streamlit_option_menu import option_menu

# Function to create a styled box for displaying key metrics
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

# Main app function
def app():
    
    # Hide Streamlit's default menu and footer
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    # Load data from Excel
    df = pd.read_excel(
        io="psdp.xlsx",
        engine='openpyxl',
        sheet_name='data',
        skiprows=0,
        usecols='A:L',
        nrows=50000,
    )
     
    # Option menu for navigation
    selected_option = option_menu(
        None, 
        ["Budget Execution (2023-24)", "Projects < 70% Expenditure", 'Projects Headwise Expenditure'], 
        icons=['house', "list-task", 'gear'], 
        menu_icon="cast", 
        default_index=0, 
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green"},
        }
    )

    # Option 1: Budget Execution (2023-24)
    if selected_option == "Budget Execution (2023-24)":
        project_names = df["projectname"].unique()
        st.markdown("---")
        selected_project = st.selectbox('Select the Project', project_names)

        # Filter the DataFrame based on the selected project
        df_selection = df[df["projectname"] == selected_project]

        total_budget = df_selection['Original Budget'].sum() / 1000000
        released_budget = df_selection['Released Budget'].sum() / 1000000
        Expenditure = df_selection['Expenditure'].sum() / 1000000
        
        st.markdown("---")
        objFun.projectInfoCard(total_budget, released_budget, Expenditure)

        st.markdown("---")
        objFun.circulechart(total_budget, released_budget, Expenditure, selected_project)
        st.markdown("---")

        df_grouped = df_selection.groupby('head')[['Expenditure', 'Released Budget']].sum().reset_index()

        # Plot Bars
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

        st.pyplot(plt)

    # Option 2: Projects with Expenditure < 70%
    elif selected_option == "Projects < 70% Expenditure":
        projects_below_70_list = []

        # Iterate through unique project names
        for project_name in df['projectname'].unique():
            project_data = df[df['projectname'] == project_name]
            Release = project_data['Released Budget'].sum()
            Expenditure = project_data['Expenditure'].sum()

            if Expenditure < 0.7 * Release:
                percentage = round((Expenditure / Release) * 100)
                projects_below_70_list.append({
                    'ProjectName': project_name,
                    'Release': Release / 1000000,  # Convert to millions
                    'Expenditure': Expenditure / 1000000,  # Convert to millions
                    'Percentage': percentage
                })

        projects_below_70_df = pd.DataFrame(projects_below_70_list)

        def format_percentage(val):
            try:
                percentage_value = float(val[:-1])
                if percentage_value < 30:
                    return 'font-weight: bold; color: red'
                else:
                    return 'font-weight: bold; color: black'
            except ValueError:
                return 'font-weight: bold; color: black'

        st.write("Projects with Overall Expenditure Less Than 70%:")
        st.table(projects_below_70_df.style.applymap(format_percentage, subset=['Percentage']).set_table_styles([{'selector': 'th', 'props': [('font-size', '150%')]}]))

    # Option 3: Projects Headwise Expenditure
    elif selected_option == 'Projects Headwise Expenditure':
        projects_below_70_list = []
        headwise_below_70_list = []

        # Iterate through unique project names
        for project_name in df['projectname'].unique():
            project_data = df[df['projectname'] == project_name]
            Release = project_data['Released Budget'].sum()
            Expenditure = project_data['Expenditure'].sum()

            if Expenditure < 0.7 * Release:
                percentage = round((Expenditure / Release) * 100)
                projects_below_70_list.append({
                    'ProjectName': project_name,
                    'Release': Release / 1000000,  # Convert to millions
                    'Expenditure': Expenditure / 1000000,  # Convert to millions
                    'Percentage': percentage
                })

                heads_below_70 = project_data[project_data['Expenditure'] < 0.7 * project_data['Released Budget']]
                if not heads_below_70.empty:
                    headwise_below_70_list.append({
                        'ProjectName': project_name,
                        'Release': Release / 1000000,  # Convert to millions
                        'Heads_Below_70': heads_below_70[['head', 'Released Budget', 'Expenditure']].copy()
                    })

        projects_below_70_df = pd.DataFrame(projects_below_70_list)
        projects_below_70_df_display = projects_below_70_df.copy()
        projects_below_70_df_display['Release'] = projects_below_70_df['Release'].apply(lambda x: f"{x:.2f} ")
        projects_below_70_df_display['Expenditure'] = projects_below_70_df['Expenditure'].apply(lambda x: f"{x:.2f} ")
        projects_below_70_df_display['Percentage'] = projects_below_70_df['Percentage'].astype(str) + '%'

        st.write("Headwise Expenditure Below 70% for Each Project:")

        for index, row in enumerate(headwise_below_70_list):
            expander = st.expander(f"Project: {row['ProjectName']}")
            expander.write(f"Total Release: {row['Release']:.2f} million")

            if 'Released Budget' in row['Heads_Below_70'].columns and 'Expenditure' in row['Heads_Below_70'].columns:
                heads_table = row['Heads_Below_70']
                heads_table['Expenditure Percentage'] = (heads_table['Expenditure'] / heads_table['Released Budget']) * 100
                heads_table_style = heads_table.style.applymap(
                    lambda x: 'background-color: #FFC8C8' if pd.notna(x) and x < 50 else '',
                    subset=['Expenditure Percentage']
                ).format({'Expenditure Percentage': '{:.2f}%'})

                expander.write(heads_table_style)

if __name__ == "__main__":
    app()
