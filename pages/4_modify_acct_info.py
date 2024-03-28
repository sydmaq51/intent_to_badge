import streamlit as st
import pandas as pd


def workshop_chosen_changed():
   st.session_state['editing_workshop']=False
   st.session_state['submit_new_account_info'] = False
   st.session_state['account_locator'] = ''
   st.session_state['account_identifier'] = ''


