import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Pakar PLTS & Energi", page_icon="☀️")
st.title("☀️ Chatbot Asisten PLTS & Energi Berkelanjutan")
st.markdown("Tanyakan apa saja tentang Pembangkit Listrik Tenaga Surya, analisis performa, hingga integrasi AI.")

# Sidebar untuk keamanan API Key
with st.sidebar:
    st.header("Konfigurasi API")
    api_key = st.text_input("Masukkan Google API Key", type="password")
    
if not api_key:
    st.info("Silakan masukkan API Key di bilah samping kiri untuk mulai belajar.")
    st.stop()

genai.configure(api_key=api_key)

# 1. MENAMBAHKAN SYSTEM PROMPT KHUSUS PLTS
system_prompt = """
Anda adalah seorang asisten AI ahli di bidang Pembangkit Listrik Tenaga Surya (PLTS), Sistem Energi Berkelanjutan, dan Konservasi Energi. 
Tugas utama Anda adalah menjadi tutor dan rekan diskusi yang andal.

Keahlian khusus Anda meliputi:
- Konsep dasar hingga lanjutan mengenai fotovoltaik (PV).
- Sistem monitoring cerdas dan penerapan arsitektur PV-Digital Twin (PVDT).
- Analisis performa sistem kelistrikan dan evaluasi kapasitas (misalnya skala 10 kWp).
- Integrasi Machine Learning untuk sistem PV, termasuk penggunaan Random Forest, Isolation Forest, GNN, dan LSTM untuk deteksi anomali serta prediksi daya.

Berikan penjelasan yang terstruktur, teknis namun mudah dipahami, dan gunakan istilah keteknikan yang tepat.
"""

# 2. MEMASUKKAN SYSTEM PROMPT KE DALAM MODEL
# Catatan: system_instruction didukung pada model gemini-1.5 ke atas.
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=system_prompt
)

# Inisialisasi memori
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.gemini_chat = model.start_chat(history=[])

# Tampilkan riwayat pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Tangkap input teks dari pengguna
if prompt := st.chat_input("Tanyakan tentang performa PV, Digital Twin, atau prediksi daya..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Hubungkan ke API Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = st.session_state.gemini_chat.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
