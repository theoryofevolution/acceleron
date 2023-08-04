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

print(top_teams['Team'][0])

st.subheader(f"Winner: {top_teams['Team'][0]}")
st.subheader(f"Runner Up: {top_teams['Team'][1]}")
st.subheader(f"Third Place: {top_teams['Team'][2]}")