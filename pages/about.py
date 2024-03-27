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

