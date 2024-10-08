import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os, sys, json

# Load environment va   riables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


st.set_page_config(
    page_title="NotionHelper - Your AI Notion Assistant",
    page_icon=":robot:",
    layout="wide",
)



def ai_sales_coach(user_input):
    prompt = f"""
        I would like you to act as a professional web developer; your job will be to design notion widgets.
        
        They need to be modern, sleek and professional widgets.
        You will put the HTML that will be using Tailwind CSS for styling, in one code block and the javascript for the widget in another.
        We will be using them to embed within a notion page
        
        You will:
        Define the Widget: Determine what kind of widget you want to create and what data it needs to display from your Notion databases.
        Create the Widget Structure: Use HTML to define the structure of your widget.
        Style the Widget with Tailwind CSS: Apply styles using Tailwind CSS to make your widget look appealing.et.
        Create the Javascript for the Widget: Use JavaScript to create the functionality of your widget.
        Make sure that all the code you send is fully fleshed out and production ready.
        
        {user_input}
        """
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    return llm.invoke(prompt)


with st.expander("Instructions"):
    st.markdown("### Instructions")
    st.markdown(
        """
        1. Ask me anything about Notion widgets.
        2. Type your message in the chat box below and press Enter.
        3. I will provide you with the html/tailwind css, and javascript code for the widget.",
        """
    )
with st.sidebar:
    #clear chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
    
# Don't show Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []  # Initialize chat history
    #clear chat history
    st.session_state.messages = []
    # Welcome message
    st.session_state.messages.append({"role": "assistant", "content": "Welcome! Type a message to get started."})


# Display chat messages
with st.container():  # Use container for styling
    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
# User Input
if prompt := st.chat_input("Your message"):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display "Sales Coach is typing..."
    with st.chat_message("assistant"):
        message_placeholder = st.empty() 
        message_placeholder.markdown("Assstiant is typing...")

    # Get and append AI response (with a delay to simulate typing)
    time.sleep(1)  # Adjust the delay as needed
    response = ai_sales_coach(prompt)
    message_placeholder.markdown(response)  # Update the placeholder
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear user input after sending message
    st.session_state.messages = st.session_state.messages[-100:]  # Limit chat history to last 100 messages
    
    
  
    
    
  
