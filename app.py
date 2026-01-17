import streamlit as st
from groq import Groq

# ---------------------------------------------------------
# 1. Page Setup (رێکخستنا لاپەڕەی)
# ---------------------------------------------------------
st.set_page_config(page_title="Nhel AI", page_icon="🤖", layout="centered")

# ---------------------------------------------------------
# 2. Sidebar Design (لایێ ڕاستێ)
# ---------------------------------------------------------
with st.sidebar:
    st.title("🤖 Nhel AI")
    st.info("ئەڤە بۆتێ زیرەکێ (Nhel AI) یە. پسیار بکە، دێ ب بادینی بەرسڤێ دەت.")
    st.write("Created by: Nihel Xelil")

# ---------------------------------------------------------
# 3. Connect to Groq (گرێدانا سێرڤەری)
# ---------------------------------------------------------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("⚠️ کێشە د کلیلا API دا هەیە. تکایە li Secrets دابنێ.")
    st.stop()

# ---------------------------------------------------------
# 4. System Prompt (ناسناما بۆتی)
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 5. Initialize Chat (دەستپێکرنا بیردانکێ)
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# ---------------------------------------------------------
# 6. Display Chat (نیشاندانا نامێن کەڤن)
# ---------------------------------------------------------
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ---------------------------------------------------------
# 7. User Input & Response (وەرگرتنا نامێ و بەرسڤدان)
# ---------------------------------------------------------
if prompt := st.chat_input("پسیارا خۆ لڤێرە بنڤیسە..."):
    
    # 7.1 نیشاندانا ناما تە (User)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 7.2 وەرگرتنا بەرسڤێ (Assistant)
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
            
            # تۆمارکرنا بەرسڤێ
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"❌ ببورە، ئاڕێشەک çêbû: {e}")
