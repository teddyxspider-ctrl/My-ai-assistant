
import os
import requests
import streamlit as st

st.set_page_config(page_title="My AI Assistant", page_icon="🤖")
st.title("🤖 My AI Assistant")
st.caption("Roman Urdu + English | AI Voice Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Apna sawal likho...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

    if not key:
        st.error("Groq API key abhi set nahi hui.")
    else:
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": "Bearer " + key,
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-oss-120b",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant. Reply in simple Roman Urdu or English, matching the user's language."
                        },
                        *st.session_state.messages,
                    ],
                },
                timeout=60,
            )
            response.raise_for_status()
            answer = response.json()["choices"][0]["message"]["content"]

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

            with st.chat_message("assistant"):
                st.write(answer)

        except Exception:
            st.error("AI se connection nahi ho saka. API key aur connection check karo.")
          
