import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()

st.subheader("View All Essentials Badges Earned By Your Uni ID")
st.write("Click on column headings to sort. Use the drop list to filter the checks to just a single workshop.")
st.write("You can search the table of results by rolling your cursor over the header and choosing the magnifying lens symbol.")
        
if st.session_state.auth_status == 'authed':
                all_my_badges_df = session.table("AMAZING.APP.BADGE_LOOKUP").filter(col("uni_id")== st.session_state.uni_id)
                all_my_bdages_pd_df = all_my_tests_df.to_pandas()
                badge_rows = all_my_badges_pd_df.shape[0]
                         
                if badge_rows > 0:                         
                        st.dataframe(all_my_badges_pd_df
                                , column_order=["BADGE_TEMPLATE_NAME","BADGE_URL","UNI_ID","ACCOUNT_LOCATOR","EMAIL","ISSUED_AT"]
                                , column_config={ 
                                "BADGE_TEMPLATE_NAME": "Badge Name"
                                ,"BADGE_URL": "Link to Badge"
                                ,"UNI_ID": "Your UNI ID"
                                ,"ACCOUNT_LOCATOR": "Your Account Locator"
                                ,"EMAIL": "Email on Badge"
                                ,"ISSUED_AT": "Time/Date Issued"                                
                                },    
                                hide_index=True,
                                height=1200
                        )

else: # not authed
   st.markdown(":red[Please sign in using your UNI_ID and UUID in the sidebar of the homepage.]")                                        

