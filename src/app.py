import streamlit as st
import os
from dotenv import load_dotenv

st.set_page_config(layout="centered")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi there! I'm your task assistant. How can I help?"}
    ]

# --- LOAD ENV ---
load_dotenv()
default_openai = os.getenv("OPENAI_API_KEY", "")
default_notion = os.getenv("NOTION_API_KEY", "")
default_db = os.getenv("NOTION_DB_LINK", "")
default_template = os.getenv("NOTION_TEMPLATE_LINK", "")
default_purpose = os.getenv("AGENT_PURPOSE", "")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    openai_api_key = st.text_input("OpenAI API Key", value=default_openai, type="password")
    notion_api_key = st.text_input("Notion API Key", value=default_notion, type="password")
    notion_database_url = st.text_input("Notion Database URL", value=default_db)
    notion_template_url = st.text_input("Notion Template URL", value=default_template)
    agent_purpose = st.text_area("Agent Purpose / Style", value=default_purpose)
    if st.button("💾 Save Settings"):
        env_path = "../.env"
        os.makedirs(os.path.dirname(env_path), exist_ok=True)
        from dotenv import set_key
        set_key(env_path, "OPENAI_API_KEY", openai_api_key)
        set_key(env_path, "NOTION_API_KEY", notion_api_key)
        set_key(env_path, "NOTION_DB_LINK", notion_database_url)
        set_key(env_path, "NOTION_TEMPLATE_LINK", notion_template_url)
        set_key(env_path, "AGENT_PURPOSE", agent_purpose)
        st.success("✅ Environment variables updated!")


st.title("Ideo - A Notion Assistant")
st.markdown("### 💬 Chat with Assistant")

# --- CHAT DISPLAY ---
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# --- USER INPUT ---
user_input = st.chat_input("Speak to the agent...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Placeholder assistant reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            assistant_reply = f"I heard: {user_input}. (Placeholder reply)"
            st.write(assistant_reply)
    
    st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})
    st.rerun()