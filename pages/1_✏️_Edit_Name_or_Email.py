import streamlit as st
import pandas as pd

cnx=st.connection("snowflake")
session = cnx.session()


def get_user_profile_info():
   #start over with authentication and populating vars
   this_user_sql =  (f"select badge_given_name, badge_middle_name, badge_family_name, display_name, badge_email "
                     f"from UNI_USER_BADGENAME_BADGEEMAIL where UNI_ID=trim('{st.session_state.uni_id}') "
                     f"and UNI_UUID=trim('{st.session_state.uni_uuid}')")
   this_user_df = session.sql(this_user_sql)
   user_results_pd_df = this_user_df.to_pandas()                          
   user_rows = user_results_pd_df.shape[0]

   if user_rows>=1:       
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

####################### PAGE CONTENTS ###########
st.subheader(":pencil2: Edit your Badge Name or Badge Email")
st.write("Please use any characters or alphabet you would like. We want you to be able to display your name in your mother tongue.")
if 'auth_status' not in st.session_state or st.session_state.auth_status == 'not-authed':
   st.markdown(":red[Please sign in using your UNI_ID and UUID in the sidebar of the homepage.]")
elif st.session_state.auth_status == 'authed':
  with st.form("badge_name_and_email"):
    st.write("Confirm Your Name for Any Badges That Might Be Issued")     
    edited_given = st.text_input("Given Name (Name used to greet you)", st.session_state.given_name)
    edited_middle = st.text_input('Middle Name/Nickname/Alternate-Spelling (Optional)', st.session_state.middle_name)
    edited_family = st.text_input('Family Name', st.session_state.family_name)
    edited_email = st.text_input("The Email Address You Want Your Badge Sent To (does not have to match UNI, Snowflake Trial, or Work):", st.session_state.badge_email)
    submit_edits = st.form_submit_button("Update My Badge Name & Badge Email")  
    
    if submit_edits:
      session.call('AMAZING.APP.UPDATE_BADGENAME_BADGEEMAIL_SP',st.session_state.uni_id, st.session_state.uni_uuid, edited_given, edited_middle, edited_family, edited_email)
      get_user_profile_info() 
      st.success('Badge Name & Email Updated', icon='🚀')

   
