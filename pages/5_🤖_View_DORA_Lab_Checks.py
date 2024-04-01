import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()

st.subheader("View ALl DORA Tests You Have Run")
st.write("Click on column headings to sort. Use the drop list to filter the checks to just a single workshop.")
st.write("You can search the table by rolling your cursor over the header and choosing the magnifying lense symbol.")
        

if st.session_state.auth_status == 'authed':
        all_my_tests_df = session.table("AMAZING.APP.ALL_MY_TESTS").filter(col("uni_id")== st.session_state.uni_id)
        all_my_tests_pd_df = all_my_tests_df.to_pandas()
        amt_rows = all_my_tests_pd_df.shape[0]

        workshop_filter = all_my_tests_pd_df['BADGE_ACRO'].unique()
        # step_filter= all_my_tests_pd_df['STEP'].unique()
        # st.dataframe(all_my_tests_pd_df)
        
        if amt_rows > 0:
                mw_choice = st.selectbox("Filter to workshop records for:", workshop_filter)
                # pf_choice = st.selectbox('Pass/Fail Filter:', ('True','False') )                        
                st.markdown("*Please note that if you have only started one workshop, you will only have one choice in the list*") 

                if mw_choice:
                        filtered_df = all_my_tests_pd_df[all_my_tests_df['BADGE_ACRO'].isin(mw_choice)] 
                                         
                        st.dataframe(filtered_df
                                , column_order=["STEP","ACCOUNT_LOCATOR","PASSED", "DORA_TIMESTAMP"]
                                , column_config={ 
                                "STEP": "DORA Check #"
                                ,"ACCOUNT_LOCATOR": "Acct Loc"
                                , "PASSED": "Passed"
                                ,"DORA_TIMESTAMP": "Submission Date/Time"},    
                                hide_index=True,
                                height=1200
                        )

                                        

