import os
import json
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="My AI Assistant",
    page_icon="🤖"
)

st.title("🤖 My AI Assistant")
st.caption("Roman Urdu + English | AI Voice Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

def speak_button(text, number):
    safe_text = json.dumps(text, ensure_ascii=True)
    components.html(
        f"""
        <button onclick="speakAnswer({safe_text})"
        style="padding:10px 16px;border-radius:10px;
        border:1px solid #888;cursor:pointer;">
        🔊 Speak
        </button>
        <script>
        function speakAnswer(text) {{
            const u = new SpeechSynthesisUtterance(text);
            u.lang = "en-GB";
            u.rate = 1;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(u);
        }}
        </script>
        """,
        height=55,
    )

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            speak_button(msg["content"], i)

question = st.chat_input("Apna sawal likho...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    key = st.secrets.get(
        "GROQ_API_KEY",
        os.getenv("GROQ_API_KEY")
    )

    if not key:
        st.error("Groq API key set nahi hui.")
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
                            "content": (
                                "You are a helpful assistant. "
                                "Reply in simple Roman Urdu or English, "
                                "matching the user's language."
                            ),
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
                speak_button(answer, len(st.session_state.messages))

        except Exception:
            st.error(
                "AI connection nahi ho saka. "
                "Internet aur API settings check karo."
            )
                
