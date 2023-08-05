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
    targetTime.setHours(17, 0, 0, 0); // Set target time to 5:00 PM (17:00)
    var display = document.querySelector('#time');
    startTimer(targetTime, display);
};
</script>
<body>
  <div>Time left <span id="time">17:00:00</span></div>
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
        uploaded_file = st.file_uploader("Choose your CSV submission", accept_multiple_files=False, type=['csv'])
        if uploaded_file is not None:
            if uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)['LABEL']
        submitted = st.form_submit_button("Submit", type='primary')
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
    if current_hour >= 17 and current_minute >= 0:
        submitted = False
        if st.button('The results are out!'):
            switch_page('winners')
    elif submitted:
        if uploaded_file is None:
            st.warning("You must submit a CSV file!")
        else:
            model_score = accuracy_score(ground_truth, df)
            user_row = pd.Series([model_score, username], index=leaderboard.columns)

            if username in leaderboard['Team'].values:
                leaderboard.loc[leaderboard['Team'] == username, 'Score'] = model_score
                leaderboard.loc[leaderboard['Team'] == username, 'Team'] = username
            else:
                leaderboard = leaderboard.append(user_row, ignore_index=True)

            # Sorting the dataframe by Score in descending order
            leaderboard = leaderboard.sort_values(by='Score', ascending=False).reset_index(drop=True)
            leaderboard.to_csv('leaderboard.csv', index=False)
            st.table(leaderboard)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
