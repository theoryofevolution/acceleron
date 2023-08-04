
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

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

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

try:
    if authenticator.register_user('Register', preauthorization=False):
        st.success('User registered successfully')
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        switch_page('login')
except Exception as e:
    st.error(e)

