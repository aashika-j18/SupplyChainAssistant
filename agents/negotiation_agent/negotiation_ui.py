import pandas as pd
import streamlit as st
from negotiation_agent import negotiation_agent

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! Please provide item description, quantity, and offer details to proceed."}
    ]

st.title("Supplier Negotiation Agent")
st.write("Analyze and compare vendor offers to make informed negotiation decisions.")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user's message
if prompt := st.chat_input("Enter the current vendor offer details:"):
    # Append user's message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate agent's response **with full conversation history**
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Pass full chat history to agent
        history_text = "\n".join(f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history)
        response = negotiation_agent.run(history_text)
        
        response_text = response.content
        response_placeholder.markdown(response_text)

    # Append agent's response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
