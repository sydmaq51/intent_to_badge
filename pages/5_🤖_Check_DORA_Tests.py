import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()

all_my_tests_df = session.table("AMAZING.APP.ALL_MY_TESTS").filter(col("uni_id")== '0053r00000ANXAgAAP')
st.dataframe(all_my_tests_df)
