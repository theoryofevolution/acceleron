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
import json



st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

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

timer =  """
<style>
    .centered-div {
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: sans-serif;
        font-size: 24px;
        font-weight: bold;
        color: #31333F;
    }
    #time {
        margin-left: 10px;  /* Adjust this value as needed for more or less space */
    }
</style>
<div class="centered-div">
    <span id="pre-text">Competition closes in</span><span id="time">00d 00h 00m 00s</span>
</div>
<script>
    function countdownTimer(endDate, display) {
        var timer = setInterval(function () {
            var now = new Date().getTime();
            var distance = endDate - now;

            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            days = days < 10 ? "0" + days : days;
            hours = hours < 10 ? "0" + hours : hours;
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

            if (distance < 0) {
                clearInterval(timer);
                document.getElementById('pre-text').textContent = "Time is up!";
                display.textContent = " Please reload the page.";
            }
        }, 1000);
    }

    window.onload = function () {
        var endDate = new Date("2023-08-30T17:00:00").getTime();  // Adjust end date as needed
        var display = document.querySelector('#time');
        countdownTimer(endDate, display);
    };
</script>
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
    if username == 'yashs':
        def yaml_to_json(yaml_file_path):
            with open(yaml_file_path, 'r') as yaml_file:
                # Convert YAML file content to Python dictionary
                data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            
            # Convert Python dictionary to JSON string
            json_str = json.dumps(data, indent=4)
            return json_str

        # Streamlit UI
        st.title("Private Admin Console")

        # Path to the YAML file
        yaml_file_path = "config.yaml"  # Update this to your YAML file path

        try:
            # Convert YAML to JSON
            json_output = yaml_to_json(yaml_file_path)
            st.download_button("Download User Data JSON file", data=json_output, file_name="user_data.json", mime="application/json")
            st.download_button("Download Winner Data", data=json_output, file_name="leaderboard.csv", mime="text/csv")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.markdown(
        """
        <style>
            .center-text {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100px;
                font-size: 48px;
                font-weight: bold;  /* Make it bold */
            }
        </style>
        <div class="center-text">
            The People of Programming Accelerator
        </div>
        """,
        unsafe_allow_html=True,
    )
        html(timer)
        info, website, other, other1, other2 = st.columns(5)
        with info:
            pass
        with website:
            hasClicked = card(
            title="Sponsor Info Card 1",
            text="Some description",
            image="http://placekitten.com/200/300",
            url="https://github.com/gamcoh/st-card"
            )
        with other:
            hasClicked = card(
            title="Sponsor Info Card 2",
            text="Some other description",
            image="http://placekitten.com/200/300",
            url="https://github.com/gamcoh/st-card"
            )
        with other1:
            hasClicked = card(
            title="Sponsor Info Card 3",
            text="Some other OTHER description. You can create more or less cards.",
            image="http://placekitten.com/200/300",
            url="https://github.com/gamcoh/st-card"
            )
        with other2:
            pass
        cs1, cs2 = st.columns(2)
        gt = pd.read_csv('ground_truth.csv')
        compd = pd.read_csv('iris_dataset.csv')
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv(index=False).encode('utf-8')
        csv = convert_df(gt)
        compd = convert_df(compd)
        with cs1:
            st.subheader('Competition Data')
            st.download_button(
            label="Download sample submission as CSV",
            data=csv,
            file_name='sample_submission.csv',
            mime='text/csv')
            st.download_button(
            label="Download competiton data as CSV",
            data=compd,
            file_name='competition_data.csv',
            mime='text/csv')
        with cs2:
            st.subheader('Competition Information')
            with st.expander("See background information"):
                st.write("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sollicitudin tempor id eu nisl nunc mi ipsum. Bibendum neque egestas congue quisque egestas diam. Eget aliquet nibh praesent tristique magna sit. Duis tristique sollicitudin nibh sit amet commodo. Sit amet volutpat consequat mauris nunc congue nisi vitae. Nam at lectus urna duis. At augue eget arcu dictum varius duis at. Nisi lacus sed viverra tellus in hac habitasse platea. Magna fermentum iaculis eu non diam. At imperdiet dui accumsan sit amet nulla facilisi.""")
            with st.expander("See submission rules"):
                st.write("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sollicitudin tempor id eu nisl nunc mi ipsum. Bibendum neque egestas congue quisque egestas diam. Eget aliquet nibh praesent tristique magna sit. Duis tristique sollicitudin nibh sit amet commodo. Sit amet volutpat consequat mauris nunc congue nisi vitae. Nam at lectus urna duis. At augue eget arcu dictum varius duis at. Nisi lacus sed viverra tellus in hac habitasse platea. Magna fermentum iaculis eu non diam. At imperdiet dui accumsan sit amet nulla facilisi.""")
        global submitted, leaderboard
        st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        leaderboard = get_data()
        leaderboard.index = leaderboard.index + 1
        ground_truth = pd.read_csv('ground_truth.csv')['VARIETY']
        submission, leader = st.columns(2)
        with submission:
            with st.form("CSV_submission"):
                uploaded_file = st.file_uploader("Choose your CSV submission", accept_multiple_files=False, type=['csv'])
                if uploaded_file is not None:
                    try:
                        if uploaded_file.type == "text/csv":
                            df = pd.read_csv(uploaded_file)['VARIETY']
                    except:
                        st.error("Error with submission")
                submitted = st.form_submit_button("Submit", type='primary')
                # Get current date and time
                current_time = datetime.now()
                current_hour = current_time.hour
                current_minute = current_time.minute
                current_day = current_time.day
                # Check if it's 10 pm and the 15th day of the month
                # Get current date and time
                current_time = datetime.now()
                current_hour = current_time.hour
                current_minute = current_time.minute
                current_day = current_time.day
                if submitted:
                    if uploaded_file is None:
                        st.warning("You must submit a CSV file!")
                    if current_hour >= 17 and current_minute >= 0 and current_day >= 30:
                        st.warning("Time is up!")
                    elif current_day >= 30:
                        st.warning("Time is up!")
                    else:
                        try:
                            model_score = accuracy_score(ground_truth, df)
                            user_row = pd.Series([model_score, username], index=leaderboard.columns)
                            if username in leaderboard['Team'].values:
                                leaderboard.loc[leaderboard['Team'] == username, 'Score'] = model_score
                                leaderboard.loc[leaderboard['Team'] == username, 'Team'] = username
                            else:
                                leaderboard = leaderboard.append(user_row, ignore_index=True)
                            # Sorting the dataframe by Score in descending order
                            leaderboard = leaderboard.sort_values(by='Score', ascending=False).reset_index(drop=True)
                            leaderboard.index = leaderboard.index + 1
                            leaderboard.to_csv('leaderboard.csv', index=False)
                        except:
                            st.warning("Error!")
        if current_hour >= 17 and current_minute >= 0 and current_day >= 30:
            if st.button('Check out the winners!'):
                switch_page('winners')
        elif current_day >= 30:
            if st.button('Check out the winners!'):
                switch_page('winners')
        with leader:
            if st.button('Refresh Leaderboard'):
                st.table(leaderboard)
            else:
                st.table(leaderboard)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')