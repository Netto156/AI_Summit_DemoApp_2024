from openai import OpenAI
import streamlit as st
import re
import time
from email.message import EmailMessage
import smtplib
from streamlit_extras.stylable_container import stylable_container
# python -m streamlit run Chatbot.py

# Set constants
MODEL_ID = st.secrets["model_id"]
API_KEY = st.secrets["api_key"]
EMAIL_PW = st.secrets["email_pw"]
EMAIL_SENDER = st.secrets["email"]

# Get CSS styling
with open( ".app\style.css" ) as css:
    MAIN_CSS = css.read()

#  ------------------------ Logic ---------------------------------------------
@st.cache_resource
def get_client():
    print("Creating new client....")
    client = OpenAI(api_key=API_KEY)
    return client

CLIENT = get_client()


def create_new_thread():
    print("Creating new thread id....")
    thread = CLIENT.beta.threads.create()
    st.session_state['Thread_id'] = thread.id
    return


def validate_user_input():
    data_valid = True

    # Validate email
    if data_valid:
        if not re.match(r"^\S+@\S+\.\S+$", st.session_state['email']):
            data_valid = False

    # Validate first name
    if data_valid:
        data_valid = len(st.session_state['first_name']) >= 2

    # Validate last name
    if data_valid:
        data_valid = len(st.session_state['last_name']) >= 3

    # Assign output
    st.session_state['Valid_input'] = data_valid
    return


def query_assistant(user_input):
    assistant=CLIENT.beta.assistants.retrieve(MODEL_ID)
    thread = CLIENT.beta.threads.retrieve(st.session_state['Thread_id'])
    message = CLIENT.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= user_input
    )
    run = CLIENT.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
    )

    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1) # Wait for 1 second
        run = CLIENT.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        if run.status == 'completed': 
            messages = CLIENT.beta.threads.messages.list(
            thread_id=thread.id
        )
            GPT_response = messages.data[0].content[0].text.value
        else:
            print(run.status)  
    
    return(GPT_response) 


def mail_conversation():
    if st.session_state["mail_my_result"] == "Yes":
        print("Sending conversation per mail...")
        email = st.session_state.email
        print(email)
        conversation = ""
        for m in st.session_state['messages']:
            conversation += "--{0} : {1} \n\n".format(m["role"], m["content"])
        # send_email(email, conversation)
    return

# ---------------------------------- UI Functions --------------------------------------------

def get_user_info():
    print("getting user info")
    st.session_state['Form_count'] += 1
    st.markdown("""<div class='FormHeader'/>Please enter your contact details to continue""" , unsafe_allow_html=True)
    placeholder = st.empty()

    with placeholder.form(key="user_input_{0}".format(st.session_state['Form_count'])):
        with stylable_container(key="Start_dialog", css_styles=MAIN_CSS):

            st.text_input("First name", placeholder="Enter your first name", key="first_name")
            st.text_input("Last name", placeholder="Enter your last name", key="last_name")
            st.text_input("Email", placeholder="Enter your email", key="email")
            col1, _, col3 = st.columns(3)
            with col1:
                submit_button = st.form_submit_button("Submit", on_click=validate_user_input)
            with col3:
                st.link_button("See our privacy policy", "https://www.incentro.com/nl-NL/privacy-policy")

            if submit_button:
                placeholder.empty()
    return


def send_email(recipient, message):
    print("sneding mail to: "+ recipient)
    sender = EMAIL_SENDER
    password = EMAIL_PW

    message = """Incentro thanks you for your interest in their demo at the UiPath AI summit.\nHereby you receive a copy of your conversation with our chatbot.\n\n""" + message + """\n\nPlease feel welcome to reach out.\n\nWith kind regards the AI-summit-bot @ incentrp"""

    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "Recap of conversation with chatbot demo of Incentro - UiPath AI summit"
    email.set_content(message)

    with smtplib.SMTP("smtp-mail.outlook.com", port=587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.sendmail(sender, recipient, email.as_string())
        smtp.quit()


def end_the_conversation():
    st.markdown("""<div class='FormHeader'/>Feedback on the conversation""" , unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        placeholder_for_radio1 = st.radio("Did you like this tool?", ["Yes", "No"], key="liked", index=None)

    with col2:
        placeholder_for_radio2 = st.radio("Would you like to receive a copy of the conversation per email?", ["Yes", "No"], horizontal=True, key="mail_my_result", index=None)
    
    if st.button("Submit"):
        st.session_state['Conversation_ended'] = True
        st.session_state['Ending_conversation'] = False
        st.rerun()


def conversation_ended():
    with stylable_container(key="Final_dialog", css_styles=MAIN_CSS):
        st.markdown("Thank you for your time, we hope you found this usefull")
        st.link_button("See other succes stories", "https://www.incentro.com/en")
    

# This is needed to make sure you do not lose your session variables (pretty weird, I know....)
for x,y in st.session_state.items():
    st.session_state[x] = y


# ---------------------------------- UI Main page --------------------------------------------


with stylable_container(key="main_page", css_styles=MAIN_CSS):
    st.image("https://0097f9ca.flyingcdn.com/wp-content/uploads/2022/04/Incentro-logo-2018-Orange-1024x174.png", width=200)
    st.title("Hyper Automation Discoverer")
    st.caption("""<div class='CenterElem'/> 🤖 A chatbot to help you discovery you automation potential 🚀""", unsafe_allow_html=True)

# Initialize variables
if "Valid_input" not in st.session_state:
    print("initializing vars..")
    st.session_state['Valid_input'] = False
    st.session_state['Conversation_ended'] = False
    st.session_state['Form_count'] = 0
    st.session_state['Ending_conversation'] = False

# Get user input before starting the chat
if st.session_state['Valid_input'] == False:
    if st.session_state['Form_count'] > 0:
        get_user_info()
        st.info("To continue, please correctly fill in this form")
    else:
        get_user_info()

# get user input at the end of the conversation
if st.session_state['Ending_conversation']:
    end_the_conversation()


# Start chat with user
if st.session_state['Valid_input'] and not st.session_state['Conversation_ended'] and not st.session_state['Ending_conversation']:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hi {0}, I'd like to help you discovery your automation potential. In what branch do you work?".format(st.session_state.first_name)}]

    # write chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Get user input 
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Create new thread
        if not st.session_state['Thread_id']:
            create_new_thread()


        # Display loading symbol while getting response from gpt-model
        with st.spinner('Thinking...'):
            msg = query_assistant(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    # End conversation
    if st.button("End conversation"):
        st.session_state["Ending_conversation"] = True
        st.rerun()

# Conversation has ended and last pop-up was filled in
if st.session_state['Conversation_ended']:
    mail_conversation()
    conversation_ended()
