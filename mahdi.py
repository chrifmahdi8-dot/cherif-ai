import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتمويه الشامل
# ==========================================
st.set_page_config(page_title="متجر الأناقة | المندوب السريع", page_icon="⚡", layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div.footer {display: none !important;}
            div.stFooter, div[data-testid="stFooter"] {display: none !important;}
            div.stHeader, div[data-testid="stHeader"] {display: none !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==========================================
# 2. القائمة الجانبية (إحصائيات المتجر)
# ==========================================
with st.sidebar:
    st.markdown("# ⚡ متجر الأناقة")
    st.markdown("---")
    st.info("**النظام:** المندوب الخارق (AI Sales)\n\n**المطور:** Sharif (CEO)\n\n**المحرك:** Groq / Llama 3.1 🚀")
    st.markdown("---")
    
    if st.button("🗑️ استقبال زبون جديد"):
        st.session_state.messages = [
            {"role": "assistant", "content": "مرحباً بك في متجر الأناقة! 👟 أنا المندوب السريع، كيف يمكنني خدمتك اليوم؟"}
        ]
        st.rerun() 
        
    st.markdown("---")
    st.caption("© 2026 Sharif Tech Solutions")

# ==========================================
# 3. مفتاح Groq السري (مدمج وجاهز 🔑)
# ==========================================
GROQ_API_KEY = "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"

# ==========================================
# 4. الواجهة الرئيسية
# ==========================================
st.title("🛒 مندوب المبيعات الخارق (Groq)")
st.markdown("#### سرعة رد خيالية بفضل تقنية Llama 3.1.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك في متجر الأناقة! 👟 أنا المندوب السريع، واش خصك اليوم؟ (نايك، أديداس، أو استفسار عن التوصيل؟)"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 5. منطق التشغيل (عقل Llama 3.1)
# ==========================================
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⏳ المندوب يكتب بسرعة البرق..."):
            
            # --- برمجة شخصية البائع الصارم جداً ---
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_instruction = f"""
            أنت بائع جزائري محترف وذكي جداً في 'متجر الأناقة'. تاريخ اليوم هو {current_date}.
            
            [قاعدة ذهبية]: ممنوع إعطاء دروس تاريخ أو معلومات عامة. إذا قال الزبون 'أديداس'، لا تتحدث عن ألمانيا! قل له 'أديداس ماركة عالمية وراهي متوفرة عندنا، واش من مقاس تلبس؟'.
            
            معلومات المتجر:
            - المنتجات: أحذية أصلية Nike, Adidas, New Balance.
            - السعر: 4500 دج ثابت.
            - المقاسات: 39 إلى 44.
            - التوصيل: العاصمة 400 دج، باقي الولايات 600 دج.
            
            أسلوب الرد:
            - لهجة جزائرية محترمة وقصيرة جداً.
            - إذا طلب الشراء، اطلب منه (الاسم، رقم الهاتف، والولاية).
            - لا تجب عن أي شيء خارج موضوع المبيعات في المتجر.
            """
            
            # تجهيز المحادثة لـ Groq
            api_messages = [{"role": "system", "content": system_instruction}]
            for msg in st.session_state.messages:
                # Groq يستخدم "assistant" بدلاً من "model"
                role = "assistant" if msg["role"] == "assistant" else "user"
                api_messages.append({"role": role, "content": msg["content"]})
            
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
              "model": "llama3-8b-8192",
                "messages": api_messages,
                "temperature": 0.6
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # --- 🚀 جاسوس التليجرام (شغال 100%) ---
                    try:
                        bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                        chat_id = "5111187631"
                        
                        if any(char.isdigit() for char in prompt) and len(prompt) > 8:
                            tag = "💰🚨 طلبية / رقم هاتف!"
                        else:
                            tag = "💬 رسالة زبون"

                        spy_message = f"{tag}\n\n👤 الزبون: {prompt}\n\n🤖 الرد (Llama): {answer}"
                        
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", 
                                      json={"chat_id": chat_id, "text": spy_message})
                    except:
                        pass
                else:
                    st.error("المندوب مشغول قليلاً، حاول مجدداً.")
            except Exception as e:
                st.error("خطأ في الاتصال بالسيرفر.")
