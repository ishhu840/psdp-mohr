import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

# Load your data
df = pd.read_excel(
    io="psdp.xlsx",
    engine='openpyxl',
    sheet_name='Umbrella',
    skiprows=0,
    usecols=['Project Name', 'Executing Agency', 'FY-2023-24 Budget', 'FY-2024-25 Budget', 'Total Budget', 'Released'],
    nrows=50000,
)

def app():
    # Add a title to your app
    st.title("Umbrella (8) Projects Funding Overview")

    # Create a color mapping for Executing Agency
    unique_agencies = df['Executing Agency'].unique()
    color_mapping = {agency: to_rgba(plt.cm.Paired(i)) for i, agency in enumerate(unique_agencies)}

    # Create a pie chart
    fig, ax = plt.subplots(figsize=(16, 12))  # Increase the figsize for a larger chart
    project_names = df['Project Name']
    total_budgets = df['Total Budget']
    released = df['Released']  # Released column
    exec_agency = df['Executing Agency']  # Executing Agency column

    # Calculate percentages
    percentages = total_budgets / total_budgets.sum()

    # Adjust the explode list to increase the gap for projects with low percentages
    explode = [0.2 if p < 0.1 else 0.05 for p in percentages]

    wedges, _, autotexts = ax.pie(
        total_budgets,
        labels=None,  # Remove labels from the pie chart
        autopct=lambda p: f'{p:.1f}%',  # Display percentage
        startangle=90,
        pctdistance=0.85,
        explode=explode,  # Adjust the gap size
        colors=[color_mapping[agency] for agency in exec_agency]  # Use the color mapping
    )  # Add percentages and gaps, but no labels

    # Customize font size for percentages
    for autotext in autotexts:
        autotext.set_fontsize(14)  # Adjust the font size for percentages
        autotext.set_position((1.1 * autotext.get_position()[0], autotext.get_position()[1]))


    # Add project names with color codes at the bottom
    legend_labels_project = [plt.Line2D([0], [0], marker='', color=color_mapping[agency], label=name, 
                                        markersize=14, markerfacecolor=color_mapping[agency], linewidth=12) 
                             for name, agency in zip(project_names, exec_agency)]

    # Create legend for Executing Agency
    legend_labels_exec_agency = [plt.Line2D([0], [0], marker='o', color='w', label=agency, 
                                            markersize=16, markerfacecolor=color_mapping[agency], linewidth=12) 
                                 for agency in unique_agencies]

    # Combine the legends
    legend_labels_combined = legend_labels_project + legend_labels_exec_agency
    
    plt.legend(handles=legend_labels_combined, 
               title="Projects Name & Executing Agency", 
               loc="lower center", 
               bbox_to_anchor=(0.5, -0.25), 
               ncol=2)
    
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Display the pie chart at the start
    st.pyplot(fig)

    # Display the data table below the pie chart
    st.write("Project Funding Details")
    st.write(df)

# Run your Streamlit app
if __name__ == '__main__':
    app()
