import streamlit as st
import pandas as pd

cnx=st.connection("snowflake")
session = cnx.session()

all_my_tests_df = session.table("AMAZING.APP.ALL_MY_TESTS").filter(col("uni_id")== st.session_state.uni_id)
st.dataframe(all_my_tests_df)
