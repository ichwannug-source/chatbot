import streamlit as st
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Aplikasi Chatbot", page_icon="🤖")
st.title("Chatbot Sederhana")

# 2. Inisialisasi memori obrolan (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Tampilkan riwayat pesan sebelumnya di layar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Tangkap input teks dari pengguna
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    
    # Tampilkan pesan pengguna di UI
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Simpan pesan pengguna ke memori
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 5. Buat dan tampilkan respons bot
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Contoh respons statis (Di sinilah Anda akan memasukkan logika LLM/AI nantinya)
        assistant_response = f"Saya menerima pesan Anda: '{prompt}'. Sistem AI belum terhubung."
        
        # Simulasi efek mengetik (stream)
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Simpan respons bot ke memori
    st.session_state.messages.append({"role": "assistant", "content": full_response})
