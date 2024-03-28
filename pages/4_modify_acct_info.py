import streamlit as st
import pandas as pd

if 'aid_legit' not in session_state:
   st.session_state('aid_legit')=False
if 'al_legit' not in session_state:
   st.session_state('al_legit')=False

def validate_acct_loc(acct_loc):
   if len(acct_loc) < 7 or len(acct_loc) > 8:
      st.write("The ACCOUNT LOCATOR does not seem accurate. Please try again.")
      st.session_state('aid_legit')=False
   else: 
      st.write("The ACCOUNT LOCATOR entered seems legit.")
      st.session_state('aid_legit')=True
      
def validate_acct_id(acct_id):
   if len(acct_id) < 15 or len(acct_id) > 18:
      st.write("The ACCOUNT ID you entered does not seem accurate. Please try again.")
      st.session_state('al_legit')=False
   elif acct_id.find(".") < 0:
      st.write("The ACCOUNT ID does not seem accurate. Please try again.")
      st.session_state('al_legit')=False
   else: 
      st.write("The ACCOUNT ID entered seems legit.")
      st.session_state('al_legit')=True

cnx=st.connection("snowflake")
session = cnx.session()

def workshop_chosen_changed():
   st.session_state['editing_workshop']=False
   st.session_state['submit_new_account_info'] = False
   st.session_state['account_locator'] = ''
   st.session_state['account_identifier'] = ''
   st.session_state('aid_legit')=False
   st.session_state('al_legit')=False

# drop list with option button for editing
if st.session_state.auth_status == 'authed':
   st.session_state.workshop_choice =  st.selectbox("Choose Workshop/Badge want to enter/edit account info for:"
                                                      , ('Badge 1: DWW', 'Badge 2: CMCW', 'Badge 3: DABW', 'Badge 4: DLKW', 'Badge 5: DNGW')
                                                      , on_change = workshop_chosen_changed()
                                                      , key=1)
    
   #get_workshop_info()
   with st.form("edit_acct_info"):
      st.markdown("**Edit Trial Account Info for " + st.session_state.workshop_choice + "**")
      edited_acct_id = st.text_input("Enter Your Account Identifier as found in your Snowflake Account:", st.session_state.account_identifier)
      edited_acct_loc = st.text_input("Enter Your Account Locator as found in your Snowflake Account:", st.session_state.account_locator)
      submit_button = st.form_submit_button("Update Trial Account Info")

      if submit_button: 
         validate_acct_id(edited_acct_id)
         validate_acct_loc(edited_acct_loc)

         st.session_state.edited_acct_id = edited_acct_id
         st.session_state.edited_acct_loc = edited_acct_loc



else: # not authed
         st.markdown(":red[Please sign in using your UNI_ID and UUID in the section above.]")  





