import streamlit as st
import google.generativeai as genai

# إعدادات الواجهة
st.set_page_config(page_title="تطبيق الذكاء الاصطناعي", page_icon="🤖", layout="centered")

st.title("🤖 مساعدك الذكي")
st.caption("تطبيق ذكاء اصطناعي يعمل عبر Gemini API")

# إدخال مفتاح الـ API
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

if not api_key:
    st.info("⚠️ يرجى إدخال مفتاح API في القائمة الجانبية للبدء.", icon="🔑")
    st.stop()

# تهيئة النموذج
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # إضافة سؤال المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد من الذكاء الاصطناعي
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
