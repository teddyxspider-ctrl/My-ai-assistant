import os
import json
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="My AI Assistant", page_icon="🤖")
st.title("🤖 My AI Assistant")
st.caption("Roman Urdu + English | AI Voice Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            text_json = json.dumps(msg["content"])
            components.html(
                f"""
                <button id="speak{i}" style="padding:10px;border-radius:10px">
                🔊 Speak
                </button>
                <script>
                document.getElementById("speak{i}").addEventListener("click", function() {{
                    const text = {text_json};
                    const u = new SpeechSynthesisUtterance(text);
                    u.lang = "en-GB";
                    u.volume = 1;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(u);
                }});
                </script>
                """,
                height=60,
            )

question = st.chat_input("Apna sawal likho...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

    if not key:
        st.error("Groq API key set nahi hui. Streamlit Secrets check karo.")
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
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        except Exception:
            st.error("AI connection nahi ho saka. Internet aur API settings check karo.")
