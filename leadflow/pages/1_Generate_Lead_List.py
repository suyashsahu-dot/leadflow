import streamlit as st
import pandas as pd
import googlemaps
from datetime import datetime

API_KEY = "<Your google cloud console API key>"
gmaps = googlemaps.Client(key=API_KEY)

st.title("Generate Lead List")

st.subheader("Ideal Customer Profile (ICP)")
industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Retail", "Education", "Law firm"])
location = st.text_input("Location (e.g., New York, USA)")
num_leads = st.number_input("Number of Leads", min_value=1, max_value=100, value=10)

if st.button("Generate Lead List"):
    if location:
        places_result = gmaps.places(query=f"{industry} in {location}")

        leads = []
        for place in places_result.get('results', [])[:num_leads]:
            name = place.get('name')
            address = place.get('formatted_address')
            phone_number = place.get('formatted_phone_number', 'N/A')
            website = place.get('website', 'N/A')
            leads.append({
                "Name": name,
                "Address": address,
                "Phone Number": phone_number,
                "Website": website
            })

        df = pd.DataFrame(leads)

        st.write("Generated Leads:")
        st.dataframe(df)

        excel_file = "lead_list.xlsx"
        df.to_excel(excel_file, index=False)
        st.download_button(
            label="Download Lead List as Excel",
            data=open(excel_file, "rb").read(),
            file_name=excel_file,
            mime="application/vnd.ms-excel"
        )
    else:
        st.error("Please enter a valid location.")