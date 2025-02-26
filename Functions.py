import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

larger_font_size = 60

df = pd.read_excel(
    io="psdp.xlsx",
    engine='openpyxl',
    sheet_name='ProjectDeatil',
    skiprows=0,
    usecols='A:G',
    nrows=50000,
)

css = """
        <style>
        .custom-info-box {
            background-color: #F0F8FF; /* Light sky blue color */
            border: 1px solid #1E90FF; /* Blue border */
            padding: 5px;
            border-radius: 5px;
            font-size: 20px; /* Increase font size */
            font-weight: bold; /* Make the font bold */

            
        }
        
          .custom-info-box1 {
            background-color: #ffd9b3; /* Light sky blue color */
            border: 1px solid #1E90FF; /* Blue border */
            padding: 5px;
            border-radius: 5px;
            font-size: 20px; /* Increase font size */
            font-weight: bold; /* Make the font bold */

            
        }
        
        .custom-info-box2 {
            background-color: #c2f0c2; /* Light sky blue color */
            border: 1px solid #1E90FF; /* Blue border */
            padding: 5px;
            border-radius: 5px;
            font-size: 20px; /* Increase font size */
            font-weight: bold; /* Make the font bold */

            
        }
        </style>
    """

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

def projectInfoCard(total_budget,released_budget,total_expenditure):    

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
            st.markdown(
                """
                <div style="background-color: #e6f7ff; padding: 10px; border-radius: 5px;">
                    <span style="font-size: 20px; font-weight: bold;">Total Budget</span>
                    <br>
                    <span style="font-size: 24px; color: #0066cc;">FY (2024-25)</span>
                    <br>
                    <span style="font-size: 36px;">{:.2f} m</span>
                </div>
                """.format(total_budget),
                unsafe_allow_html=True,
            )

    with middle_column:
            st.markdown(
                """
                <div style="background-color: #c2f0c2; padding: 10px; border-radius: 5px;">
                    <span style="font-size: 20px; font-weight: bold;">Released Budget</span>
                    <br>
                    <span style="font-size: 24px; color: #009900;">Q1 + Q2 + Q3</span>
                    <br>
                    <span style="font-size: 36px;">{:.2f} m</span>
                </div>
                """.format(released_budget),
                unsafe_allow_html=True,
            )

    with right_column:
            st.markdown(
                """
                <div style="background-color: #ffd9b3; padding: 10px; border-radius: 5px;">
                    <span style="font-size: 20px; font-weight: bold;">Expenditure</span>
                    <br>
                    <span style="font-size: 24px; color: #ff6600;">July-Till Date</span>
                    <br>
                    <span style="font-size: 36px;">{:.2f} m</span>
                </div>
                """.format(total_expenditure),
                unsafe_allow_html=True,

            )

def circulechart(total_budget,released_budget,total_expenditure,project_name):
   
    left_column, right_column = st.columns(2)

    with left_column:
        # Define the percentage ranges
        range_1 = total_budget * 0.15
        range_2 = total_budget * 0.20
        range_3 = total_budget * 0.25
        range_4 = total_budget * 0.40

        # Create the figure
        fig = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=released_budget,  # Initial value
            mode="gauge+number+delta",
            title={'text': "Quarter Wise Release & Expenditure (FY : 2024-25)"},
            delta={'reference': total_expenditure},
            gauge={'axis': {'range': [0, total_budget], 'tickwidth': 1, 'tickcolor': "black", 'tickvals': [0, range_1 , range_1 + range_2, range_1 + range_2 + range_3, total_budget]},
                'bar': {'color': "Green"},
                'steps': [
                    {'range': [0, range_1], 'color': "DarkTurquoise" },
                    {'range': [range_1, range_1 + range_2], 'color': "MediumTurquoise"},
                    {'range': [range_1 + range_2, range_1 + range_2 + range_3], 'color': "Turquoise"},
                    {'range': [range_1 + range_2 + range_3, total_budget], 'color': "PaleTurquoise"}],
                'threshold': {'line': {'color': "brown", 'width': 4}, 'thickness': 0.75 ,'value': total_expenditure}}))
            
        # Update the chart with dynamic values
        fig.update_traces(value=released_budget, delta={'reference': total_expenditure})
       # fig.update_layout(title_text=f" Total Budget (2024-25): {total_budget}, Released: {released_budget},  Expenditure: {total_expenditure}")
        #fig.update_layout(title_text=f"Quater Wise Release  - Q1 =  {range_1} (15%) , Q2 =  {range_2} (20%), Q3 =  {range_3} (25%) , Q4 =  {range_4} (40%)")
       
        # Show the figure with a smaller size
        st.plotly_chart(fig, use_container_width=True, height=300)
        
    with right_column:
        
        # Filter the DataFrame based on 'Project Name'
        df_selection = df[df["Project Name"] == project_name]

        # Load custom CSS
        st.markdown(css, unsafe_allow_html=True)

        # Display the selected project name
        st.markdown(f"<div class='custom-info-box' style='text-align: center;'>Project Chronology</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-info-box'>Project Name: {project_name}</div>", unsafe_allow_html=True)

        # Check and display 'Start Date'
        if 'Start Date' in df_selection:
            df_selection['Start Date'] = df_selection['Start Date'].fillna("N/A").astype(str)
            st.markdown(f"<div class='custom-info-box'>Start Date : {df_selection['Start Date'].iloc[0]}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='custom-info-box'>Start Date not available</div>", unsafe_allow_html=True)

        # Check and display 'End Date'
        if 'End Date' in df_selection:
            df_selection['End Date'] = df_selection['End Date'].fillna("N/A").astype(str)
            st.markdown(f"<div class='custom-info-box'>End Date : {df_selection['End Date'].iloc[0]}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='custom-info-box'>End Date not available</div>", unsafe_allow_html=True)

       # Check if 'Total Extension' column exists
        if 'Total Extension' in df_selection:
        # Get the 'Total Extension' value as a string
            total_extension = str(df_selection['Total Extension'].iloc[0])
            st.markdown(f"<div class='custom-info-box'>Number of  Extension : {int(total_extension)}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='custom-info-box'>Total Extension not available</div>", unsafe_allow_html=True)
        
        if 'Actual Budget' in df_selection:
    # Get the 'Actual Budget' value as a string
    
            project_budget = df_selection['Actual Budget'].iloc[0]
        
            if not pd.isna(project_budget):
                # Convert to integer if it's not NaN
                project_budget = float(project_budget)
                st.markdown(f"<div class='custom-info-box2'>Project Budget : {project_budget} M</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='custom-info-box'>Project Budget not available</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='custom-info-box'>Project Budget not available</div>", unsafe_allow_html=True)

        
        if 'Total Expenditure' in df_selection:
    # Get the 'Total Expenditure' value as a string
    
            project_totalexp = df_selection['Total Expenditure'].iloc[0]
        
            if not pd.isna(project_totalexp):
                # Convert to integer if it's not NaN
                project_totalexp = float(project_totalexp)
                st.markdown(f"<div class='custom-info-box1'>Total Expenditure Till-Date : {(project_totalexp + total_expenditure):.3f} M</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='custom-info-box1'>Total Expenditure in % Till-Date : {((project_totalexp + total_expenditure)/project_budget * 100):.2f}  %</div>", unsafe_allow_html=True)

            else:
                st.markdown("<div class='custom-info-box'>Total Expenditure Till-Date not available</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='custom-info-box'>Total Expenditure Till-Date not available</div>", unsafe_allow_html=True)


        if 'Duration' in df_selection:
        # Get the 'Total Extension' value as a string
            total_duration = str(df_selection['Duration'].iloc[0])
            st.markdown(f"<div class='custom-info-box'>Project Duration : {int(total_duration)} Years</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='custom-info-box'>Total Duration not available</div>", unsafe_allow_html=True)
        
        
             
def printinfo(total_budget,released_budget,total_expenditure):
    
    left_column, middle_column, right_column = st.columns(3)

        # Display the styled boxes in each column
    with left_column:
                st.markdown(styled_box("📌", "Total Budget", f"{total_budget} M"), unsafe_allow_html=True)

    with middle_column:
                st.markdown(styled_box("📈", "Released Budget", f"{released_budget} M"), unsafe_allow_html=True)

    with right_column:
                st.markdown(styled_box("📉", "Expenditure", f"{total_expenditure} M"), unsafe_allow_html=True) 
