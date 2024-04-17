import streamlit as st
import pandas as pd
import time

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
      st.write(":red[The ACCOUNT ID you entered does not seem accurate. Please try again.]")
      st.session_state.al_legit = False
   elif acct_id.find(".") < 0:
      st.markdown(":red[The ACCOUNT ID does not seem accurate. Please try again.]")
      st.session_state.al_legit = False
   else: 
      st.markdown(":green[The ACCOUNT ID entered seems legit.]")
      st.session_state.al_legit = True

def validate_acme(acme_acct_loc):
   if acme_acct_loc == 'ACME':
      st.markdown(':red[The ACCOUNT LOCATOR is not ACME, that is the Account Name. Please look again.]')
   elif len(acme_acct_loc) < 7 or len(acct_loc) > 8:
      st.write(":red[The ACME ACCOUNT LOCATOR does not seem accurate. Please try again.]")
      st.session_state.acme_legit = False
   else: 
      st.write(":green[The ACME ACCOUNT LOCATOR you entered seems legit.]")
      st.session_state.acme_legit = True


def get_workshop_info():   
   st.session_state.account_locator = ''
   st.session_state.account_identifier = ''
   st.session_state.aid_legit = False
   st.session_state.al_legit = False
   st.session_state.new_record = 'False'
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
      st.session_state.new_record= False
      if for_edits_pd_df['ACCOUNT_LOCATOR'].iloc[0] is not None:
         st.session_state['account_locator'] = for_edits_pd_df['ACCOUNT_LOCATOR'].iloc[0] 
      if for_edits_pd_df['ACCOUNT_IDENTIFIER'].iloc[0] is not None:
         st.session_state['account_identifier'] = for_edits_pd_df['ACCOUNT_IDENTIFIER'].iloc[0]      
   elif for_edits_pd_df_rows == 0:
      st.write('You have not previously entered account information for this workshop. Please add the information below.')
      st.session_state.new_record= True
      st.session_state.edited_acme = '' # if a new record can't be acme so acme is blank
   else:
      st.write("there should only be 1 or zero rows.") 

cnx=st.connection("snowflake")
session = cnx.session()

st.subheader(":link: Add or Edit Trial Account Rows for Workshops")
# drop list with option button for editing
if st.session_state.auth_status == 'authed':
   with st.form("select a workshop"):
      st.session_state.subform_toggle = False   #subform is open - not disabled
      st.session_state.workshop_choice =  st.selectbox("Choose Workshop/Badge want to enter/edit account info for:"
                                                      , ('<Choose a Workshop>','Badge 1: DWW', 'Badge 2: CMCW', 'Badge 3: DABW', 'Badge 4: DLKW', 'Badge 5: DNGW')
                                                      , key=1)
      load_or_create = st.form_submit_button("Load or Create Workshop Acct Info")
      
      if load_or_create:
         if st.session_state.workshop_choice == '<Choose a Workshop>':
            st.session_state.workshop_choice = ':red[NO WORKSHOP CHOSEN]'
            st.markdown(":red[Please choose a workskhop from the list before clicking the button.]")
            st.session_state.account_locator = ''
            st.session_state.account_identifier = ''
            st.session_state.subform_toggle = True #subform is disabled
         else:   
            # st.write(st.session_state.workshop_choice)
            st.session_state.subform_toggle= False #subform can be edited
            get_workshop_info()
   
   with st.form("edit_acct_info"):
      st.markdown("**Edit Trial Account Info for " + st.session_state.workshop_choice + "**")
      edited_acct_id = st.text_input("Enter Your Account Identifier as found in your Snowflake Account:", st.session_state.account_identifier, disabled=st.session_state.subform_toggle)
      edited_acct_loc = st.text_input("Enter Your Account Locator as found in your Snowflake Account:", st.session_state.account_locator, disabled=st.session_state.subform_toggle)
      if st.session_state.workshop_choice == 'Badge 2: CMCW' and st.session_state.new_record == False:
         edited_acme = st.text_input("ACME Account Locator:")
      
      submit_button = st.form_submit_button("Update Trial Account Info", disabled=st.session_state.subform_toggle)

      if submit_button: 
         if st.session_state.workshop_choice != '<Choose a Workshop>' and st.session_state.workshop_choice != ':red[NO WORKSHOP CHOSEN]':
            validate_acct_id(edited_acct_id)
            validate_acct_loc(edited_acct_loc)
            if st.session_state.workshop_choice == 'Badge 2: CMCW' and st.session_state.new_record == False:
               validate_acme(edited_acme)    
            if st.session_state.al_legit == True and st.session_state.aid_legit==True:
               st.session_state.edited_acct_id = edited_acct_id
               st.session_state.edited_acct_loc = edited_acct_loc
               st.session_state.edited_acme = edited_acme
               if st.session_state.workshop_choice == 'Badge 2: CMCW':
                  session.call('AMAZING.APP.CMCW_ADD_ACCT_INFO_SP', st.session_state.new_record, st.session_state.uni_id, st.session_state.uni_uuid, st.session_state.workshop_choice, edited_acct_id, edited_acct_loc, edited_acme)
                  # PROCEDURE AMAZING.APP.CMCW_ADD_ACCT_INFO_SP
               else:   
                  session.call('AMAZING.APP.ADD_ACCT_INFO_SP', st.session_state.new_record, st.session_state.uni_id, st.session_state.uni_uuid, st.session_state.workshop_choice, edited_acct_id, edited_acct_loc, 'MAIN')
               st.session_state.account_locator = ''
               st.session_state.account_identifier = ''
               st.success('Snowflake Trial Account Workshop Data Updated', icon='🚀')
               time.sleep(2)
               st.switch_page("pages/3_⛓️_View_All_Trial_Acct_Info.py")

else: # not authed
   st.markdown(":red[Please sign in using your UNI_ID and UUID in the sidebar of the homepage.]")

st.markdown('-------')
st.subheader('How to find your Trial Account Information:')
st.image('https://learn.snowflake.com/asset-v1:snowflake+X+X+type@asset+block@dil_1.png','Finding your Account ID')
st.image('https://learn.snowflake.com/asset-v1:snowflake+X+X+type@asset+block@dil_3.png','Finding your Account Locator')




