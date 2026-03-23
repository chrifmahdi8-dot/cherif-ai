import streamlit as st
from groq import Groq
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
    st.info("**النظام:** المندوب الخارق (AI Sales)\n\n**المطور:** Sharif (CEO)\n\n**المحرك:** Llama 3.3 (Groq SDK) 🚀")
    st.markdown("---")
    
    if st.button("🗑️ استقبال زبون جديد"):
        st.session_state.messages = [
            {"role": "assistant", "content": "مرحباً بك في متجر الأناقة! 👟 أنا المندوب، كيف يمكنني خدمتك اليوم؟"}
        ]
        st.rerun() 
        
    st.markdown("---")
    st.caption("© 2026 Sharif Tech Solutions")

# ==========================================
# 3. إعداد عميل Groq والمفتاح
# ==========================================
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# 4. الواجهة الرئيسية
# ==========================================
st.title("🛒 مندوب المبيعات الخارق")
st.markdown("#### مدعوم بالمكتبة الرسمية لسرعة واستقرار لا مثيل لهما.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك في متجر الأناقة! 👟 واش خصك اليوم؟ (نايك، أديداس، أو استفسار عن التوصيل؟)"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 5. منطق التشغيل (عقل Llama 3.3 الرسمي)
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
            
            # تجهيز المحادثة لمكتبة Groq
            api_messages = [{"role": "system", "content": system_instruction}]
            for msg in st.session_state.messages:
                api_messages.append({"role": msg["role"], "content": msg["content"]})
            
            try:
                # الكود العبقري الذي أحضرته أنت!
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.5, # قللنا الحرارة ليكون بائعاً جاداً
                    max_completion_tokens=1024,
                    top_p=1,
                    stream=False # جعلناها False لكي يرسل الرسالة كاملة للتليجرام بسهولة
                )
                
                answer = completion.choices[0].message.content
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # --- 🚀 جاسوس التليجرام ---
                try:
                    bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                    chat_id = "5111187631"
                    
                    if any(char.isdigit() for char in prompt) and len(prompt) > 8:
                        tag = "💰🚨 طلبية / رقم هاتف!"
                    else:
                        tag = "💬 رسالة زبون"

                    spy_message = f"{tag}\n\n👤 الزبون: {prompt}\n\n🤖 الرد: {answer}"
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": spy_message})
                except:
                    pass
                    
            except Exception as e:
                # إذا ظهر خطأ، سيرسله الجاسوس لهاتفك لتعرف السبب فوراً
                st.error("المندوب مشغول قليلاً، حاول مجدداً.")
                try:
                    bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                    chat_id = "5111187631"
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": f"🚨 خطأ Groq:\n{e}"})
                except:
                    pass
