import streamlit as st
import pandas as pd


def workshop_chosen_changed():
   st.session_state['editing_workshop']=False
   st.session_state['submit_new_account_info'] = False
   st.session_state['account_locator'] = ''
   st.session_state['account_identifier'] = ''

# drop list with option button for editing
st.session_state.workshop_choice =  st.selectbox("Choose Workshop/Badge want to enter/edit account info for:"
                                                      , ('Badge 1: DWW', 'Badge 2: CMCW', 'Badge 3: DABW', 'Badge 4: DLKW', 'Badge 5: DNGW')
                                                      , on_change = workshop_chosen_changed()
                                                      , key=1)
workshop_to_view = st.button("Create/Edit Acct Info for Chosen Workshop") 

if workshop_to_view: #button clicked
      st.session_state.editing_workshop=True

##******* gets sub form to show up ********
# clicking above button makes this appear by setting property to True
if st.session_state.editing_workshop==True:    
   get_workshop_info()
   with st.form("edit_acct_info"):
      st.markdown("**Edit Trial Account Info for " + st.session_state.workshop_choice + "**")
      edited_acct_id = st.text_input("Enter Your Account Identifier as found in your Snowflake Account:", st.session_state.account_identifier)
      edited_acct_loc = st.text_input("Enter Your Account Locator as found in your Snowflake Account:", st.session_state.account_locator)
      submit_button = st.form_submit_button("Update Trial Account Info")

      if submit_button: 
         st.session_state.submit_new_acct_info=True
         st.session_state.edited_acct_id = edited_acct_id
         st.session_state.edited_acct_loc = edited_acct_loc


if st.session_state.submit_new_acct_info==True: 
   #st.write(f"You submited ACCOUNT IDENTIFIER {st.session_state.edited_acct_id} and ACCOUNT LOCATOR {st.session_state.edited_acct_loc} for Workshop {st.session_state.workshop_choice}")
   st.write("under the if")

   st.write('Outside the form')
   st.write("EDITED ACCOUNT ID IS: "+ st.session_state.edited_acct_id)

   else: # not authed
         st.markdown(":red[Please sign in using your UNI_ID and UUID in the section above.]")  





