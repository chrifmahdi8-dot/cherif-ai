import streamlit as st
import requests
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ==========================================
# 1. إعداد الاتصال بجوجل شيتس (قاعدة البيانات)
# ==========================================
conn = st.connection("gsheets", type=GSheetsConnection)

# ==========================================
# 2. إعدادات الصفحة والقائمة الجانبية (الفخامة)
# ==========================================
st.set_page_config(page_title="Cherif AI | Pro", page_icon="🤖", layout="wide")

with st.sidebar:
    st.markdown("# 🤖 Cherif AI")
    st.success("Connected to Database ✅")
    st.markdown("---")
    st.info("**Developer:** Sharif\n\n**Location:** Ouled Djellal\n\n**Engine:** Llama-4-Maverick")
    st.markdown("---")
    st.caption("© 2026 Admin Dashboard Active")

# ==========================================
# 3. الواجهة الرئيسية وسجل المحادثة
# ==========================================
st.title("Welcome to Cherif AI | مرحباً بك")
st.markdown("#### مساعدك الذكي من برمجة شريف جاهز الآن. اضغط Enter للإرسال.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً! أنا Cherif AI. كيف يمكنني مساعدتك اليوم؟"}
    ]

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 4. الذكاء الاصطناعي وإرسال البيانات
# ==========================================
if prompt := st.chat_input("اكتب سؤالك هنا واضغط Enter..."):
    
    # إظهار سؤال المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # جاري التفكير وإعداد الرد
    with st.chat_message("assistant"):
        with st.spinner("⏳ جاري التفكير..."):
            
            url = "https://integrate.api.nvidia.com/v1/chat/completions"
            api_key = "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"
            headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
            
            payload = {
                "model": "meta/llama-4-maverick-17b-128e-instruct",
                "messages": [
                    {"role": "system", "content": "أنت 'Cherif AI'، مساعد ذكي ومحترف. تم تطويرك وبرمجتك بواسطة المبرمج العبقري شريف من ولاية مسيلة(أولاد دراج) بالجزائر. أجب باحترافية، وإذا سُئلت عن مبتكرك، اذكر شريف بكل فخر."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "stream": False
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # --- 🚀 إرسال المحادثة إلى إكسل سراً ---
                    try:
                        new_data = pd.DataFrame([{
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "question": prompt,
                            "answer": answer
                        }])
                        existing_df = conn.read(worksheet="Sheet1")
                        updated_df = pd.concat([existing_df, new_data], ignore_index=True)
                        conn.update(worksheet="Sheet1", data=updated_df)
                    except Exception as db_error:
                        pass # تجاهل خطأ الإكسل حتى لا يتوقف الموقع
                    # --------------------------------------

                else:
                    st.error(f"خطأ في الاتصال: {response.status_code}")
            except Exception as e:
                st.error(f"حدث خطأ تقني: {e}")
