import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import matplotlib.patches as patches
import plotly.graph_objects as go
from matplotlib.patches import Arc
import testpage as tp

df = pd.read_excel(
        io="psdp.xlsx",
        engine='openpyxl',
        sheet_name='Umbrella',
        skiprows=0,
        usecols='A:F',
        nrows=50000,
    )


def app():

 
 st.write("Testing page ")