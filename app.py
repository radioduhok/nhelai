import streamlit as st
from groq import Groq

# 1. Page Setup (Navê Malperî)
st.set_page_config(page_title="Nhel AI", page_icon="🤖", layout="centered")

# 2. Sidebar Design (Navê kêlekê)
with st.sidebar:
    st.title("🤖 Nhel AI")
    st.info("ئەڤە بۆتێ زیرەکێ (Nhel AI) یە. پسیار بکە، دێ ب بادینی بەرسڤێ دەت.")
    st.write("Created by: Nihel Xelil")

# 3. Connect to Groq (Bi Rêka Secrets)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("کێشە د کلیلا API دا هەیە. تکایە li Secrets دابنێ.")
    st.stop()

# 4. System Prompt (Mêşkê Nhel AI)
system_prompt = {
    "role": "system",
    "content": """
    You are a helpful and polite AI assistant named 'Nhel AI'. 
    You were created by Nihel Xelil.
    You MUST answer strictly in Kurdish Badini dialect (Kurmanji). 
    Your tone should be friendly and professional.
    Do not use Sorani or English unless explicitly asked.
    """
}

# 5. Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# 6. Display Chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. User Input & Response
if prompt := st.chat_input("پسیارا خۆ لڤێرە بنڤیسە..."):
    # Nîşandana pisyara bikarhêneri
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Wergrtina bersivê
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
