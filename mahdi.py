import streamlit as st
from groq import Groq
import requests
from datetime import datetime
import base64
from PIL import Image

# ==========================================
# 1. إعدادات الصفحة الفاخرة والتمويه
# ==========================================
st.set_page_config(
    page_title="Massilya Dermo-Cosmétiques | المندوب الخبير", 
    page_icon="🧴", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
div.footer {display: none !important;}
div.stFooter, div[data-testid="stFooter"] {display: none !important;}
div.stHeader, div[data-testid="stHeader"] {display: none !important;}

/* تحسين مظهر واجهة المحادثة */
[data-testid="stChatMessageAvatarAssistant"] { background-color: #10B981; }
[data-testid="stChatMessageAssistant"] { background-color: #F0FDF4; border-radius: 10px; padding: 10px; }

/* تخصيص مظهر الأزرار */
.stButton>button { background-color: #10B981; color: white; border-radius: 5px; border: none; }
.stButton>button:hover { background-color: #059669; color: white; }

/* تصميم بطاقات المنتجات */
.prod-card { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #A7F3D0; text-align: center; margin-bottom: 20px; transition: 0.3s; }
.prod-card:hover { box-shadow: 0 4px 8px rgba(16, 185, 129, 0.2); border-color: #10B981; }
.prod-card h4 { color: #10B981; margin-top: 10px; font-family: sans-serif;}
.prod-card p { font-size: 0.9rem; color: #444; }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==========================================
# 2. القائمة الجانبية ومفتاح Groq
# ==========================================
with st.sidebar:
    st.markdown("# 🧴 مختبرات Massilya")
    st.markdown("---")
    if st.button("🗑️ استقبال زبون جديد"):
        st.session_state.messages = [{"role": "assistant", "content": "مرحباً بكم في Massilya!🧴 كيف يمكنني مساعدتكم اليوم في اختيار المنتج الأنسب لبشرتكم؟"}]
        st.rerun() 
    st.markdown("---")
    st.caption("Powered by Sharif AI Solutions")

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# 3. الواجهة (اللوغو والترويسة)
# ==========================================
cols = st.columns([1, 2, 1])
with cols[1]:
    try:
        logo = Image.open("logo.jpg.jpg") # اسم صورة اللوغو
        st.image(logo, use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ اللوغو غير موجود، تأكد من رفع صورة باسم 'logo.jpg.jpg'.")

st.markdown("<h1 style='text-align: center; color: #065F46; font-size: 2.2rem;'>مختبرات Massilya - خبيرك الرقمي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #10B981; font-size: 1.1rem;'>العناية بالبشرة، التجميل، والتغذية - استشارة احترافية 24/7</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 4. قسم تعريف المنتجات (البطاقات)
# ==========================================
st.markdown("<h2 style='text-align: right; color: #065F46;'>✨ تشكيلة منتجاتنا المتخصصة</h2>", unsafe_allow_html=True)

prod_cols = st.columns(4)
# المنتجات المعروضة في الواجهة
placeholders = [
    {"name": "كريم 30% يوريا", "desc": "علاج جلد الدجاجة والشعر تحت الجلد"},
    {"name": "محلول تساقط الشعر", "desc": "بزيت إكليل الجبل وفيتامين B5"},
    {"name": "غسول مقشر (الأسود)", "desc": "2% حمض الساليسيليك ضد حب الشباب"},
    {"name": "شامبو ضد القشرة", "desc": "علاج نهائي للقشرة وحكة الفروة"},
    {"name": "غسول للبشرة الدهنية", "desc": "بالألوفيرا لتقليل إفراز الدهون"},
    {"name": "غسول للبشرة الجافة", "desc": "خالي من الصابون والسلفات"},
    {"name": "كريم الاستحمام", "desc": "غني بزيت اللوز الحلو لرغوة حريرية"},
    {"name": "جل الاستحمام", "desc": "ترطيب 100% بتركيز غليسيرين 5%"}
]

for i, prod in enumerate(placeholders):
    with prod_cols[i % 4]:
        st.markdown(f"""
        <div class="prod-card">
            <div style="font-size: 3rem; color: #10B981;">🧴</div>
            <h4>{prod['name']}</h4>
            <p>{prod['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 5. المندوب الذكي (منطق Llama 3.3 + Telegram)
# ==========================================
st.markdown("<h2 style='text-align: right; color: #065F46;'>💬 استشارة العناية بالبشرة</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بيك في Massilya!🧴 واش راكي حابة تستفسري اليوم على بشرتك ولا شعرك؟"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("اكتبوا سؤالكم لخبير Massilya الآلي..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⏳ الخبير يحلل نوع بشرتك..."):
            
            # --- برمجة شخصية مندوب Massilya ---
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_instruction = f"""
            أنت خبير مبيعات جزائري من العاصمة تعمل في 'Massilya Dermo-Cosmétiques'.
            
            [قواعد التحدث الإجبارية - الدارجة الجزائرية فقط]:
            1. يجب أن تستخدم هذه الكلمات حصرياً: (واش راكي، ختي، خويا، حابة، مليح، هايل، هكذا، درك، باش، شحال، بزاف، يعطيك الصحة، بلا مزية).
            2. إدمج بعض الكلمات الفرنسية بأسلوب جزائري: (D'accord, Bien sûr, La peau, Le visage, Normalement, La livraison).
            3. إذا أردت قول "بكام" قل: "بشحال".
            4. إذا أردت قول "عايزة" قل: "واش راكي حابة".
            5. إذا أردت قول "كويس" قل: "هايل" أو "مليح".
            6. تكلم بإجابات قصيرة ومباشرة، ولا تكن روبوتياً.
            7. هدفك: إقناع الزبونة وأخذ (الاسم، الولاية، رقم الهاتف). التوصيل: العاصمة 400 دج، وباقي الولايات 600 دج.
            
            [أمثلة إجبارية لطريقة الرد]:
            الزبون: سلام عندي الحبوب في وجهي
            أنت: وعليكم السلام ختي، مرحبا بيك. على جال الحبوب ننصحك بالغسول الأسود المقشر (950 دج)، راهو هايل وينحي لي بوان نوار. تحبي نكونفيرميلك لاكوموند؟
            الزبون: شحال التوصيل؟
            أنت: التوصيل للعاصمة بـ 400 دج، وباقي الولايات 600 دج. ابعثيلي برك اسمك والولاية ورقم التيليفون باش نبعثوهالك d'accord؟
            
            [قائمة المنتجات الـ 12 المتوفرة]:
            1. غسول أصفر (للبشرة العادية/المختلطة): 500 دج.
            2. غسول أزرق (للبشرة الجافة/الحساسة): 500 دج.
            3. غسول أخضر (للبشرة الدهنية): 500 دج. بالألوفيرا.
            4. غسول أبيض/أزرق (ضد حب الشباب 1%): 500 دج.
            5. غسول أسود (مقشر قوي 2% BHA): 950 دج.
            6. شامبو ضد القشرة (DS): 750 دج.
            7. محلول ضد تساقط الشعر (Lotion): 1100 دج.
            8. شامبو للشعر الجاف والمتقصف: 800 دج.
            9. جل الاستحمام (للبشرة الجافة): 500 دج.
            10. كريم الاستحمام المرغي: 500 دج.
            11. كريم مقشر 30% يوريا: 850 دج. لجلد الدجاجة والشعر تحت الجلد.
            12. غسول PanOxyl (مستورد): 3,700 دج.
            """
            
            api_messages = [{"role": "system", "content": system_instruction}]
            for msg in st.session_state.messages:
                api_messages.append({"role": msg["role"], "content": msg["content"]})
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.3, 
                    max_completion_tokens=1024,
                    top_p=1,
                    stream=False 
                )
                
                answer = completion.choices[0].message.content
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # --- جاسوس التليجرام ---
                try:
                    bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                    chat_id = "5111187631"
                    digits_count = sum(char.isdigit() for char in prompt)
                    
                    if digits_count >= 8:
                        spy_message = f"💰🚨 طلبية جديدة لمختبرات Massilya!\n\n👤 رسالة الزبون:\n{prompt}\n\n🤖 رد المندوب:\n{answer}"
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": spy_message})
                except:
                    pass
                    
            except Exception as e:
                st.error("الخبير مشغول قليلاً، حاول مجدداً.")
