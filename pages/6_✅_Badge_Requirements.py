
import streamlit as st

st.subheader(":white_check_mark: Badge Requirements")
st.write("Please check the requirements listed on this page. We get SO MANY inquiries that we should not get. This app should provide you with what you need to SELF-SERVICE any issues.")

st.write("This app is new as of April 9th, 2024. You may have used other methods to get badges in the past. The concepts are the same but the methods have changed.")
st.markdown('----------')

if st.session_state.given_name is None:
  emoji_1 = ":x:"
else:
  emoji_1 = ":white_check_mark:"
st.markdown(emoji_1 + " **STEP 1:** Tell us your name and email.") 
st.markdown("*Edit as needed. This is done on the :pencil2:  page.*") 
st.markdown("**CURRENT STATUS:** Your name is listed as " + st.session_state.given_name + " " + st.session_state.middle_name)
st.markdown('----------')

st.write(st.session_state.display_name)
if "DISPLAY NAME" in st.session_state.display_name:
  emoji_2 = ":x:"
else:
  emoji_2 = ":white_check_mark:"
st.markdown(emoji_2 + " **STEP 2:** Generate a Display Name. :green[This is NEW!]") 
st.markdown("*The Display Name feature gives you full control over how your name is displayed on any badge that is issued. This is done on the :star: page.*") 
st.markdown("")
st.markdown('------------')
st.markdown(":white_check_mark: **STEP 3:** For EVERY BADGE you hope to receive, you will need to see a row on the :chains: page.") 
st.markdown("To create or edit the info on the :chains: page, use the :link: page. Without this LINK established for each badge, DORA does not know who is doing the work so she cannot issue the badge.")         
st.markdown("Every badge entry on the :chains: page should have both Account Locator and Account ID field completed.")
st.markdown("")
st.markdown("*Some older entries where you have already received your badge may have empty values. That is okay for older badges but for NEW badges, ALL columns MUST be complete.*")

st.markdown('---------------------')
st.markdown(":white_check_mark: **STEP 4:** For EVERY BADGE you hope to recieve, you need to complete every DORA check and see both PASSED and VALID for that test.") 
st.markdown("*View your tests on the :robot_face: page. Filter down to PASSED and VALID. These are the only tests DORA considers.*")
st.markdown("*A test that is PASSED but NOT VALID is a test that was changed by you before sending it to DORA.*")
st.markdown("*You can FAIL any or all tests many times as long as you pass each test at least one time (and it is valid). When each test has at least one VALID/PASSED entry you can receive your badge.*")

st.markdown('---------------------')

st.subheader(":x: Troubleshooting")
st.markdown("Did you make one of these common mistakes?")
st.markdown(":x: Have you received this badge already? We check the UNI ID before issueing. We don't issue twice to the same UNI ID.")
st.markdown(":x: Has someone using the same Snowflake Trial Account already received the badge? We don't issue twice on the same Trial Account.")
st.markdown(":x: Did you accidently skip a test? Look closely at your tests, is any number in the sequence missing?")
st.markdown(":x: Did mis-spell your email? It happens so often. If you did this, you'll have to file a ticket to get it corrected.")
st.markdown(":x: Have you checked ACHIEVE.SNOWFLAKE.COM and/or your Email Inbox to see if your badge was already issued? The :sports_medal: page has some lag time between when your badge is issued and when it shows up in that list.")


