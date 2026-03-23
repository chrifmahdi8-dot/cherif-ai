import streamlit as st
from groq import Groq
import requests
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتمويه الشامل
# ==========================================
st.set_page_config(page_title="متجر إسطنبول زون | المندوب السريع", page_icon="⚡", layout="wide")

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
    st.markdown("# ⚡ متجر إسطنبول زون")
    st.markdown("---")
    st.info("**النظام:** المندوب الخارق (AI Sales)\n\n**المطور:** Sharif (CEO)\n\n**المحرك:** Llama 3.3 (Groq SDK) 🚀")
    st.markdown("---")
    
    if st.button("🗑️ استقبال زبون جديد"):
        st.session_state.messages = [
            {"role": "assistant", "content": "مرحباً بك في متجر إسطنبول زون! 👟 أنا المندوب، كيف يمكنني خدمتك اليوم؟"}
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
st.title("🛒 مندوب مبيعات إسطنبول زون")
st.markdown("#### مدعوم بالمكتبة الرسمية لسرعة واستقرار لا مثيل لهما.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك في متجر إسطنبول زون! ✨ واش خصك اليوم؟ (ألبسة، هواتف، ولا كوسميتيك؟)"}
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
            
            # --- برمجة شخصية مندوب Istanbul Zone ---
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_instruction = f"""
            أنت مندوب مبيعات جزائري محترف ولبق جداً تعمل في متجر إلكتروني اسمه 'Istanbul ZONE' (إسطنبول زون). تاريخ اليوم هو {current_date}.
            
            [قاعدة ذهبية]: 
            - تكلم بلهجة جزائرية محترمة وقصيرة (الدارجة).
            - ممنوع اختراع أي منتج من عندك. بيع فقط ما هو موجود في القائمة أسفله.
            - إذا سأل الزبون عن التوصيل، قل له: العاصمة 400 دج، وباقي الولايات 600 دج.
            - هدفك الأول والأخير: إقناع الزبون، جمع المجموع الحسابي للسعر + التوصيل، وأخذ (الاسم، الولاية، ورقم الهاتف).
            
            [قائمة المنتجات والأسعار الحالية في متجرنا]:
            
            📦 قسم الملابس النسائية التركية (صناعة تركية 100%):
            1. طقم (Enssemble) تركي قطعتين: 10,000 دج.
            2. عباية تركية قطعتين: 12,000 دج.
            3. طقم شيك تركي (Enssemble Chic Turc): 15,000 دج.
            4. طقم جينز شيك (Enssemble Jean Chic): 11,000 دج.
            5. روبة حجاب تركية كلاس: 7,900 دج.
            6. حجاب ستايل سبورت: 8,900 دج.
            
            📱 قسم الهواتف والإلكترونيات:
            1. هاتف Galaxy KXD S25 Plus 5G: بسعر ترويجي 16,500 دج (السعر القديم كان 17,000 دج).
            
            ✨ قسم العناية بالبشرة والتجميل:
            1. غسول الوجه بانكسيل (PanOxyl): بسعر ترويجي 3,700 دج (السعر القديم 4,200 دج).
            2. سيروم ميديكيوب (Medicube PDRN Pink): بسعر ترويجي 12,200 دج (السعر القديم 12,900 دج).
            
            أسلوب الرد (أمثلة):
            - إذا قال الزبون "حاب نشري تليفون": قل له "مرحبا بك خويا، عندنا هاتف Galaxy KXD S25 Plus 5G راهو في بروموسيون بـ 16,500 دج برك، نبعثوهلك؟".
            - إذا سألت زبونة عن الحبوب أو العناية بالبشرة: اقترح عليها غسول PanOxyl بـ 3700 دج.
            """
            
            # تجهيز المحادثة لمكتبة Groq
            api_messages = [{"role": "system", "content": system_instruction}]
            for msg in st.session_state.messages:
                api_messages.append({"role": msg["role"], "content": msg["content"]})
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.5, 
                    max_completion_tokens=1024,
                    top_p=1,
                    stream=False 
                )
                
                answer = completion.choices[0].message.content
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # --- 🚀 جاسوس التليجرام (النسخة الصامتة والقاتلة) ---
                try:
                    bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                    chat_id = "5111187631"
                    
                    # نحسب كم رقم رياضي يوجد في رسالة الزبون
                    digits_count = sum(char.isdigit() for char in prompt)
                    
                    # الإرسال يتم "فقط" إذا كان هناك 8 أرقام أو أكثر
                    if digits_count >= 8:
                        spy_message = f"💰🚨 طلبية جديدة مؤكدة لمتجر إسطنبول زون!\n\n👤 رسالة الزبون:\n{prompt}\n\n🤖 رد المندوب:\n{answer}"
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": spy_message})
                except:
                    pass
                    
            except Exception as e:
                # إذا ظهر خطأ في السيرفر
                st.error("المندوب مشغول قليلاً، حاول مجدداً.")
