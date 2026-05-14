import streamlit as st
import requests
import json

# Page Configuration
st.set_page_config(
    page_title="AI Chatbot API Tester",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        color: #ffffff;
    }
    .response-container {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("⚙️ API Configuration")
st.sidebar.markdown("Configure your connection settings below.")

api_url = st.sidebar.text_input("API URL", value="http://127.0.0.1:8000/v1/chat")
api_key = st.sidebar.text_input("MASTER_API_KEY", type="password", placeholder="Enter your x-api-key")
provider = st.sidebar.selectbox("Provider", options=["groq", "gemini", "llama"], index=0)

st.sidebar.markdown("---")
st.sidebar.info("""
**How to use:**
1. Ensure your FastAPI server is running.
2. Enter your API Key.
3. Choose a provider.
4. Send a message in the chat box!
""")

# Main UI
st.title("🤖 AI Chatbot API Tester")
st.markdown("Test your production-grade Chatbot API in real-time.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare Request
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "message": prompt,
        "provider": provider
    }

    # Show request details in an expander for debugging
    with st.expander("🛠️ Request Debug Details"):
        st.write("**URL:**", api_url)
        st.write("**Headers:**", {k: (v if k != "x-api-key" else "****") for k, v in headers.items()})
        st.write("**Payload:**", payload)

    # API Call
    try:
        with st.spinner(f"Requesting {provider}..."):
            response = requests.post(api_url, headers=headers, json=payload)
            
        # Display Status Code
        if response.status_code == 200:
            result = response.json()
            reply = result.get("output_text", "No response found in output_text.")
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
                
            st.success(f"Response Status: {response.status_code} OK")
        else:
            error_msg = f"Error {response.status_code}: {response.text}"
            st.error(error_msg)
            
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")

# Clear Chat Button
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()
