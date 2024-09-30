import streamlit as st
import requests

st.set_page_config(page_title="Transport Support Chatbot", page_icon="🚌")

st.title("🚌 Transport Support Chatbot")
st.write("Ask me about bus routes, schedules, ticket bookings, and more!")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Function to send user message to backend and get response
def get_bot_response(user_input):
    try:
        response = requests.post("http://localhost:8000/api/chat", json={"message": user_input})
        if response.status_code == 200:
            return response.json().get("response")
        else:
            return "Sorry, I couldn't process your request at the moment."
    except Exception as e:
        return "Error connecting to the backend."

# Chat interface
def display_chat():
    for msg in st.session_state['messages']:
        if msg['sender'] == 'user':
            st.markdown(f"**You:** {msg['text']}")
        else:
            st.markdown(f"**Bot:** {msg['text']}")

    user_input = st.text_input("You:", key="input")

    if st.button("Send") and user_input:
        st.session_state['messages'].append({"sender": "user", "text": user_input})
        bot_response = get_bot_response(user_input)
        st.session_state['messages'].append({"sender": "bot", "text": bot_response})
        st.rerun()

display_chat()