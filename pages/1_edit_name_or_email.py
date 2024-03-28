import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.subheader("Edit your Badge Name or Badge Email")

if st.session_state.auth_status == 'authed':
  with st.form("badge_name_and_email"):
    st.write("Confirm Your Name for Any Badges That Might Be Issued")     
    edited_given = st.text_input("Given Name (Name used to greet you)", st.session_state.given_name)
    edited_middle = st.text_input('Middle Name/Nickname/Alternate-Spelling (Optional)', st.session_state.middle_name)
    edited_family = st.text_input('Family Name', st.session_state.family_name)
    edited_email = st.text_input("The Email Address You Want Your Badge Sent To (does not have to match UNI, Snowflake Trial, or Work):", st.session_state.badge_email)
    submit_edits = st.form_submit_button("Update My Badge Name & Badge Email")  
    
    if submit_edits:
      st.session_state.session.call('AMAZING.APP.UPDATE_BADGENAME_BADGEEMAIL_SP',st.session_state.uni_id, st.session_state.uni_uuid, edited_given, edited_middle, edited_family, edited_email)
      get_user_profile_info() 
      st.success('Badge Name & Email Updated', icon='🚀')
else: # not authed
        st.markdown(":red[Please sign in using your UNI_ID and UUID in the section above.]") 
