import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman (Harus selalu di baris paling atas)
st.set_page_config(page_title="PVDT Assistant", page_icon="☀️", layout="centered")

# 2. Injeksi Custom CSS untuk Tema Hijau-Kuning-Biru
custom_css = """
<style>
    /* Mengubah warna latar belakang Sidebar (Gradasi Hijau Muda ke Biru Muda) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E8F5E9 0%, #E3F2FD 100%);
    }
    
    /* Mengubah warna Judul Utama (Biru Laut) */
    h1 {
        color: #0277BD !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Mempercantik area input chat (Garis tepi Hijau Daun) */
    [data-testid="stChatInput"] {
        border: 2px solid #4CAF50 !important;
        border-radius: 15px !important;
        background-color: #FAFAFA !important;
    }
    
    /* Mengubah warna garis pemisah (Kuning Matahari) */
    hr {
        border: 0;
        height: 3px;
        background-image: linear-gradient(to right, rgba(251, 192, 45, 0), rgba(251, 192, 45, 0.75), rgba(251, 192, 45, 0));
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Menyorot teks petunjuk di sidebar (Biru Gelap) */
    .sidebar-text {
        color: #01579B;
        font-weight: bold;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Antarmuka Utama
st.title("☀️ PVDT Assistant")
st.markdown("### Asisten AI untuk Analisis PLTS & Energi Berkelanjutan")
st.markdown("---") # Ini akan memanggil garis pemisah kuning dari CSS di atas

# 4. Sidebar dengan Elemen Warna
with st.sidebar:
    st.markdown("<h2 style='color: #2E7D32;'>Konfigurasi Sistem</h2>", unsafe_allow_html=True)
    api_key = st.text_input("Masukkan Google API Key", type="password")
    
    st.markdown("""
    <div style='background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; margin-top: 20px;'>
        <span style='color: #F57F17; font-size: 14px;'><b>Tips:</b> Pastikan API Key yang Anda gunakan memiliki awalan <b>AQ.</b> atau <b>AIza</b>.</span>
    </div>
    """, unsafe_allow_html=True)
    
if not api_key:
    st.warning("Silakan masukkan API Key di bilah samping kiri untuk mulai berdiskusi.")
    st.stop()

genai.configure(api_key=api_key)

# 5. Instruksi Sistem Model
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

# Konfigurasi Model
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-001',
    system_instruction=system_prompt
)

# 6. Inisialisasi Memori
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.gemini_chat = model.start_chat(history=[])

# Tampilkan riwayat pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Tangkap dan Proses Input
if prompt := st.chat_input("Ketik pertanyaan seputar anomali data, efisiensi PV, atau prediksi daya..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

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
            st.error(f"Terjadi kesalahan saat menghubungi server: {e}")
