import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("Chatbot AI dengan Gemini")

# Sidebar untuk keamanan API Key
with st.sidebar:
    st.header("Konfigurasi")
    api_key = st.text_input("Masukkan Google API Key", type="password")
    st.markdown("[Dapatkan API Key di Google AI Studio](https://aistudio.google.com/app/apikey)")

# Hentikan eksekusi jika API Key belum dimasukkan
if not api_key:
    st.info("Silakan masukkan API Key di bilah samping kiri untuk mulai mengobrol.")
    st.stop()

# Konfigurasi SDK Google
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 2. Inisialisasi memori Streamlit dan sesi chat Gemini
if "messages" not in st.session_state:
    st.session_state.messages = []
    # start_chat menyimpan riwayat percakapan di memori model Gemini
    st.session_state.gemini_chat = model.start_chat(history=[])

# 3. Tampilkan riwayat pesan di antarmuka (UI)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Tangkap input teks dari pengguna
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    
    # Tampilkan pesan pengguna di UI dan simpan di memori Streamlit
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 5. Hubungkan ke API Gemini dan tampilkan respons
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Kirim pesan ke Gemini API (stream=True agar muncul per kata seperti sedang mengetik)
            response = st.session_state.gemini_chat.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            # Tampilkan hasil akhir tanpa kursor blok
            message_placeholder.markdown(full_response)
            
            # Simpan respons bot ke memori Streamlit
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menghubungi API: {e}")
