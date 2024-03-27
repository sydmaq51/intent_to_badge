import streamlit as st
import pandas as pd

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




with tab5:
   st.write("just a placeholder for now")
