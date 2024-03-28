import streamlit as st
import pandas as pd

st.set_page_config(
   page_title="Snow-Amazing Badge Mgmt",
   page_icon= "🏆"
)

def initialize_user_info():
   # session is open but not authed
   st.session_state['auth_status'] = 'not_authed'
   # all profile fields get set back to nothing
   st.session_state['given_name'] = ''
   st.session_state['middle_name'] = ''
   st.session_state['family_name'] = ''
   st.session_state['badge_email'] = ''
   st.session_state['display_name'] = ''
   # workshop/account fields are set back to nothing 
   st.session_state['workshop_choice'] = '' 
   st.session_state['account_locator'] = ''
   st.session_state['account_identifier'] = ''
   st.session_state['submit_new_account_info'] = False


with st.sidebar:
   st.sidebar.header("User")
   uni_id = st.text_input('Enter your learn.snowflake.com UNI ID:')
   uni_uuid = st.text_input('Enter the secret UUID displayed on the DORA is Listening Page of any Workshop:')
   find_my_uni_record = st.button("Find my UNI User Info")

# Page Header
st.header('Are You Snow-A-Mazing?')
st.write('Welcome to the learn.snowflake.com Workshop Badge Management app!')
st.write('Using this app you can manage your badge name and email and you can view your results.')


if find_my_uni_record:
   # reset all session vars
   initialize_user_info()

   # Set uni_id and key to entries on form
   st.session_state['uni_id'] = uni_id
   st.session_state['uni_uuid'] = uni_uuid

   # this will query the db and if finds a match will populate profile vars
   get_user_profile_info()

