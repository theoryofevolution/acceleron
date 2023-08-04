import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from streamlit_card import card
import json
import pandas as pd
from sklearn.metrics import accuracy_score
import yaml
from yaml.loader import SafeLoader
from streamlit.components.v1 import html
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page


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

def get_data():
        return pd.read_csv('leaderboard.csv')

timer = """
<!DOCTYPE html>
<html>
<head>
    <style>
    body {
        font-family: sans-serif;
        color: #31333F;
        font-size: 20px; /* adjust size as necessary */
        font-weight: bold;
    }
    </style>
<script>
function startTimer(targetTime, display) {
    setInterval(function () {
        var currentTime = new Date();
        var remainingTime = targetTime - currentTime;

        var hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = hours + ":" + minutes + ":" + seconds;

        if (remainingTime < 0) {
            clearInterval(this);
            display.textContent = "00:00:00";
        }
    }, 1000);
}

window.onload = function () {
    var targetTime = new Date();
    targetTime.setHours(22, 30, 0, 0); // Set target time to 5:00 PM (17:00)
    var display = document.querySelector('#time');
    startTimer(targetTime, display);
};
</script>
<body>
  <div>Time left <span id="time">22:30:00</span></div>
</body>
</html>
"""



hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f'Welcome *{name}*')
    authenticator.logout('Logout', 'main')
    st.title('The Quine Accelerator')
    html(timer)
    global submitted
    leaderboard = get_data()
    ground_truth = pd.read_csv('ground_truth.csv')['LABEL']
    with st.form("CSV_submission"):
        uploaded_file = st.file_uploader("Choose a CSV", accept_multiple_files=False, type=['csv'])
        if uploaded_file is not None:
            if uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)['LABEL']
        submitted = st.form_submit_button("Submit", type='primary')
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
    if submitted:
        model_score = accuracy_score(ground_truth, df)
        new_row = {'Team': username, 'Score': model_score}
        leaderboard = leaderboard.append(new_row, ignore_index=True)
        leaderboard = leaderboard.sort_values('Score', ascending=False).groupby('Team').first().reset_index()
        leaderboard.to_csv('leaderboard.csv', index=False)
        top_teams = leaderboard.nlargest(3, 'Score', keep='all')
        st.table(top_teams)
    if current_hour >= 22 and current_minute >= 30:
        if st.button('Find out who the winners are!'):
            switch_page('winners')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
