import streamlit as st
import requests

# 1. إعداد شكل صفحة الموقع
st.set_page_config(page_title="Sharif AI", page_icon="🤖")

st.title("🤖 ذكاء شريف الاصطناعي - Llama 4")
st.write("أهلاً بك! هذا الموقع من برمجة شريف، مدعوم بأقوى نماذج الذكاء الاصطناعي.")

# 2. واجهة المستخدم في الموقع
user_question = st.text_input("اكتب سؤالك هنا:")

if st.button("إرسال السؤال"):
    if user_question:
        with st.spinner("⏳ جاري التفكير..."):
            # إعدادات الـ API الخاصة بك
            url = "https://integrate.api.nvidia.com/v1/chat/completions"
            api_key = "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"
            
            headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
            payload = {
                "model": "meta/llama-4-maverick-17b-128e-instruct",
                "messages": [{"role": "user", "content": user_question}],
                "temperature": 0.7,
                "stream": False
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.success("الرد:")
                    st.write(answer)
                else:
                    st.error(f"خطأ في الاتصال بالخادم: {response.status_code}")
            except Exception as e:
                st.error(f"حدث خطأ تقني: {e}")
    else:
        st.warning("من فضلك اكتب سؤالاً أولاً!")

# إضافة لمسة جمالية في الأسفل
st.markdown("---")
st.caption("برمج بواسطة شريف | 2026")