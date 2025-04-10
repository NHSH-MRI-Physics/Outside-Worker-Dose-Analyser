import streamlit as st


st.title("Boardwide Dose Statistics")

if st.session_state["uploaded_data"] == None:
    st.warning("Please upload a file first from the Staff Dose Collater File Selection Page.")
    st.stop()


st.write(st.session_state["uploaded_data"].staff["test@nhs.com"].name)