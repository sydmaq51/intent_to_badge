import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

if 'submit_new_acct_info' not in st.session_state:
   st.session_state.submit_new_acct_info = False
   
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

def get_user_profile_info():
   #start over with authentication and populating vars
   this_user_sql =  (f"select badge_given_name, badge_middle_name, badge_family_name, display_name, badge_email "
                     f"from UNI_USER_BADGENAME_BADGEEMAIL where UNI_ID=trim('{st.session_state.uni_id}') "
                     f"and UNI_UUID=trim('{st.session_state.uni_uuid}')")
   this_user_df = session.sql(this_user_sql)
   user_results_pd_df = this_user_df.to_pandas()                          
   user_rows = user_results_pd_df.shape[0]

   if user_rows>=1:
      # if at least one row was found then the key must have been correct so we consider the user authorized
      st.session_state['auth_status'] = 'authed'
       
      # 1 row found means the UNI_ID is legit and can be used to look up other information
      # all user vars need to be checked to make sure they aren't empty before we set session vars
      
      if user_results_pd_df['BADGE_GIVEN_NAME'].iloc[0] is not None:
         st.session_state['given_name'] = user_results_pd_df['BADGE_GIVEN_NAME'].iloc[0]
      if user_results_pd_df['BADGE_MIDDLE_NAME'].iloc[0] is not None:    
         st.session_state['middle_name'] = user_results_pd_df['BADGE_MIDDLE_NAME'].iloc[0]
      if user_results_pd_df['BADGE_FAMILY_NAME'].iloc[0] is not None:    
         st.session_state['family_name'] = user_results_pd_df['BADGE_FAMILY_NAME'].iloc[0]
      if user_results_pd_df['BADGE_EMAIL'].iloc[0] is not None:
         st.session_state['badge_email'] = user_results_pd_df['BADGE_EMAIL'].iloc[0]  
      if user_results_pd_df['DISPLAY_NAME'].iloc[0] is not None:
         st.session_state['display_name'] = user_results_pd_df['DISPLAY_NAME'].iloc[0]
      else:
         st.session_state['display_name'] = "PLEASE GO TO THE DISPLAY NAME TAB TO GENERATE A DISPLAY NAME FOR YOUR BADGE"
      st.dataframe(user_results_pd_df)
   else: # no rows returned
        st.markdown(":red[There is no record of the UNI_ID/UUID combination you entered. Please double-check the info you entered, check the FAQs tab below for tips on FINDING YOUR INFO, and try again]") 

def get_user_workshop_acct_info():
   # get a table of all the entries this user has made
   workshops_sql =  (f"select award_desc, organization_id ||\'.\'|| account_name as ACCOUNT_IDENTIFIER, account_locator " 
                     f"from AMAZING.APP.USER_ACCOUNT_INFO_BY_COURSE where type = 'MAIN' and UNI_ID=trim('{st.session_state.uni_id}') " 
                     f"and UNI_UUID=trim('{uni_uuid}')") 
   workshops_df = session.sql(workshops_sql)
   workshops_results = workshops_df.to_pandas()
   workshops_rows = workshops_results.shape[0]

   # show the entries
   if workshops_rows>=1:
       st.write("You have entered account info for the following badge workshops:")
       st.dataframe(workshops_results)

def workshop_chosen_changed():
   st.session_state['editing_workshop']=False
   st.session_state['submit_new_account_info'] = False
   st.session_state['account_locator'] = ''
   st.session_state['account_identifier'] = ''


def get_workshop_info():   
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
      st.write('Finished the function, boss!')   
   elif for_edits_pd_df_rows == 0:
      st.write('You have not previously entered account information for this workshop. Please add the information below.')
   else:
      st.write("there should only be 1 or zero rows.") 
      
#####################################
# Session Initializations
# initialize_user_info()
cnx=st.connection("snowflake")
session = cnx.session()
if 'auth_status' not in st.session_state:
    st.session_state['auth_status'] = 'not_authed'

# Temp for debugging
st.session_state

# Page Header
st.header('Are You Snow-A-Mazing?')
st.write('Welcome to the learn.snowflake.com Workshop Badge Management app!')
st.write('Using this app you can manage your badge name and email and you can view your results.')

uni_id = st.text_input('Enter your learn.snowflake.com UNI ID:')
uni_uuid = st.text_input('Enter the secret UUID displayed on the DORA is Listening Page of any Workshop:')
find_my_uni_record = st.button("Find my UNI User Info")

if find_my_uni_record:
   # reset all session vars
   initialize_user_info()

   # Set uni_id and key to entries on form
   st.session_state['uni_id'] = uni_id
   st.session_state['uni_uuid'] = uni_uuid

   # this will query the db and if finds a match will populate profile vars
   get_user_profile_info()

###################################### Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["View Name/Email", "Edit Name/Email","Display Name", "Workshop Account Info", "FAQs"])

with tab1:
   st.subheader("Your Name and Email - Currently Stored in Our System")
   if st.session_state.auth_status == 'authed':
        st.markdown("**GIVEN NAME:** " + st.session_state.given_name)
        st.markdown("**MIDDLE/ALTERNATE NAME:** "+ st.session_state.middle_name) 
        st.markdown("**FAMILY NAME:** " + st.session_state.family_name)
        st.markdown("**EMAIL:** " + st.session_state.badge_email)
        if st.session_state.display_name != "PLEASE GO TO THE DISPLAY NAME TAB TO GENERATE A DISPLAY NAME FOR YOUR BADGE":
            st.markdown("**Name Will Display on Badge As:** " + st.session_state.display_name)
        else:
            md_str =  "**Name Will Display on Badge As:** :red[" + st.session_state.display_name + "]"       
            st.markdown(md_str)
        st.write("-----")
        st.markdown("*If your display name has not been generated, or you would like to make changes to information, use other tabs and edit your information*")
   else:
        st.markdown(":red[Please sign in using your UNI_ID and UUID in the section above.]")
###################################
with tab2:
   st.subheader("Edit or Confirm Your Name for Your Badge(s)")

   if st.session_state.auth_status == 'authed':
        with st.form("badge_name_and_email"):
            st.write("Confirm Your Name for Any Badges That Might Be Issued")     
            edited_given = st.text_input("Given Name (Name used to greet you)", st.session_state.given_name)
            edited_middle = st.text_input('Middle Name/Nickname/Alternate-Spelling (Optional)', st.session_state.middle_name)
            edited_family = st.text_input('Family Name', st.session_state.family_name)
            edited_email = st.text_input("The Email Address You Want Your Badge Sent To (does not have to match UNI, Snowflake Trial, or Work):", st.session_state.badge_email)
            submit_edits = st.form_submit_button("Update My Badge Name & Badge Email")  

        if submit_edits:
            session.call('AMAZING.APP.UPDATE_BADGENAME_BADGEEMAIL_SP',uni_id, uni_uuid, edited_given, edited_middle, edited_family, edited_email)
            get_user_profile_info() 
            st.success('Badge Name & Email Updated', icon='🚀')

   else: # not authed
        st.markdown(":red[Please sign in using your UNI_ID and UUID in the section above.]")  
 
#######################################
with tab3:
   st.subheader("Format the Display of Your Name on Your Badge(s)")

   if st.session_state.auth_status == 'authed':
      with st.form("display_formatting"):
            display_option_1 = edited_given.capitalize() + " " + edited_middle.capitalize() + " " + edited_family.capitalize() #lazy do it for me
            display_option_2 = edited_given.capitalize() + " " + edited_middle.capitalize() + " " + edited_family #european w nobiliary
            display_option_3 = edited_family.upper() + " " + edited_middle + " " + edited_given.capitalize()  #east asian with alt script middle
            display_option_4 = edited_family.upper() + " " +  edited_given.capitalize() + " " + edited_middle.capitalize() #east asian with alt script middle
            display_option_5 = edited_given.capitalize() + " " +  edited_middle.capitalize() + " " + edited_family.upper() #ze french
                
            badge_name_order = st.radio("Name Display Order You Prefer:",                            
                                  [display_option_1, display_option_2, display_option_3, display_option_4, display_option_5],
                                  captions = ["Common in Anglo Traditions", "For names with nobiliary particles", "For use with dual script like 전 JEON Joon-kook 정국 ", "For cultures that put FAMILY name first", "Common for French and Francophonic"]
                                   )
            submit_display_format = st.form_submit_button("Record My Name Display Preference")
        
      if submit_display_format:
            if badge_name_order == display_option_1:
                display_format = 1
                edited_display_name = display_option_1     
            elif badge_name_order == display_option_2:
                display_format = 2
                edited_display_name = display_option_2    
            elif badge_name_order == display_option_3:
                display_format = 3
                edited_display_name = display_option_3         
            elif badge_name_order == display_option_4:
                display_format = 4
                edited_display_name = display_option_4
            elif badge_name_order == display_option_5:
                display_format = 5
                edited_display_name = display_option_5
            else: 
                st.write('Choose a format for your name')
                    
            session.call('AMAZING.APP.UPDATE_BADGE_DISPLAYNAME_SP',uni_id, uni_uuid, display_format, edited_display_name)
            get_user_profile_info()
            st.success('Badge Display Name Updated', icon='🚀')
   else: # not authed
         st.markdown(":red[Please sign in using your UNI_ID and UUID in the section above.]")  
 
##########################################
with tab4:
   st.subheader("View Trial Account Information You've Entered")
   if st.session_state.auth_status == 'authed':
      # display of info for all registered workshops
      get_user_workshop_acct_info()        
     
      # drop list with option button for editing
      st.session_state.workshop_choice =  st.selectbox("Choose Workshop/Badge want to enter/edit account info for:"
                                                      , ('Badge 1: DWW', 'Badge 2: CMCW', 'Badge 3: DABW', 'Badge 4: DLKW', 'Badge 5: DNGW')
                                                      , on_change = workshop_chosen_changed()
                                                      , key=1)
      workshop_to_view = st.button("Create/Edit Acct Info for Chosen Workshop") 

      if workshop_to_view: #button clicked
         st.session_state.editing_workshop=True
         # st.session_state.submit_new_acct_info=False


      # clicking above button makes this appear by setting property to True
      if st.session_state.editing_workshop==True:    
         get_workshop_info()
         with st.form("edit_acct_info"):
            st.markdown("**Edit Trial Account Info for " + st.session_state.workshop_choice + "**")
            edited_acct_id = st.text_input("Enter Your Account Identifier as found in your Snowflake Account:", st.session_state.account_identifier)
            edited_acct_loc = st.text_input("Enter Your Account Locator as found in your Snowflake Account:", st.session_state.account_locator)
            submit_button = st.form_submit_button("Update Trial Account Info")
    
         if submit_button: #button clicked
               st.session_state.submit_new_acct_info=True
               st.write(f"You submited ACCOUNT IDENTIFIER {edited_acct_id} and ACCOUNT LOCATOR {edited_acct_loc} for Workshop {st.session_state.workshop_choice}")
               
         if st.session_state.submit_new_acct_info==True: 
            if len(edited_acct_id) < 15 or len(edited_acct_id) > 18:
               st.write("The ACCOUNT ID you entered does not seem accurate. Please try again.")
            elif edited_acct_id.find(".") < 0:
               st.write("The ACCOUNT ID does not seem accurate. Please try again.")
            elif len(edited_acct_loc) < 7 or len(edited_acct_loc) > 8:
               st.write("The ACCOUNT LOCATOR does not seem accurate. Please try again.")
            else:    
               st.session_state.account_identifier = edited_acct_id
               st.session_state.account_locator = edited_acct_loc
               st.write(f"Planning to write {edited_acct_id} and {edited_acct_loc} to the database")
               # get_user_workshop_acct_info()

      #else:
           #st.write("If you intend to pursue the " + st.session_state.workshop_acro + " badge, you should click the Register button below.")
           # new_badge_interest = st.button("Register for the " + st.session_state.workshop_acro + " Badge")
      
   else: # not authed
         st.markdown(":red[Please sign in using your UNI_ID and UUID in the section above.]")  
 
        
        #with st.form("workshops"):  
         #   st.write("editing will happen here")
         #   workshop_chosen = st.form_submit_button("Show Data on My Chosen Workshop")
