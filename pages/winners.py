import streamlit as st
import pandas as pd

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

data = pd.read_csv("leaderboard.csv")

top_teams = data.nlargest(3, 'Score', keep='all')
st.balloons()
st.subheader(f"Winner: {top_teams['Team'][0]}")
st.write(f"Score: {top_teams['Score'][0]}")
if 1 in top_teams.index:
    st.subheader(f"Runner Up: {top_teams['Team'][1]}")
    st.write(f"Score: {top_teams['Score'][1]}")
if 2 in top_teams.index:
    st.subheader(f"Third Place: {top_teams['Team'][2]}")
    st.write(f"Score: {top_teams['Score'][2]}")