import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()

all_my_tests_df = session.table("AMAZING.APP.ALL_MY_TESTS").filter(col("uni_id")== st.session_state.uni_id)
all_my_tests_pd_df = all_my_tests_df.to_pandas()
st.dataframe(all_my_tests_pd_df
             , column_order=["STEP","ACCOUNT_LOCATOR","PASSED", "DORA_TIMESTAMP"]
            , column_config={ 
                        "STEP": "DORA Check #"
                        ,"ACCOUNT_LOCATOR": "Acct Loc"
                        , "PASSED": "Passed"
                        ,"DORA_TIMESTAMP": "Submission Date/Time"
            },    
             hide_index=True
            )

