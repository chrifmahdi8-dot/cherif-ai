import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import google.generativeai as genai
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

# ==========================================
# 🚨 إخفاء جميع علامات Streamlit (حاسوب + هاتف) 🚨
# ==========================================
hide_streamlit_style = """
<style>
/* إخفاء القائمة الرئيسية والفوتر */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* إخفاء الهيدر (الأعلى) بالكامل */
header {visibility: hidden;}
[data-testid="stHeader"] {display: none !important;}

/* إخفاء أزرار Streamlit في الحاسوب والهاتف */
.stDeployButton {display: none !important;}
[data-testid="stAppDeployButton"] {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stDecoration"] {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}
div.stFooter, div[data-testid="stFooter"] {display: none !important;}

/* استهداف الزر المائي العائم في نسخة الهواتف */
.viewerBadge_container {display: none !important;}
.viewerBadge_link {display: none !important;}
div[class^="viewerBadge"] {display: none !important;}

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
# 2. إعداد المفاتيح السرية (نظام محمي ومزدوج)
# ==========================================
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    
    groq_client = Groq(api_key=GROQ_API_KEY)
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error("⚠️ يرجى إعداد المفاتيح السرية (Secrets) في إعدادات Streamlit.")
    st.stop()

# ==========================================
# 3. القائمة الجانبية 
# ==========================================
with st.sidebar:
    st.markdown("# 🧴 مختبرات Massilya")
    st.markdown("---")
    if st.button("🗑️ استقبال زبون جديد"):
        st.session_state.messages = [{"role": "assistant", "content": "أهلاً ومرحباً بكم في مختبرات Massilya! 🧴 أنا طبيب ومندوب مبيعات. كيف يمكنني مساعدتكم اليوم؟"}]
        st.rerun() 
    st.markdown("---")
    st.caption("Powered by Sharif AI Solutions")

# ==========================================
# 4. الواجهة (الشريط العلوي الثابت - البحث الذكي عن اللوغو)
# ==========================================
logo_b64 = None
for logo_name in ["logo.png", "logo.jpg", "logo.jpeg", "logo.jpg.jpg"]:
    logo_b64 = get_image_base64(logo_name)
    if logo_b64:
        break

if logo_b64:
    header_html = f"""
    <style>
    .sticky-header {{
        position: fixed; top: 0; left: 0; right: 0; background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px); box-shadow: 0 2px 10px rgba(0,0,0,0.1); z-index: 99999;
        display: flex; align-items: center; padding: 10px 20px; direction: rtl;
    }}
    .header-logo {{ height: 45px; margin-left: 15px; border-radius: 5px; }}
    .header-title {{ color: #065F46; font-size: 1.2rem; font-weight: bold; margin: 0; font-family: 'Cairo', sans-serif; }}
    .block-container {{ padding-top: 80px !important; }}
    </style>
    <div class="sticky-header">
        <img src="data:image/jpeg;base64,{logo_b64}" class="header-logo" alt="Massilya Logo">
        <p class="header-title">مختبرات Massilya</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #10B981; margin-top: 10px;'>استشارة طبية وتجميلية 24/7</h3>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 5. قسم تعريف المنتجات (السلايدر المعزول الآمن)
# ==========================================
st.markdown("<h2 style='text-align: right; color: #065F46;'>✨ تشكيلة منتجاتنا المتخصصة</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right; color: #666;'>👈 اسحب لليمين واليسار لتصفح المنتجات</p>", unsafe_allow_html=True)

placeholders = [
    {"name": "Crème 30% Urée", "desc": "علاج فعال لجلد الدجاجة والخشونة", "img_file": "chicken.jpeg"},
    {"name": "Lotion Anti-Chute", "desc": "محلول مكثف لعلاج تساقط الشعر", "img_file": "produit.jpeg"},
    {"name": "Gel Exfoliant 2% BHA", "desc": "مقشر قوي لحب الشباب (الأسود)", "img_file": "2acide.jpeg"},
    {"name": "Shampooing Anti-Pelliculaire", "desc": "علاج نهائي للقشرة وحكة الفروة", "img_file": "champo.png"},
    {"name": "Gel Nettoyant Purifiant", "desc": "منظف عميق للبشرة الدهنية", "img_file": "oily.jpeg"},
    {"name": "Gel Ultra Doux", "desc": "عناية فائقة للبشرة الجافة والحساسة", "img_file": "dry.png"},
    {"name": "Gel Peaux Acnéiques", "desc": "عناية يومية للبشرة المعرضة للحبوب", "img_file": "hab chbab.png"},
    {"name": "Crème de Douche", "desc": "كريم استحمام لترطيب الجسم", "img_file": "jel.png"}
]

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { margin: 0; padding: 0; font-family: sans-serif; background-color: transparent; }
    .slider-container { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 15px; padding: 15px 5px 25px 5px; scrollbar-width: thin; scrollbar-color: #10B981 transparent; }
    .slider-container::-webkit-scrollbar { height: 8px; }
    .slider-container::-webkit-scrollbar-thumb { background-color: #10B981; border-radius: 10px; }
    .slider-card { flex: 0 0 240px; scroll-snap-align: start; background-color: white; padding: 15px; border-radius: 15px; border: 2px solid #A7F3D0; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.3s; }
    .slider-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(16, 185, 129, 0.2); border-color: #10B981; }
    .slider-img { width: 100%; height: 180px; object-fit: contain; border-radius: 10px; margin-bottom: 10px; }
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
        img_src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    html_code += f'<div class="slider-card"><img src="{img_src}" class="slider-img"><h4>{prod["name"]}</h4><p>{prod["desc"]}</p></div>'

html_code += "</div></body></html>"
components.html(html_code, height=360, scrolling=False)
st.markdown("---")

# ==========================================
# 6. المندوب الذكي المزدوج (Groq الأساسي + Gemini الاحتياطي)
# ==========================================
st.markdown("<h2 style='text-align: right; color: #065F46;'>💬 استشارة العناية بالبشرة</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "أهلاً ومرحباً بكم في مختبرات Massilya! 🧴 أنا طبيب ومندوب مبيعات. كيف يمكنني مساعدتكم اليوم؟"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("اكتبوا سؤالكم لخبير Massilya الآلي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⏳ الخبير يجهز الرد..."):
            
            # --- برمجة شخصية مندوب Massilya (التوازن الذهبي: فوائد بدون جرائد) ---
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_instruction = f"""
            أنت طبيب أمراض جلدية وخبير مبيعات محترف تعمل في مختبرات 'Massilya Dermo-Cosmétiques' في الجزائر. 
            تاريخ اليوم هو {current_date}.
            
            [قواعد التحدث الإجبارية 🚨]: 
            1. تحدث باللغة العربية الفصحى المبسطة، الواضحة، والمهنية جداً، ولا تستخدم أحرف أجنبية وسط الكلام (إلا لاسم المنتج).
            2. كن لبقاً مثل طبيب حقيقي يرحب بمرضاه.
            3. [طول الإجابة]: إجاباتك يجب أن تكون **متوسطة الطول (حوالي 4 إلى 6 أسطر)**. لا تكتب مقالات أو "جرائد"، ولكن يجب أن **تشرح فوائد المنتج** بأسلوب طبي جذاب ليتحمس الزبون.
            4. استخدم دائماً الاسم التجاري الدقيق للمنتج باللغة الفرنسية.
            5. [منع الهلوسة 🛑]: يُمنع التحدث في مواضيع شخصية أو الرد على الاستفزازات. إذا سُئلت عن شيء غريب قل: "عذراً، أنا هنا فقط لتقديم استشارات حول منتجات Massilya".
            6. هدفك النهائي: تشخيص، اقتراح منتج بفوائده، وأخذ (الاسم، الولاية، ورقم الهاتف) لتأكيد الطلب. 
            7. تكلفة التوصيل: العاصمة 400 دج، وباقي الولايات 600 دج.
            
            [الكتالوج الرسمي لمنتجات Massilya المتوفرة]:
            🧴 الوجه:
            1. MASSILYA Gel Exfoliant Moussant 2% BHA (200ml) - 950 د.ج (مقشر قوي لحب الشباب والرؤوس السوداء).
            2. MASSILYA Gel Nettoyant Purifiant Peaux Grasses (250ml) - 500 د.ج (للبشرة الدهنية).
            3. MASSILYA Gel Nettoyant Visage Peaux Normales et Mixtes (250ml) - 500 د.ج (للبشرة العادية والمختلطة).
            4. MASSILYA Gel Nettoyant Visage Ultra Doux (250ml) - 500 د.ج (للبشرة الجافة والحساسة).
            5. MASSILYA Gel Moussant Pour Peaux Acnéiques (250ml) - 500 د.ج (للبشرة المعرضة لحب الشباب).
            
            💆‍♀️ الشعر:
            6. MASSILYA Lotion Anti Chute (150ml) - 1100 د.ج (محلول لتساقط الشعر).
            7. MASSILYA Shampooing Anti-Pelliculaire (200ml) - 750 د.ج (شامبو للقشرة العادية).
            8. MASSILYA Shampoing Cheveux Secs et Abimés (200ml) - 800 د.ج (للشعر الجاف والمتقصف).
            9. MASSILYA Shampooing Anti Pelliculaire PSO F (200ml) - 780 د.ج (مخصص لصدفية الشعر).
            
            🛁 الجسم:
            10. MASSILYA Crème Anti-Rugosité 30% Urée (120ml) - 850 د.ج (لجلد الدجاجة والخشونة).
            11. MASSILYA Lait Hydratant Emollient 5% Visage et Corps - 850 د.ج (مرطب للوجه والجسم).
            12. MASSILYA Lait Hydratant Emollient 10% Corps - 1050 د.ج (مرطب قوي للجسم شديد الجفاف).
            13. MASSILYA Crème de Douche Lavante (400ml) - 500 د.ج (كريم استحمام).
            """
            
            answer = ""
            
            try:
                api_messages = [{"role": "system", "content": system_instruction}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.4, # توازن ممتاز بين الذكاء والصرامة
                    max_completion_tokens=400, # يسمح بشرح الفوائد دون الثرثرة الطويلة
                    top_p=1,
                    stream=False 
                )
                answer = completion.choices[0].message.content

            except Exception as groq_error:
                try:
                    gemini_model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
                    gemini_history = []
                    for m in st.session_state.messages[:-1]:
                        role = "user" if m["role"] == "user" else "model"
                        gemini_history.append({"role": role, "parts": [m["content"]]})
                    
                    chat = gemini_model.start_chat(history=gemini_history)
                    response = chat.send_message(prompt)
                    answer = response.text
                except Exception as gemini_error:
                    answer = "عذراً، الأطباء في المختبر مشغولون حالياً. يرجى المحاولة بعد قليل! ⏳"

            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            try:
                bot_token = "8758469394:AAFnu5x88Bn1XZSPyEvninIoQ5-TB3JMpPw"
                chat_id = "5111187631"
                if sum(char.isdigit() for char in prompt) >= 8:
                    spy_message = f"💰🚨 طلبية جديدة لمختبرات Massilya!\n\n👤 رسالة الزبون:\n{prompt}\n\n🤖 تشخيص المندوب:\n{answer}"
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": spy_message})
            except:
                pass
