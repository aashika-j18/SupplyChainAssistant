
import pandas as pd
import streamlit as st
from agents.negotiation_agent import negotiation_agent


st.title("Supplier Negotiation Agent")
st.write("Analyze and compare vendor offers to make informed negotiation decisions.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter the current vendor offer details:"):
  
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_text = ""
        response = negotiation_agent.run(prompt)
        response_text = response.content
        response_placeholder.markdown(response_text)

    st.session_state.chat_history.append({"role": "assistant", "content": response_text})


