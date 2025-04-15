import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
import FileAnalysis

st.set_page_config(
    page_title="File Selection",
    page_icon="📊"
)

st.title("Outside Worker Dose Analyser")

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

    if st.session_state["uploaded_data"].warningMessages:
        warnings_df = pd.DataFrame(st.session_state["uploaded_data"].warningMessages, columns=["Warnings"])
        styled_df = warnings_df.style.set_properties(**{'text-align': 'center'}).set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
        st.markdown(styled_df.hide(axis="index").to_html(), unsafe_allow_html=True)


elif st.session_state["uploaded_file"] is not None:
    st.write("Data loaded successfully.")   
    st.write("File already uploaded:", st.session_state["uploaded_file"].name)
    
    if st.session_state["uploaded_data"].warningMessages:
        warnings_df = pd.DataFrame(st.session_state["uploaded_data"].warningMessages, columns=["Warnings"])
        styled_df = warnings_df.style.set_properties(**{'text-align': 'center'}).set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
        st.markdown(styled_df.hide(axis="index").to_html(), unsafe_allow_html=True)


