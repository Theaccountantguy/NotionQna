from openai import OpenAI
import streamlit as st
import time
import openai
from streamlit_option_menu import option_menu
import json
import requests
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
from pathlib import Path

THIS_DIR = Path(__file__).parent
CSS_FILE = THIS_DIR / "style" / "style.css"
ASSETS = THIS_DIR / "assets"
LOTTIE_ANIMATION = ASSETS / "hello.json"

pageimage = "images/pagetitle.png"
avatarimage = "images/chat-bot.png"
user_image = "images/user.png"
message_count = 0

st.set_page_config(page_title="Notion Formula Chatbot", layout="wide", page_icon=pageimage)

with open(CSS_FILE) as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)
    
lottie_hello = load_lottiefile("assets/hello.json")

selected = option_menu(
    menu_title=None,
    options=["Info","Chat","Give"],
    icons=["info-square","chat-dots","gift"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

if selected == "Chat":
    #st.info("Bot is selected")
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

with st.sidebar:
    api_key_input = st.text_input('**Enter API Key:**', type="password", placeholder="Enter API Key Here", help="Go to https://platform.openai.com/api-keys to generate your API key")
    option = st.selectbox('**Select GPT Model:**',('gpt-3.5-turbo','gpt-4-1106-preview'), help=("1. For **free plan** of OpenAI, Select **'gpt-3.5-turbo'** (lower accuracy) \n 2. For **paid plan** of OpenAI, Select **'gpt-4-1106-preview'** (higher accuracy)"))
    file = st.file_uploader("**Add Your Image:** (Optional)",  type = ['png', 'jpg', 'jpeg'] ,label_visibility="visible",help=("This image will be visible in the chat window when you type questions (leave empty for default image)"))
    # Sidebar API key input with a toggle
    # Links for additional actions or information
    #st.markdown("[Get an OpenAI API key](https://platform.openai.com/api-keys)")
    
    #components.html(
    #"""
    #<script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script><script type='text/javascript'>kofiwidget2.init('Donate', '#29abe0', 'G2G1V9SV5');kofiwidget2.draw();</script> 
    #""",
    #)
    url = 'https://ko-fi.com/theaccountantguy'

# Create a markdown link that looks like a button
    link = f'<a href="{url}" target="_blank"><button style="display: inline-block; background-color: #0291d9; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; font-size: 16px; cursor: pointer; border-radius: 5px;">🎁 Donate</button></a>'
    st.markdown(link, unsafe_allow_html=True)
    #components.html(
    #"""
    #<div style='width: 200px; height: 100px; transform: scale(1); transform-origin: top left;'>
    #    <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script>
    #    <script type='text/javascript'>kofiwidget2.init('Donate', '#29abe0', 'G2G1V9SV5');kofiwidget2.draw();</script> 
    #</div>
    #""",
    #height=50
#)
    #st.sidebar.write('<br>', unsafe_allow_html=True)
    st.sidebar.markdown("Made with ❤️ by [Sanat Biswal](https://theaccountantguy.gumroad.com/)", unsafe_allow_html=True)
    
col1, col2 = st.columns([16, 4])

if(selected == "Chat"):
    with col1:
        st.title("Notion Formula Chatbot")
        st.caption("😎 An AI powered chatbot to help with Notion formulas")
    user_image_path = user_image
if file:
    user_image_path = file
if(selected == "Chat"):
    with st.expander("⬇️ **Instructions**", expanded=False):  # Set to True if you want it expanded by default
        st.markdown("""
    Thank you for using the Notion Formula Bot! Follow the steps below to start using the bot:
""")
        st.write('**Step 1 :** Enter an **OpenAI key** on the left to activate the Chatbot.')
        st.write('**Step 2:** Select your desired **GPT Model** to interact with the bot.')
        st.markdown("""
    <u>**Tutorial:**</u> 👉 Watch this **YouTube video** for instructions on setting up the bot correctly.
""", unsafe_allow_html=True)
        st.markdown("""
    <u>**Note:**</u> How it works? 👇 \n1. **Free Plan**, limited to **<u>10 conversations</u>**\n\n2. **Paid Plan**, enjoy **<u>Unlimited Conversations</u>** (click on **Upgrade** above for paid plan 🚀)
""", unsafe_allow_html=True)
if api_key_input:
    def test_openai_api_key(api_key_input):
        try:
        # Temporary set the OpenAI API key
            openai.api_key = api_key_input
        
        # Perform a lightweight test call - This is just a placeholder example
            response = openai.Completion.create(engine=option, prompt="Hello", max_tokens=5)
        
        # If the call succeeds, the API key is valid
            st.success("API key validated!")
            return True
        except Exception as e:
        # If an error occurs, the API key might be invalid
            st.error(f"Failed to validate API key: {e}")
            return False
    
    #if test_openai_api_key(api_key_input):
    #    st.success('API Key is valid!')
    #else:
    #    st.error('API Key is invalid or unauthorized.')

    client = OpenAI(api_key=api_key_input)

    if(api_key_input.startswith('sk-') and len(api_key_input)>50):
        if(selected=="Chat"):
            st.success("API Key Entered. Proceed to ask your questions below!. 👇" ,icon='✅')
    else:
        if(selected=="Chat"):
            error_placeholder = st.empty()
            error_placeholder.error("Incorrect API Key Entered!", icon='❌')
            time.sleep(3)
            error_placeholder.empty()
            st.info("Please enter your OpenAI API Key to proceed.",icon='🔑')
else:
    if(selected=="Chat"):
        def prompt_for_api_key():
            st.info("Please enter your OpenAI API Key to proceed." ,icon='🔑')

client = OpenAI(api_key=api_key_input)
client = None
if api_key_input:
    client = OpenAI(api_key=api_key_input)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = option

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

for message in st.session_state.messages:
    avatar_path = user_image_path if message["role"] == "user" else avatarimage
    with st.chat_message(message["role"], avatar=avatar_path):
        st.markdown(message["content"])
    
#max_messages = (
#    10 # Counting both user and assistant messages, so 10 iterations of conversation
#)

#if len(st.session_state.messages) >= max_messages:
#    st.info("Message limit exceeded")
#    st.stop()

if (prompt := st.chat_input("Type Notion formula question here ")):
    
    if not api_key_input:
        prompt_for_api_key()
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    #st.session_state.conversation_count += 1

    # Display user's message
    user_image_path = "images/chatbot.png"
    if file:
        user_image_path = file
    else:
        user_image_path = user_image

    with st.chat_message("user", avatar=user_image_path):
        st.markdown(prompt)

    # Placeholder for "Bot is thinking..." message
    thinking_placeholder = st.empty()

    avatar_path = "images/chat-bot.png"
    # Display "Bot is thinking..." message in the placeholder
    with thinking_placeholder.container():
        avatar_path = "images/chat-bot.png"
        with st.chat_message("assistant", avatar=avatar_path):
            st.markdown("Generating response... 😎💡📝")

    # Call the API to get the assistant's response
    stream = client.chat.completions.create(
        model=option,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Use the write_stream to asynchronously get the response and display it
    # Assuming st.write_stream will handle the stream and display the response
    with st.chat_message("assistant", avatar=avatar_path):
        response = st.write_stream(stream)

    # Clear the "Bot is thinking..." message after the response is received
    thinking_placeholder.empty()

    # Now display the assistant's actual response in place of "Bot is thinking..."
    #with st.chat_message("assistant", avatar=avatar_path):
    #    st.markdown(response)

    # Append the assistant's response to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_count += 1
    message_count = int(len(st.session_state.messages) / 2)

with col2:
    if(selected == "Chat"):
        st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
        st.button('Clear Chat History', key='clear_chat', on_click=clear_chat_history)
        st.markdown("""
        <style>
        .stButton>button {
        color: black;
        background-color: #ebeef5;
        }
        .stButton>button:hover {
        background-color: grey;  /* Change this to your desired hover color */
        color: white;  /* Optional: Change text color on hover */
        }
        </style>""", unsafe_allow_html=True)
        st.text('Conversations : ' + str(st.session_state.conversation_count))

if(selected == "Info"):
    
    col1, col2 = st.columns([0.7, 0.2])
    with col1:
        st.write("Hi, I am **Sanat** 👋")
        st.subheader("A Notion User just like you")
        st.markdown("""
        I have always felt the need to take help of a Chat bot to help me with the Notion formulas, <br>thus Notion Formula Bot.
    """, unsafe_allow_html=True)
        st.markdown("[More about me ->](https://theaccountantguy.gumroad.com/)")
    with col2:    
        st_lottie(lottie_hello, height=200, width=200)
if(selected == "Info"):        
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <h4 style='font-weight:heavy;'>🤖 What is Notion Formula Chatbot</h4>
    """, unsafe_allow_html=True)
    st.markdown("""
        <p style='font-weight:normal;'>Notion Formula Bot simplifies your work by quickly solving your Notion formula-related queries. Simply type your formula query in the chat window and let the chatbot do the magic for you 🤩 </p>
    """, unsafe_allow_html=True)
    st.markdown("""
        <p style='font-weight:normal;'>Navigate to the <u>chat section</u> above to get started now. </p>
    """, unsafe_allow_html=True)
    st.markdown("[Watch here ->](https://theaccountantguy.gumroad.com/)")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <h4 style='font-weight:heavy;'>🤝 Connect with me</h4>
    """, unsafe_allow_html=True)
    st.markdown("✉️ [ notionformyuse@gmail.com->](mailto:notionformyuse@gmail.com)")
    st.markdown("🌐 [ Twitter->](https://twitter.com/accountantguy21)")

if(selected == "Give"):
    st.markdown("""
        <p style='font-weight:normal;'>If you are looking to <strong>support</strong> my work, you can click on the <strong><u>Donate</u></strong> button below to donate any amount as you wish. 😊 <br><br> Thanks! 🙏</p>
    """, unsafe_allow_html=True)
    url = 'https://ko-fi.com/theaccountantguy'
    st.write('<br>', unsafe_allow_html=True)
# Create a markdown link that looks like a button
    link = f'<a href="{url}" target="_blank"><button style="display: inline-block; background-color: #0291d9; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; font-size: 16px; cursor: pointer; border-radius: 5px;">🎁 Donate</button></a>'
    st.markdown(link, unsafe_allow_html=True)
    #components.html(
    #"""
    #<script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script><script type='text/javascript'>kofiwidget2.init('Donate', '#29abe0', 'G2G1V9SV5');kofiwidget2.draw();</script> 
    #""",
    #)
   