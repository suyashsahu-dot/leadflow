import streamlit as st

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Generate Lead List",
    "Outreach and Follow up",
    "Generate Invoice & Contracts",
    "Tax Management"
])

if page == "Generate Lead List":
    st.switch_page("pages/1_Generate_Lead_List.py")
elif page == "Outreach and Follow up":
    st.switch_page("pages/2_Outreach_and_Follow_up.py")
elif page == "Generate Invoice & Contracts":
    st.switch_page("pages/3_Generate_Invoice_&_Contracts.py")
elif page == "Tax Management":
    st.switch_page("pages/4_Tax_Management.py")