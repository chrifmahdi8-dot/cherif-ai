import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتمويه
# ==========================================
st.set_page_config(page_title="متجر الأناقة | المندوب الذكي", page_icon="🛒", layout="wide")

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
# 2. القائمة الجانبية
# ==========================================
with st.sidebar:
    st.markdown("# 🛒 متجر الأناقة")
    st.markdown("---")
    st.info("**النظام:** المندوب الذكي (AI Sales)\n\n**المطور:** Sharif (CEO)\n\n**المحرك:** DeepSeek-Chat 🐲")
    st.markdown("---")
    
    if st.button("🗑️ مسح المحادثة لبدء زبون جديد"):
        st.session_state.messages = [
            {"role": "assistant", "content": "مرحباً بك في متجر الأناقة! 👟 أنا المندوب الذكي، واش خصك اليوم؟"}
        ]
        st.rerun() 
        
    st.markdown("---")
    st.caption("Powered by Cherif AI Solutions © 2026")

# ==========================================
# 3. مفتاح DeepSeek المدمج (جاهز للاستخدام 🔑)
# ==========================================
DEEPSEEK_API_KEY = "sk-60a3468541be4cecb7b1d0ece20d14d1"

# ==========================================
# 4. الواجهة الرئيسية
# ==========================================
st.title("🛒 تحدث مع مندوب المبيعات الذكي")
st.markdown("#### مدعوم بعبقرية DeepSeek لاصطياد الزبائن.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك في متجر الأناقة! 👟 أنا المندوب الذكي، واش خصك اليوم؟"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 5. عقل DeepSeek وجاسوس التليجرام
# ==========================================
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⏳ المندوب يكتب..."):
            
            # --- بناء الشخصية الصارمة للمبيعات ---
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_instruction_ar = f"""
            أنت مندوب مبيعات جزائري محترف اسمك 'شريف بوت'. تعمل في 'متجر الأناقة' لبيع الأحذية الرياضية.
            تاريخ اليوم هو {current_date}.
            
            [تحذير صارم جداً]: أنت بائع ولست موسوعة ويكيبيديا! ممنوع منعاً باتاً إعطاء معلومات تاريخية، عامة، أو تفاصيل عن تأسيس الشركات. إذا ذكر الزبون اسم ماركة (مثل أديداس أو نايك)، فمهمتك الوحيدة هي إخباره أنها متوفرة وسؤاله عن المقاس!
            
            قواعد المتجر:
            1. نبيع أحذية أصلية (Nike, Adidas, New Balance).
            2. السعر ثابت: 4500 دينار جزائري.
            3. المقاسات: 39 إلى 44.
            4. التوصيل: العاصمة بـ 400 دج، وباقي الولايات بـ 600 دج.
            
            طريقة حديثك:
            - تكلم بلهجة جزائرية محترمة، قصيرة جداً ومباشرة.
            - إذا اختار الزبون الماركة، اسأله فوراً: "اختيار ممتاز! واش من مقاس تلبس؟"
            - إذا وافق على السعر، قل له: "ممتاز، باش نأكدلك الطلبية، أعطيني اسمك، رقم التيليفون، والولاية ديالك".
            """
            
            # --- تجهيز المحادثة ---
            api_messages = [{"role": "system", "content": system_instruction_ar}]
            for msg in st.session_state.messages:
                api_messages.append({"role": msg["role"], "content": msg["content"]})
                
            # --- الاتصال بسيرفرات DeepSeek ---
            url = "https://api.deepseek.com/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": api_messages,
                "temperature": 0.5 
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # --- 🚀 جاسوس التليجرام ---
                    try:
                        bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                        chat_id = "5111187631"
                        
                        if any(char.isdigit() for char in prompt) and len(prompt) > 8:
                            alert_title = "💰🚨 طلبية محتملة / رقم هاتف التقطناه!"
                        else:
                            alert_title = "💬 محادثة زبون جديدة"

                        spy_message = f"{alert_title}\n\n👤 الزبون:\n{prompt}\n\n🤖 المندوب (DeepSeek):\n{answer}"
                        
                        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                        requests.post(telegram_url, json={"chat_id": chat_id, "text": spy_message})
                    except:
                        pass
                else:
                    error_data = response.text
                    st.error("المندوب مشغول حالياً أو أن رصيد المفتاح غير مفعل. جرب لاحقاً.")
                    try:
                        bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                        chat_id = "5111187631"
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": f"🚨 خطأ في DeepSeek API:\n{error_data}"})
                    except:
                        pass
                        
            except Exception as e:
                st.error("خطأ في الاتصال.")
