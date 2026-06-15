import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


st.title("GenAI Interview Coach")
st.caption("Powered by Gemini 2.5 Flash")

# initialize chat history in session_state
if "history" not in st.session_state:
    st.session_state.history = []

# display all previous messages
for msg in st.session_state.history:
    role = "user" if msg["role"] == "user" else "assistant"
    st.chat_message(role).write(msg["parts"][0]["text"])

# handle new input
if prompt := st.chat_input("Ask me anything about GenAI interviews..."):
    # show user message
    st.chat_message("user").write(prompt)

    # add to history
    st.session_state.history.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    # call Gemini with full history
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=st.session_state.history,
        config={
            "system_instruction": "You are a GenAI interview coach. Give short, clear, interview-ready answers.",
            "temperature": 0
        }
    )

    reply = response.text

    # add reply to history
    st.session_state.history.append({
        "role": "model",
        "parts": [{"text": reply}]
    })

    # show assistant message
    st.chat_message("assistant").write(reply)



    if st.session_state.history:

        history_text = "\n\n".join(
            [
                f"{'USER' if m['role'] == 'user' else 'ASSISTANT'}:\n{m['parts'][0]['text']}"
                for m in st.session_state.history
            ]
        )

        st.download_button(
            label="📥 Download Conversation",
            data=history_text,
            file_name="interview_session.txt",
            mime="text/plain"
        )