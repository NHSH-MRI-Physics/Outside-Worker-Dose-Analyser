import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
import FileAnalysis

st.title("Outside Worker Dose Collater")

if "uploaded_data" not in st.session_state:
    st.session_state["uploaded_data"] = None

if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None


uploaded_file = st.file_uploader(
    "Choose an Excel file", type=["xlsx", "xls"]
)

if uploaded_file is not None:
    st.session_state["uploaded_file"] = uploaded_file
    st.session_state["uploaded_data"] = FileAnalysis.LoadedData(uploaded_file)
    st.write("Data loaded successfully.")   
elif st.session_state["uploaded_file"] is not None:
    st.write("Data loaded successfully.")   
    st.write("File already uploaded:", st.session_state["uploaded_file"].name)

