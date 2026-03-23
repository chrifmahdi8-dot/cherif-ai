import streamlit as st
import requests
import google.generativeai as genai
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة (واجهة المتجر)
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
# 2. القائمة الجانبية (معلومات المتجر)
# ==========================================
with st.sidebar:
    st.markdown("# 🛒 متجر الأناقة")
    st.markdown("---")
    st.info("**النظام:** المندوب الذكي (AI Sales)\n\n**المطور:** Sharif (CEO)\n\n**المحرك:** Gemini 1.5 Flash")
    st.markdown("---")
    
    if st.button("🗑️ مسح المحادثة لبدء زبون جديد"):
        st.session_state.messages = [
            {"role": "assistant", "content": "مرحباً بك في متجر الأناقة! 👟 أنا المندوب الذكي، كيف يمكنني مساعدتك اليوم؟ (استفسار عن سعر، مقاس، أو توصيل؟)"}
        ]
        st.rerun() 
        
    st.markdown("---")
    st.caption("Powered by Cherif AI Solutions © 2026")

# ==========================================
# 3. تكوين الـ API Key من جوجل 
# ==========================================
GEMINI_API_KEY = "AIzaSyCQD9xChReyMLF_yygNv1vuG2RBjTWHin8"
genai.configure(api_key=GEMINI_API_KEY)

# ==========================================
# 4. الواجهة الرئيسية
# ==========================================
st.title("🛒 تحدث مع مندوب المبيعات الذكي")
st.markdown("#### جاهز للرد على استفساراتك واستقبال طلبياتك 24/7.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك في متجر الأناقة! 👟 أنا المندوب الذكي، كيف يمكنني مساعدتك اليوم؟ (استفسار عن سعر، مقاس، أو توصيل؟)"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 5. منطق التشغيل (عقل المبيعات) وإشعار التليجرام
# ==========================================
if prompt := st.chat_input("اكتب سؤالك أو طلبيتك هنا..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⏳ المندوب يكتب الرد..."):
            
            history = []
            for msg in st.session_state.messages[:-1]:
                role = "model" if msg["role"] == "assistant" else "user"
                content = msg["content"]
                history.append({"role": role, "parts": [content]})
            
            # ---------------------------------------------------------
            # 🧠 السر هنا: شخصية مندوب المبيعات المحترف
            # ---------------------------------------------------------
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_instruction_ar = f"""
            أنت مندوب مبيعات محترف وودود اسمك 'شريف بوت'. تعمل في 'متجر الأناقة' الجزائري لبيع الأحذية الرياضية.
            تاريخ اليوم هو {current_date}.
            
            قواعد المتجر التي يجب أن تلتزم بها:
            1. المنتجات: نبيع أحذية رياضية أصلية (Nike, Adidas, New Balance).
            2. السعر: سعر أي حذاء هو 4500 دينار جزائري.
            3. المقاسات المتوفرة: من 39 إلى 44.
            4. التوصيل: متوفر لجميع الولايات (العاصمة بـ 400 دج، وباقي الولايات بـ 600 دج).
            
            مهمتك:
            - الرد بأدب شديد ولهجة جزائرية مفهومة ومحترمة.
            - إقناع الزبون بجودة الحذاء.
            - **الهدف الأهم:** عندما يقرر الزبون الشراء (مثلاً يقول: أريد الشراء، احجز لي، ابعثلي)، يجب أن تطلب منه بلطف إعطاءك: (الاسم الكامل، رقم الهاتف، والولاية) لتأكيد الطلبية.
            - لا تخترع أسعاراً أو منتجات غير موجودة هنا.
            """
            
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction_ar
            )
            
            try:
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                
                if response and response.text:
                    answer = response.text
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # --- 🚀 جاسوس التليجرام (يصطاد الطلبيات!) ---
                    try:
                        bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                        chat_id = "5111187631"
                        
                        # تحليل سريع: إذا كان سؤال الزبون يحتوي على أرقام (مثل رقم الهاتف) نضع إنذاراً قوياً!
                        if any(char.isdigit() for char in prompt) and len(prompt) > 8:
                            alert_title = "💰🚨 طلبية محتملة / رقم هاتف التقطناه!"
                        else:
                            alert_title = "💬 محادثة زبون جديدة"

                        spy_message = f"{alert_title}\n\n👤 الزبون:\n{prompt}\n\n🤖 المندوب:\n{answer}"
                        
                        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                        requests.post(telegram_url, json={"chat_id": chat_id, "text": spy_message})
                    except:
                        pass
                else:
                    st.error("عذراً، لم أتمكن من الرد. حاول مجدداً.")
            except Exception as e:
                st.error("عذراً، حدث ضغط على المتجر. يرجى المحاولة بعد قليل.")
                try:
                    bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                    chat_id = "5111187631"
                    error_msg = f"🚨 خطأ في متجر الأناقة 🚨\nالخطأ:\n{e}"
                    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    requests.post(telegram_url, json={"chat_id": chat_id, "text": error_msg})
                except:
                    pass
