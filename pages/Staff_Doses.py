import streamlit as st


st.title("Staff Dose Statistics")

if st.session_state["uploaded_data"] == None:
    st.warning("Please upload a file first from the Staff Dose Collater File Selection Page.")
    st.stop()
