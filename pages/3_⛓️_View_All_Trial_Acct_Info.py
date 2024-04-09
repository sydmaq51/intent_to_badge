import streamlit as st
import pandas as pd

cnx=st.connection("snowflake")
session = cnx.session()

def get_user_workshop_acct_info():
   # get a table of all the entries this user has made
   workshops_sql =  (f"select award_desc, organization_id ||\'.\'|| account_name as ACCOUNT_IDENTIFIER, account_locator " 
                     f"from AMAZING.APP.USER_ACCOUNT_INFO_BY_COURSE where type = 'MAIN' and UNI_ID=trim('{st.session_state.uni_id}') " 
                     f"and UNI_UUID=trim('{st.session_state.uni_uuid}')") 
   workshops_df = session.sql(workshops_sql)
   workshops_results = workshops_df.to_pandas()
   workshops_rows = workshops_results.shape[0]

   # show the entries
   if workshops_rows>=1:
       st.write("You have entered account info for the following badge workshops:")
       st.dataframe(workshops_results)
   else:
      st.write("You have not registered for any badges. Go to the next page to enter info about your Snowflake Trial Account.")

cnx=st.connection("snowflake")
session = cnx.session()

st.subheader("View Trial Account Information You've Entered")

if st.session_state.auth_status == 'authed':
   # display of info for all registered workshops
   get_user_workshop_acct_info()
   #st.dataframe(workshops_results)
   st.markdown(":red[Both Acct ID and Acct Locator are required and can be added on the next page.]")
else:
   st.markdown(":red[Please sign in using your UNI_ID and UUID in the sidebar of the homepage.]")


