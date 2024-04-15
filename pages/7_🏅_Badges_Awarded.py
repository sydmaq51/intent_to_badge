import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()

st.subheader(":sports_medal: View All Essentials Badges Earned By Your Uni ID")
st.write("Badges issued in the last 20 minutes may not yet be visible.")
st.write("If you do not see your badge here, please check the badge requirements page.")
        
if st.session_state.auth_status == 'authed':
                all_my_badges_df = session.table("AMAZING.APP.BADGE_LOOKUP").filter(col("uni_id")== st.session_state.uni_id)
                all_my_badges_pd_df = all_my_badges_df.to_pandas()
                # st.dataframe(all_my_badges_pd_df)
                badge_rows = all_my_badges_pd_df.shape[0]
                         
                if badge_rows > 0:                         
                        st.dataframe(all_my_badges_pd_df
                                , column_order=["AWARD_ACRONYM","BADGE_URL","EMAIL","ISSUED_AT"]
                                , column_config={ 
                                "AWARD_ACRONYM": "Badge"       
                                ,"BADGE_URL": st.column_config.LinkColumn("Link to Badge")        
                                ,"EMAIL": "Email on Badge"
                                ,"ISSUED_AT": "Time/Date Issued"                                
                                },    
                                hide_index=True,
                                height=200
                        )
                else:
                 st.markdown(":red[Sorry, we do not show that you have earned any badges, yet]")

else: # not authed
   st.markdown(":red[Please sign in using your UNI_ID and UUID in the sidebar of the homepage.]")                                        

