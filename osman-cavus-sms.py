import streamlit as st
import requests

# 1. Sayfa Yapılandırması
st.set_page_config(
    page_title="OSMAN ÇAVUŞ M.T.AL TOPLU SMS SİSTEMİ",
    page_icon="🏫",
    layout="wide"
)

# Özel Yüksek Kontrastlı CSS Kuralları
st.markdown("""
<style>
    /* Genel Metin Kontrastı */
    body, p, label, .stMarkdown {
        color: #1E293B !important;
        font-weight: 500;
    }
    
    /* Selectbox ve Input Metinleri */
    .stSelectbox div[data-baseweb="select"] div,
    .stTextInput input,
    .stTextArea textarea {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    /* Selectbox Açılır Menü Listesi Kontrastı */
    ul[role="listbox"] li {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #E2E8F0 !important;
    }
    
    /* Başlık Stil Yapılandırması */
    .main-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    
    /* Bakiye Kartı Stili */
    .balance-card {
        background-color: #F8FAFC;
        border: 2px solid #CBD5E1;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .balance-title {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
    }
    .balance-value {
        font-size: 1.4rem;
        color: #0F172A;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# API Sabitleri
API_URL_CREDIT = "https://www.ilksms.com/api/v1/get-credit"
API_URL_SMS = "https://www.ilksms.com/api/v1/send-sms"

# Session State Başlatma (Şablonlar ve Giriş Bilgileri)
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""
if "org_name" not in st.session_state:
    st.session_state["org_name"] = ""

if "template_1" not in st.session_state:
    st.session_state["template_1"] = ""
if "template_2" not in st.session_state:
    st.session_state["template_2"] = ""
if "template_3" not in st.session_state:
    st.session_state["template_3"] = ""

if "edit_t1" not in st.session_state:
    st.session_state["edit_t1"] = False
if "edit_t2" not in st.session_state:
    st.session_state["edit_t2"] = False
if "edit_t3" not in st.session_state:
    st.session_state["edit_t3"] = False

if "balance" not in st.session_state:
    st.session_state["balance"] = "Bilinmiyor"

# Bakiye Sorgulama Fonksiyonu
def check_balance(usr, pwd):
    if not usr or not pwd:
        return "Giriş Yapılmadı"
    payload = {
        "api_credentials": {
            "username": usr,
            "password": pwd
        }
    }
    try:
        response = requests.post(
            API_URL_CREDIT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            res_data = response.json()
            if str(res_data.get("state")).lower() == "true":
                return str(res_data.get("credit", "0"))
            else:
                return "Hata"
        return "Bağlantı Hatası"
    except Exception:
        return "Sorgu Hatası"

# --- ÜST BAŞLIK VE BAKİYE ALANI ---
col_head1, col_head2 = st.columns([3, 1])

with col_head1:
    st.markdown('<div class="main-header">OSMAN ÇAVUŞ M.T.AL TOPLU SMS SİSTEMİ</div>', unsafe_allow_html=True)

with col_head2:
    st.markdown(f"""
    <div class="balance-card">
        <div class="balance-title">SMS Bakiyesi</div>
        <div class="balance-value">{st.session_state['balance']}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- YAN MENÜ: İLKSMS GİRİŞ BİLGİLERİ ---
st.sidebar.header("🔑 API ve Hesaba Giriş")
st.session_state["username"] = st.sidebar.text_input("Kullanıcı Adı", value=st.session_state["username"])
st.session_state["password"] = st.sidebar.text_input("Şifre", type="password", value=st.session_state["password"])
st.session_state["org_name"] = st.sidebar.text_input("Başlık (Orginator)", value=st.session_state["org_name"])

if st.sidebar.button("Bakiye Güncelle"):
    st.session_state["balance"] = check_balance(st.session_state["username"], st.session_state["password"])

# --- ŞABLON DÜZENLEME BÖLÜMÜ ---
st.subheader("📝 Mesaj Şablon Yönetimi")

col_t1, col_t2, col_t3 = st.columns(3)

# Şablon 1
with col_t1:
    head_col1, head_col2 = st.columns([4, 1])
    head_col1.markdown("**Şablon 1**")
    if head_col2.button("✏️", key="btn_edit_t1"):
        st.session_state["edit_t1"] = not st.session_state["edit_t1"]
    
    if st.session_state["edit_t1"]:
        st.session_state["template_1"] = st.text_area("Şablon 1 Düzenle", value=st.session_state["template_1"], key="ta_t1", height=100)
    else:
        st.info(st.session_state["template_1"] if st.session_state["template_1"] else "Boş Şablon (Düzenlemek için ✏️ simgesine tıklayın)")

# Şablon 2
with col_t2:
    head_col1, head_col2 = st.columns([4, 1])
    head_col1.markdown("**Şablon 2**")
    if head_col2.button("✏️", key="btn_edit_t2"):
        st.session_state["edit_t2"] = not st.session_state["edit_t2"]
    
    if st.session_state["edit_t2"]:
        st.session_state["template_2"] = st.text_area("Şablon 2 Düzenle", value=st.session_state["template_2"], key="ta_t2", height=100)
    else:
        st.info(st.session_state["template_2"] if st.session_state["template_2"] else "Boş Şablon (Düzenlemek için ✏️ simgesine tıklayın)")

# Şablon 3
with col_t3:
    head_col1, head_col2 = st.columns([4, 1])
    head_col1.markdown("**Şablon 3**")
    if head_col2.button("✏️", key="btn_edit_t3"):
        st.session_state["edit_t3"] = not st.session_state["edit_t3"]
    
    if st.session_state["edit_t3"]:
        st.session_state["template_3"] = st.text_area("Şablon 3 Düzenle", value=st.session_state["template_3"], key="ta_t3", height=100)
    else:
        st.info(st.session_state["template_3"] if st.session_state["template_3"] else "Boş Şablon (Düzenlemek için ✏️ simgesine tıklayın)")

st.divider()

# --- ÖĞRENCİ NUMARALARI VE MESAJ GÖNDERİMİ ---
st.subheader("🎓 Öğrenci Okul Numaraları ve Mesaj Formu")

col_inputs, col_msg = st.columns([1, 1])

student_nos = []
with col_inputs:
    st.markdown("**Öğrenci Okul Numaraları (20 Adet)**")
    
    grid_cols = st.columns(2)
    for i in range(1, 21):
        c = grid_cols[0] if i <= 10 else grid_cols[1]
        val = c.text_input(f"Öğrenci {i} Okul No", key=f"s_no_{i}")
        if val.strip():
            student_nos.append(val.strip())

with col_msg:
    st.markdown("**Gönderilecek Mesaj**")
    
    template_options = ["Özel Mesaj Yazın", "Şablon 1", "Şablon 2", "Şablon 3"]
    selected_template = st.selectbox("Şablon Seçin", template_options)
    
    default_text = ""
    if selected_template == "Şablon 1":
        default_text = st.session_state["template_1"]
    elif selected_template == "Şablon 2":
        default_text = st.session_state["template_2"]
    elif selected_template == "Şablon 3":
        default_text = st.session_state["template_3"]
        
    final_message = st.text_area("Mesaj Metni", value=default_text, height=180)
    
    send_button = st.button("🚀 TOPLU SMS GÖNDER", type="primary", use_container_width=True)

# --- SMS GÖNDERİM MANTIĞI VE DÖNGÜSÜ ---
if send_button:
    if not st.session_state["username"] or not st.session_state["password"] or not st.session_state["org_name"]:
        st.error("Lütfen sol taraftaki menüden İlkSMS kullanıcı adı, şifre ve başlık bilgilerini eksiksiz girin!")
    elif not student_nos:
        st.warning("En az bir öğrenci okul numarası girmelisiniz!")
    elif not final_message.strip():
        st.warning("Gönderilecek mesaj metni boş olamaz!")
    else:
        success_list = []
        failed_list = []
        
        progress_bar = st.progress(0)
        total_students = len(student_nos)
        
        for idx, single_no in enumerate(student_nos):
            payload = {
                "api_credentials": {
                    "username": st.session_state["username"],
                    "password": st.session_state["password"]
                },
                "header": {
                    "orginator": st.session_state["org_name"]
                },
                "messages": [
                    {
                        "message": final_message,
                        "receivers": [single_no]
                    }
                ]
            }
            
            try:
                response = requests.post(
                    API_URL_SMS,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                if response.status_code == 200:
                    res_data = response.json()
                    if str(res_data.get("state")).lower() == "true":
                        success_list.append(single_no)
                    else:
                        failed_list.append(single_no)
                else:
                    failed_list.append(single_no)
            except Exception:
                failed_list.append(single_no)
            
            progress_bar.progress((idx + 1) / total_students)
        
        # Bakiye Bilgisini Yenile
        st.session_state["balance"] = check_balance(st.session_state["username"], st.session_state["password"])
        
        # Sonuç Bildirimleri
        if success_list:
            st.success(f"Başarıyla Gönderilenler ({len(success_list)} kişi): {', '.join(success_list)}")
        
        if failed_list:
            st.error(f"Başarısız / Rehberde Bulunamayan Numaralar ({len(failed_list)} kişi):")
            for f_no in failed_list:
                st.write(f"- Okul No **{f_no}**: SMS Başarısız")
