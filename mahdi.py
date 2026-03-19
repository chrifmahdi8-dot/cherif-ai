import streamlit as st
import requests
import time

# ==========================================
# 1. إعدادات الصفحة الأساسية (فخامة التصميم)
# Page Configuration - Luxury & Professional Look
# ==========================================
st.set_page_config(
    page_title="Cherif AI | Llama 4 Pro",
    page_icon="🤖",
    layout="wide", # استخدام عرض الشاشة بالكامل لمظهر عصري
    initial_sidebar_state="expanded"
)

# تعيين الثيم الداكن (Dark Mode) كإعداد افتراضي
# Set default theme to Dark
ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "dark"}

# ==========================================
# 2. القائمة الجانبية الأنيقة (The Sidebar)
# branding: Cherif AI
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
    # توقيعك الفخم في الأسفل
    st.caption("Crafted by Sharif | برمج بواسطة شريف")
    st.caption("© 2026 Pro Edition")

# ==========================================
# 3. عنوان الواجهة الرئيسية (Main Interface)
# Bilingual Greeting
# ==========================================
st.title("Welcome to Cherif AI | مرحباً بك")
st.markdown("#### Ask me anything! Your advanced AI assistant is ready.")
st.markdown("#### اسألني عن أي شيء! مساعدك الذكي متقن للغة العربية جاهز الآن.")
st.markdown("---")

# ==========================================
# 4. إدارة سجل المحادثة (Chat History)
# Key for Professional Chat experience
# ==========================================
# تهيئة سلة الرسائل إذا لم تكن موجودة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I am Cherif AI, powered by NVIDIA. I can speak Arabic and English. Press Enter to send your query.\n\nمرحباً! أنا شريف AI، مدعوم من NVIDIA. أتحدث العربية والإنجليزية. اضغط Enter لإرسال سؤالك."}
    ]

# عرض الرسائل السابقة من السجل (Chat History)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 5. منطق التشغيل والضغط على Enter
# Feature: Press Enter to submit
# ==========================================
# مربع الإدخال الذكي في أسفل الصفحة (يتعرف تلقائياً على Enter)
if prompt := st.chat_input("Enter your prompt / اكتب سؤالك هنا..."):
    
    # 1. إضافة رسالة المستخدم للسجل وعرضها فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. جاري التفكير (Spinner) - مظهر احترافي
    with st.chat_message("assistant"):
        with st.spinner("⏳ Thinking / جاري التفكير..."):
            
            # --- إعدادات الـ API الخاصة بك ---
            url = "https://integrate.api.nvidia.com/v1/chat/completions"
            # المفتاح الذي نستخدمه سابقاً
            api_key = "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"
            
            headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
            payload = {
                "model": "meta/llama-4-maverick-17b-128e-instruct",
                "messages": [{"role": "user", "content": prompt}], # نرسل السؤال الجديد فقط
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": False
            }

            # 3. محاولة الاتصال بالخادم
            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    
                    # عرض الرد بشكل أنيق مع إضافة رسالةassistant للسجل
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                else:
                    st.error(f"Error Connection: {response.status_code} / خطأ في الاتصال")
            except Exception as e:
                st.error(f"Technical Error / حدث خطأ تقني: {e}")

# ==========================================
# 6. لمسات جمالية في الأسفل (Footer)
# ==========================================
# (اختياري) يمكن إضافة خط رفيع في النهاية
# st.markdown("---")