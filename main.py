import streamlit as st
st.set_page_config(page_title="PSDP - 2023-24", page_icon=":bar_chart:", layout="wide")

from streamlit_option_menu import option_menu

import page1, page2, page3, page4 

# Set Streamlit page configuration

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='PSDP (FY 2023-24) ',
                options=['Projects Detail', 'Individual Project','Umbrella Project'],
                icons=['info-circle', 'person-circle', 'umbrella', 'bar_chart'],
                menu_icon='envelope-fill',
                default_index=0,  # Set default_index to 0 to select "Page1" by default
                styles={
                    "container": {"padding": "5!important", "background-color": 'white'},
                    "icon": {"color": "#52BE80", "font-size": "30px"},
                    "nav-link": {"color": "green", "font-size": "25px", "text-align": "left", "margin": "0px",
                                 "--hover-color": "#D5F5E3"},
                    "nav-link-selected": {"background-color": "#ABEBC6"},
                }
            )
        st.cache_resource.clear()

        if app == "Projects Detail":
            page1.app()
        if app == "Individual Project":
            page2.app()
        if app == "Page4":
            page3.app()
        if app == "Umbrella Project":
            page4.app()
      
if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.run()
