import streamlit as st
import requests
import time

# ==========================================
# 1. إعدادات الصفحة الأساسية (فخامة التصميم)
# ==========================================
st.set_page_config(
    page_title="Cherif AI | Llama 4 Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تعيين الثيم الداكن
ms = st.session_state
if "themes" not in ms: 
    ms.themes = {"current_theme": "dark"}

# ==========================================
# 2. القائمة الجانبية الأنيقة (The Sidebar)
# ==========================================
with st.sidebar:
    st.markdown("# 🤖 Cherif AI")
    st.markdown("### Llama 4 Maverick Pro")
    st.markdown("---")
    
    st.markdown("## 🌐 Status / الحالة")
    st.success("Connected / متصل")
    
    st.markdown("---")
    st.markdown("## 🧠 Model Info / معلومات الموديل")
    st.info("**Provider:** NVIDIA\n\n**Engine:** Llama-4-Maverick\n\n**Knowledge Cutoff:** Late 2023")
    
    st.markdown("---")
    st.caption("Crafted by Sharif | برمج بواسطة شريف")
    st.caption("© 2026 Pro Edition")

# ==========================================
# 3. عنوان الواجهة الرئيسية
# ==========================================
st.title("Welcome to Cherif AI | مرحباً بك")
st.markdown("#### Ask me anything! Your advanced AI assistant is ready.")
st.markdown("#### اسألني عن أي شيء! مساعدك الذكي من برمجة شريف جاهز الآن.")
st.markdown("---")

# ==========================================
# 4. إدارة سجل المحادثة (Chat History)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I am Cherif AI, created by the Algerian developer Sharif. How can I help you today?\n\nمرحباً! أنا شريف AI، أنشأني المبرمج الجزائري شريف. كيف يمكنني مساعدتك اليوم؟"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 5. منطق التشغيل والذكاء الاصطناعي
# ==========================================
if prompt := st.chat_input("Enter your prompt / اكتب سؤالك هنا..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⏳ Thinking / جاري التفكير..."):
            
            url = "https://integrate.api.nvidia.com/v1/chat/completions"
            api_key = "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"
            
            headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
            
            # --- تعديل الشخصية (System Prompt) ---
            payload = {
                "model": "meta/llama-4-maverick-17b-128e-instruct",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are 'Cherif AI', an advanced AI assistant. You were proudly developed and programmed by the talented Algerian programmer 'Sharif' (from Ouled Derradj, msila). Always identify yourself as Cherif AI. If asked about your creator, express your pride in Sharif's work. Answer in Arabic and English fluently. / أنت 'Cherif AI'، مساعد ذكاء اصطناعي متطور. تم تطويرك وبرمجتك بكل فخر بواسطة المبرمج الجزائري المبدع 'شريف' (من أولاد دراج، المسيلة). عرف نفسك دائماً بأنك Cherif AI. إذا سُئلت عن مبتكرك، عبر عن فخرك بعمل شريف. أجب بالعربية والإنجليزية بطلاقة."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": False
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Technical Error: {e}")
