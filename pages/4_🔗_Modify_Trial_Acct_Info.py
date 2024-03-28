import streamlit as st
import pandas as pd

if 'aid_legit' not in st.session_state:
   st.session_state.aid_legit = False
if 'al_legit' not in st.session_state:
   st.session_state.al_legit = False

def validate_acct_loc(acct_loc):
   if len(acct_loc) < 7 or len(acct_loc) > 8:
      st.write("The ACCOUNT LOCATOR does not seem accurate. Please try again.")
      st.session_state.aid_legit = False
   else: 
      st.write("The ACCOUNT LOCATOR entered seems legit.")
      st.session_state.aid_legit = True
      
def validate_acct_id(acct_id):
   if len(acct_id) < 15 or len(acct_id) > 18:
      st.write("The ACCOUNT ID you entered does not seem accurate. Please try again.")
      st.session_state.al_legit = False
   elif acct_id.find(".") < 0:
      st.write("The ACCOUNT ID does not seem accurate. Please try again.")
      st.session_state.al_legit = False
   else: 
      st.write("The ACCOUNT ID entered seems legit.")
      st.session_state.al_legit = True

cnx=st.connection("snowflake")
session = cnx.session()

def get_workshop_info():   
   st.session_state.aid_legit = False
   st.session_state.al_legit = False
   st.session_state.new_record = False
   for_edits_sql =  (f"select organization_id ||\'.\'|| account_name as ACCOUNT_IDENTIFIER, account_locator " 
                   f"from AMAZING.APP.USER_ACCOUNT_INFO_BY_COURSE where type = 'MAIN' "
                   f"and UNI_ID= trim('{st.session_state.uni_id}') and UNI_UUID=trim('{st.session_state.uni_uuid}') " 
                   f"and award_desc='{st.session_state.workshop_choice}'")
   # st.write(for_edits_sql)
   for_edits_df = session.sql(for_edits_sql)
   for_edits_pd_df = for_edits_df.to_pandas()
   for_edits_pd_df_rows = for_edits_pd_df.shape[0]

   # if the data row doesnt exist just seed it with blanks
   if for_edits_pd_df_rows == 1:
      if for_edits_pd_df['ACCOUNT_LOCATOR'].iloc[0] is not None:
         st.session_state['account_locator'] = for_edits_pd_df['ACCOUNT_LOCATOR'].iloc[0] 
      if for_edits_pd_df['ACCOUNT_IDENTIFIER'].iloc[0] is not None:
         st.session_state['account_identifier'] = for_edits_pd_df['ACCOUNT_IDENTIFIER'].iloc[0]
      st.session_state.new_record='False'   
   elif for_edits_pd_df_rows == 0:
      st.write('You have not previously entered account information for this workshop. Please add the information below.')
       st.session_state.new_record='True'
   else:
      st.write("there should only be 1 or zero rows.") 


st.subheader("Add or Edit Trial Account Rows for Workshops")
# drop list with option button for editing
if st.session_state.auth_status == 'authed':
   with st.form("select a workshop"):
      st.session_state.workshop_choice =  st.selectbox("Choose Workshop/Badge want to enter/edit account info for:"
                                                      , ('Badge 1: DWW', 'Badge 2: CMCW', 'Badge 3: DABW', 'Badge 4: DLKW', 'Badge 5: DNGW')
                                                      , key=1)
      load_or_create = st.form_submit_button("Load or Create Workshop Acct Info")
      
      if load_or_create:
         get_workshop_info()
   
   with st.form("edit_acct_info"):
      st.markdown("**Edit Trial Account Info for " + st.session_state.workshop_choice + "**")
      edited_acct_id = st.text_input("Enter Your Account Identifier as found in your Snowflake Account:", st.session_state.account_identifier)
      edited_acct_loc = st.text_input("Enter Your Account Locator as found in your Snowflake Account:", st.session_state.account_locator)
      submit_button = st.form_submit_button("Update Trial Account Info")

      if submit_button: 
         validate_acct_id(edited_acct_id)
         validate_acct_loc(edited_acct_loc)
         if st.session_state.ai_legit == True and st.session_state.aid_legit==True:
            st.session_state.edited_acct_id = edited_acct_id
            st.session_state.edited_acct_loc = edited_acct_loc
            session.call(AMAZING.APP.ADD_ACCT_INFO_SP, st.session_state.new_record, st.session_state.uni_id, st.session_state.uni_uuid, st.session_state.workshop_choice, edited_acct_id, edited_acct_loc, 'MAIN')
            st.write("Maybe a row was added?")


else: # not authed
         st.markdown(":red[Please sign in using your UNI_ID and UUID in the section above.]")  





