import streamlit as st
from streamlit_chat import message as st_message
from PIL import Image
import requests


st.set_page_config(
    page_title="Rasa_ChatBot",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state="expanded",
)

image = Image.open('logo.jpg')
st.image(image, use_column_width=True)

st.title('Rasa ChatBot')
st.markdown("""
This app is using framework RASA to create a chatbot can communicate with you!
""")

# About

st.markdown("""
* **Python Library**: ...
* **Credit:** Written by [Thong Truong](https://github.com/thongtruong2k1).
----------------------------------------------
* **Select your avatar:**
""")

AvatarStyle = [ 
    "adventurer", 
    "adventurer-neutral", 
    "avataaars",
    "big-ears",
    "big-ears-neutral",
    "big-smile",
    "bottts", 
    "croodles",
    "croodles-neutral",
    "female",
    "human",
    "male"
]

expander_avatar = st.expander("Choose your avatar")
col1, col2, col3 = expander_avatar.columns(3)

with col1:
    for avatar in AvatarStyle[:4]:
        st.markdown(f"<h3 style='text-align: center; color: black;'>{avatar}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: grey;'><img src='https://avatars.dicebear.com/api/{avatar}/15.jpg'></p>", unsafe_allow_html=True)
        st.markdown("----------------------------------")

with col2:
    for avatar in AvatarStyle[4:8]:
        st.markdown(f"<h3 style='text-align: center; color: black;'>{avatar}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: grey;'><img src='https://avatars.dicebear.com/api/{avatar}/15.jpg'></p>", unsafe_allow_html=True)
        st.markdown("----------------------------------")

with col3:
    for avatar in AvatarStyle[8:]:
        st.markdown(f"<h3 style='text-align: center; color: black;'>{avatar}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: grey;'><img src='https://avatars.dicebear.com/api/{avatar}/15.jpg'></p>", unsafe_allow_html=True)
        st.markdown("----------------------------------")




if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.avatar = "adventurer" 
    
with st.sidebar.form("form1"):
    sidebar = st.selectbox("Choose your avatar:", AvatarStyle, key="avatar_st")
    check_reset = st.checkbox("Reset The Message", False)
    submitted = st.form_submit_button("Submit")
    if submitted:
        if check_reset == True:
            st.session_state.history = []
        st.session_state.avatar = sidebar
        st.session_state.input_text = ""


def generate_answer(url):
    user_message = st.session_state.input_text
    myobj = { "sender": "test_user", "message": user_message}
    x = requests.post(url, json = myobj)
    response = eval(x.text)
    bot_message = response[0]["text"]
    st.session_state.history.append({"message": user_message, "is_user": True, "avatar_style": st.session_state.avatar, "seed": 15})
    st.session_state.history.append({"message": bot_message, "is_user": False})

st.title("Hello Chatbot")


url = 'http://localhost:5005/webhooks/myio/webhook'
try:
    input_message = st.text_input("Input Message", key="input_text", placeholder="Please enter a text")

    if st.session_state.input_text:
        generate_answer(url)

    count = 0

    for chat in st.session_state.history:
        st_message(key=count, **chat)
        count += 1
except:
    st.warning("Please enable Rasa before chat with the bot by using 'rasa --enable-api'.")