import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import requests
from datetime import datetime
import base64
import os

# ==========================================
# 1. إعدادات الصفحة الفاخرة والتمويه
# ==========================================
st.set_page_config(
    page_title="Massilya Dermo-Cosmétiques | المندوب الخبير", 
    page_icon="🧴", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# دالة تشفير الصور لتعمل داخل السلايدر المعزول والشريط الثابت
def get_image_base64(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

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
        st.session_state.messages = [{"role": "assistant", "content": "أهلاً ومرحباً بكم في مختبرات Massilya! 🧴 أنا خبير العناية بالبشرة والشعر. كيف يمكنني مساعدتكم اليوم؟"}]
        st.rerun() 
    st.markdown("---")
    st.caption("Powered by Sharif AI Solutions")

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# 3. الواجهة (الشريط العلوي الثابت - Sticky Header)
# ==========================================
logo_b64 = get_image_base64("logo.jpg.jpg") 

if logo_b64:
    header_html = f"""
    <style>
    /* تصميم الشريط العلوي الثابت */
    .sticky-header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 99999;
        display: flex;
        align-items: center;
        padding: 10px 20px;
        direction: rtl;
    }}
    .header-logo {{
        height: 45px;
        margin-left: 15px;
        border-radius: 5px;
    }}
    .header-title {{
        color: #065F46;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0;
        font-family: 'Cairo', sans-serif;
    }}
    /* إزاحة المحتوى للأسفل لكي لا يغطيه الشريط الثابت */
    .block-container {{
        padding-top: 80px !important; 
    }}
    </style>

    <div class="sticky-header">
        <img src="data:image/jpeg;base64,{logo_b64}" class="header-logo" alt="Massilya Logo">
        <p class="header-title">مختبرات Massilya</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
else:
    st.warning("⚠️ اللوغو غير موجود، تأكد من رفع صورة باسم 'logo.jpg.jpg'.")

st.markdown("<h3 style='text-align: center; color: #10B981; margin-top: 10px;'>استشارة احترافية 24/7</h3>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 4. قسم تعريف المنتجات (السلايدر المعزول الآمن)
# ==========================================
st.markdown("<h2 style='text-align: right; color: #065F46;'>✨ تشكيلة منتجاتنا المتخصصة</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right; color: #666;'>👈 اسحب لليمين واليسار لتصفح المنتجات</p>", unsafe_allow_html=True)

placeholders = [
    {"name": "كريم 30% يوريا", "desc": "علاج جلد الدجاجة والشعر تحت الجلد", "img_file": "chicken.jpeg"},
    {"name": "محلول تساقط الشعر", "desc": "بزيت إكليل الجبل وفيتامين B5", "img_file": "produit.jpeg"},
    {"name": "غسول مقشر (الأسود)", "desc": "2% حمض الساليسيليك ضد حب الشباب", "img_file": "2acide.jpeg"},
    {"name": "شامبو ضد القشرة", "desc": "علاج نهائي للقشرة وحكة الفروة", "img_file": "champo.png"},
    {"name": "غسول للبشرة الدهنية", "desc": "بالألوفيرا لتقليل إفراز الدهون", "img_file": "oily.jpeg"},
    {"name": "غسول للبشرة الجافة", "desc": "خالي من الصابون والسلفات", "img_file": "dry.png"},
    {"name": "غسول لحب الشباب", "desc": "تنظيف عميق للبشرة المعرضة لحب الشباب", "img_file": "hab chbab.png"},
    {"name": "جل الاستحمام", "desc": "ترطيب 100% بتركيز غليسيرين 5%", "img_file": "jel.png"}
]

# كود HTML المعزول (Iframe)
html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { margin: 0; padding: 0; font-family: sans-serif; background-color: transparent; }
    .slider-container {
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        gap: 15px;
        padding: 15px 5px 25px 5px;
        scrollbar-width: thin; 
        scrollbar-color: #10B981 transparent;
    }
    .slider-container::-webkit-scrollbar { height: 8px; }
    .slider-container::-webkit-scrollbar-track { background: transparent; }
    .slider-container::-webkit-scrollbar-thumb { background-color: #10B981; border-radius: 10px; }
    
    .slider-card {
        flex: 0 0 240px;
        scroll-snap-align: start;
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #A7F3D0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .slider-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(16, 185, 129, 0.2);
        border-color: #10B981;
    }
    .slider-img {
        width: 100%;
        height: 180px;
        object-fit: contain;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    h4 { color: #10B981; margin: 10px 0 5px 0; font-size: 1.1rem; }
    p { font-size: 0.85rem; color: #444; margin: 0; line-height: 1.4; }
</style>
</head>
<body>
<div class="slider-container" dir="rtl">
"""

for prod in placeholders:
    img_b64 = get_image_base64(prod['img_file'])
    if img_b64:
        ext = prod['img_file'].split('.')[-1].lower()
        mime_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
        img_src = f"data:{mime_type};base64,{img_b64}"
    else:
        # صورة شفافة فارغة كاحتياطي إذا لم يجد الملف
        img_src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        
    html_code += f"""
    <div class="slider-card">
        <img src="{img_src}" class="slider-img" alt="{prod['name']}">
        <h4>{prod['name']}</h4>
        <p>{prod['desc']}</p>
    </div>
    """

html_code += """
</div>
</body>
</html>
"""

# عرض الكود داخل نافذة معزولة آمنة (Iframe) بارتفاع مناسب
components.html(html_code, height=360, scrolling=False)

st.markdown("---")

# ==========================================
# 5. المندوب الذكي (منطق Llama 3.3 + Telegram)
# ==========================================
st.markdown("<h2 style='text-align: right; color: #065F46;'>💬 استشارة العناية بالبشرة</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً ومرحباً بكم في مختبرات Massilya! 🧴 أنا خبير العناية بالبشرة والشعر. كيف يمكنني مساعدتكم اليوم؟"}
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
            
            # --- برمجة شخصية مندوب Massilya (الفصحى الاحترافية) ---
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_instruction = f"""
            أنت خبير مبيعات وطبيب أمراض جلدية تعمل في مختبرات 'Massilya Dermo-Cosmétiques' في الجزائر. تاريخ اليوم هو {current_date}.
            
            [قواعد التحدث الإجبارية 🚨]: 
            1. تحدث باللغة العربية الفصحى المبسطة، الواضحة، والمهنية جداً.
            2. كن لبقاً مثل طبيب حقيقي يرحب بمرضاه (مثال: أهلاً بك يا سيدتي، يسعدني مساعدتك، أنصحك بـ...).
            3. إجاباتك يجب أن تكون قصيرة، مباشرة، وتركز على حل مشكلة الزبون.
            4. هدفك النهائي: تشخيص المشكلة بناءً على رسالة الزبون، اقتراح المنتج المناسب، وأخذ (الاسم، الولاية، ورقم الهاتف) لتأكيد الطلب. 
            5. تكلفة التوصيل: العاصمة 400 دج، وباقي ولايات الجزائر 600 دج.
            6. [تنبيه حاسم جداً]: كلمة "غسول" تُطلق حصرياً على منتجات الوجه. أما كلمة "جل استحمام" فتُطلق حصرياً على منتجات تنظيف الجسم. لا تخلط بينهما أبداً عند نصح الزبون.
            
            [أمثلة لطريقة الرد]:
            - الزبون: أعاني من حب الشباب في وجهي.
            - أنت: أهلاً بك. للتخلص من حب الشباب، أنصحك بشدة بالغسول الأسود المقشر (بتركيز 2% BHA) بسعر 950 دج، أو غسول 'hab chbab' المتخصص بسعر 500 دج. هل أرسل لك عبوة؟
            
            [قائمة المنتجات الـ 12 المتوفرة فقط]:
            🧴 قسم العناية بالوجه:
            1. غسول أصفر (للبشرة العادية/المختلطة): 500 دج.
            2. غسول أزرق (للبشرة الجافة/الحساسة): 500 دج.
            3. غسول أخضر (للبشرة الدهنية): 500 دج. بالألوفيرا.
            4. غسول أبيض/أزرق (ضد حب الشباب الخفيف 1%): 500 دج.
            5. غسول أسود (مقشر قوي 2% BHA): 950 دج.
            
            💆‍♀️ قسم العناية بالشعر:
            6. شامبو ضد القشرة (DS): 750 دج.
            7. محلول ضد تساقط الشعر (Lotion): 1100 دج.
            8. شامبو للشعر الجاف والمتقصف: 800 دج.
            
            🛁 قسم العناية بالجسم:
            9. جل الاستحمام (للبشرة الجافة): 500 دج. غليسيرين 5%.
            10. غسول لحب الشباب (hab chbab): 500 دج. تنظيف عميق للبشرة المعرضة لحب الشباب.
            11. كريم مقشر 30% يوريا: 850 دج. ممتاز لجلد الدجاجة والشعر تحت الجلد.
            12. غسول PanOxyl (مستورد): 3,700 دج.
            """
            
            api_messages = [{"role": "system", "content": system_instruction}]
            for msg in st.session_state.messages:
                api_messages.append({"role": msg["role"], "content": msg["content"]})
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.4, 
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
