import streamlit as st
import requests

# 1. Sayfa Yapılandırması
st.set_page_config(
    page_title="OSMAN ÇAVUŞ M.T.AL TOPLU SMS SİSTEMİ", 
    page_icon="🏫", 
    layout="wide"
)

# Sabit İlkSMS API Bilgileri
API_USERNAME = "3CW2PY7IEAQV6LGU5THOJR9M4ZKN0DFB18S"
API_PASSWORD = "UIRKWT26G1B4V8LOY37P9C5JFDSQZ0AMHEN"
API_HEADER = "O.CAVUSMTAL"

# Bakiye Sorgulama Fonksiyonu
def get_credit():
    test_payload = {
        "apiUsername": API_USERNAME,
        "apiPassword": API_PASSWORD
    }
    try:
        r = requests.post(
            "https://app.ilksms.com/api/kullanicibilgi", 
            json=test_payload, 
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if r.status_code == 200:
            res = r.json()
            if isinstance(res, dict):
                for key in ["credit", "bakiye", "kredi", "sms", "balance", "kontor"]:
                    if key in res and res[key] is not None:
                        return str(res[key])
                if "data" in res and isinstance(res["data"], dict):
                    for key in ["credit", "bakiye", "kredi"]:
                        if key in res["data"] and res["data"][key] is not None:
                            return str(res["data"][key])
    except Exception as e:
        print("Bakiye Sorgu Hatası:", e)
    return "Yüklenemedi"

# Session State Hazırlıkları
if "credit_amount" not in st.session_state:
    st.session_state["credit_amount"] = get_credit()

if "tpl_1" not in st.session_state:
    st.session_state["tpl_1"] = ""
if "tpl_2" not in st.session_state:
    st.session_state["tpl_2"] = ""
if "tpl_3" not in st.session_state:
    st.session_state["tpl_3"] = ""

if "selected_tpl_key" not in st.session_state:
    st.session_state["selected_tpl_key"] = "tpl_1"
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False

# 2. Özel CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none !important;}
    
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    label, p, span, h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 600;
    }
    
    input, textarea {
        color: #0f172a !important;
        background-color: #ffffff !important;
        border: 1px solid #94a3b8 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #94a3b8 !important;
        color: #0f172a !important;
    }
    div[data-baseweb="select"] span {
        color: #0f172a !important;
    }

    div[data-baseweb="popover"], 
    div[data-baseweb="menu"], 
    ul[role="listbox"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
    }

    li[role="option"], 
    li[role="option"] * {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    li[role="option"]:hover, 
    li[role="option"]:hover *,
    li[role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"] * {
        background-color: #2563eb !important;
        color: #ffffff !important;
    }

    .balance-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        padding: 12px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
        text-align: center;
    }
    .balance-card * {
        color: white !important;
    }

    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        height: 52px;
        border: none;
        box-shadow: 0 4px 10px rgba(29, 78, 216, 0.3);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1e40af !important;
        box-shadow: 0 6px 14px rgba(30, 64, 175, 0.4);
    }
    .stButton>button p {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- ÜST BAŞLIK & BAKIYE KARTI ---
h_col1, h_col2 = st.columns([3.8, 1.2])
with h_col1:
    st.markdown("<h2 style='margin-bottom: 0px; color: #0f172a; font-weight: 800;'>🏫 OSMAN ÇAVUŞ M.T.AL TOPLU SMS SİSTEMİ</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #334155; font-size: 15px; font-weight: 500;'>Öğrenci numaralarını girerek hızlı ve toplu SMS gönderimi yapın.</p>", unsafe_allow_html=True)
with h_col2:
    st.markdown(f"""
        <div class="balance-card">
            <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9;">Kullanılabilir Bakiye</div>
            <div style="font-size: 22px; font-weight: 800; margin-top: 2px;">💳 {st.session_state['credit_amount']} SMS</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 15px 0 25px 0; border-color: #cbd5e1;'>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.2], gap="large")

# --- SOL KOLON: 20 Adet Okul Numarası Kutusu ---
with col_left:
    st.markdown("<h3 style='color: #0f172a; font-size: 18px; font-weight: 700;'>🎓 Öğrenci Okul Numaraları</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #334155; font-size: 14px; margin-bottom: 15px;'>SMS gönderilecek öğrenci numaralarını giriniz (Max 20 Öğrenci).</p>", unsafe_allow_html=True)
    
    school_numbers = []
    grid_col1, grid_col2 = st.columns(2)
    
    for i in range(1, 21):
        target_col = grid_col1 if i % 2 != 0 else grid_col2
        with target_col:
            okul_no = st.text_input(
                f"Öğrenci No #{i}", 
                placeholder="",
                key=f"okul_no_{i}",
                label_visibility="visible"
            )
            cleaned_no = okul_no.strip()
            if cleaned_no:
                school_numbers.append(cleaned_no)

# --- SAĞ KOLON: Şablon Yönetimi & Mesaj İçeriği ---
with col_right:
    st.markdown("<h3 style='color: #0f172a; font-size: 18px; font-weight: 700;'>📝 Şablon Düzenleme & Mesaj Metni</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #334155; font-size: 14px;'>Aşağıdaki boş şablon kutularına tıklayıp yeni metin ekleyebilirsiniz:</p>", unsafe_allow_html=True)
    
    templates_data = [
        ("tpl_1", "Şablon 1"),
        ("tpl_2", "Şablon 2"),
        ("tpl_3", "Şablon 3")
    ]
    
    tpl_cols = st.columns(3)
    for idx, (tpl_key, tpl_title) in enumerate(templates_data):
        with tpl_cols[idx]:
            is_selected = (st.session_state["selected_tpl_key"] == tpl_key)
            
            border_style = "2px solid #1d4ed8" if is_selected else "1px solid #94a3b8"
            bg_style = "#dbeafe" if is_selected else "#ffffff"
            title_color = "#1e40af" if is_selected else "#0f172a"
            
            content_display = st.session_state[tpl_key] if st.session_state[tpl_key].strip() else "<i>(Boş Şablon)</i>"
            
            st.markdown(f"""
                <div style="border: {border_style}; background-color: {bg_style}; padding: 10px; border-radius: 8px; min-height: 100px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="font-weight: 700; font-size: 13px; color: {title_color}; margin-bottom: 4px;">{tpl_title}</div>
                    <div style="font-size: 12px; color: #334155; word-wrap: break-word; line-height: 1.3;">
                        {content_display}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns([2, 1])
            with btn_col1:
                if st.button("Seç", key=f"select_{tpl_key}"):
                    st.session_state["selected_tpl_key"] = tpl_key
                    st.rerun()
            with btn_col2:
                if st.button("✏️", key=f"edit_btn_{tpl_key}"):
                    st.session_state["selected_tpl_key"] = tpl_key
                    st.session_state["edit_mode"] = True
                    st.rerun()

    # Düzenleme Alanı
    if st.session_state.get("edit_mode", False):
        curr_key = st.session_state["selected_tpl_key"]
        st.info(f"✏️ {curr_key.replace('tpl_', 'Şablon ').upper()} Metnini Düzenliyorsunuz:")
        new_tpl_text = st.text_area("Şablon Metni Yazın:", value=st.session_state[curr_key], height=100)
        
        save_col1, save_col2 = st.columns(2)
        with save_col1:
            if st.button("💾 Şablonu Kaydet"):
                st.session_state[curr_key] = new_tpl_text
                st.session_state["edit_mode"] = False
                st.success("Şablon kaydedildi!")
                st.rerun()
        with save_col2:
            if st.button("❌ İptal"):
                st.session_state["edit_mode"] = False
                st.rerun()

    # Aktif Şablondan Metni Al
    selected_text = st.session_state[st.session_state["selected_tpl_key"]]

    active_message = st.text_area(
        "✉️ Gönderilecek Mesaj Metni:", 
        value=selected_text,
        height=130,
        placeholder="Göndermek istediğiniz mesajı buraya yazın veya yukarıdan şablon seçin..."
    )

    st.markdown("<hr style='margin: 15px 0; border-color: #cbd5e1;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #0f172a; font-size: 18px; font-weight: 700;'>⚙️ Gönderim Ayarları</h3>", unsafe_allow_html=True)
    
    # Mesaj Alıcısı
    veli_options = [
        ("1", "Sadece 1. Veli"),
        ("2", "Sadece 2. Veli"),
        ("12", "Her İkisi de")
    ]
    
    veli_tur_val = st.selectbox(
        "Mesaj Alıcısı Seçiniz:",
        options=veli_options,
        format_func=lambda x: x[1]
    )[0]

    char_tur_val = "turkce"

    st.markdown("<br>", unsafe_allow_html=True)
    
    # GÖNDER BUTONU
    if st.button("SMS GÖNDER"):
        if not school_numbers:
            st.warning("Lütfen sol taraftan en az 1 adet Okul Numarası giriniz!")
        elif not active_message.strip():
            st.warning("Lütfen gönderilecek mesaj metnini doldurunuz!")
        else:
            success_list = []
            failed_list = []

            with st.spinner("Numaralar kontrol ediliyor ve SMS'ler gönderiliyor..."):
                for single_no in school_numbers:
                    payload = {
                        "apiUsername": API_USERNAME,
                        "apiPassword": API_PASSWORD,
                        "baslik": API_HEADER,
                        "mesaj": str(active_message).strip(),
                        "veliTur": str(veli_tur_val),
                        "tur": str(char_tur_val),
                        "okulNumaralari": str(single_no),
                        "rehberTur": "0"
                    }

                    try:
                        url = "https://app.ilksms.com/api/okulnosms"
                        response = requests.post(
                            url, 
                            json=payload,
                            headers={"Content-Type": "application/json"},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            res_data = response.json()
if str(res_data.get("state")).lower() == "true":
    requestsdata.get("code") == 200:
                                success_list.append(single_no)
                            else:
                                failed_list.append(single_no)
                        else:
                            failed_list.append(single_no)
                    except Exception:
                        failed_list.append(single_no)

            # Başarılı Gönderimler (Ekranda Kalıcı Durur)
            if success_list:
                st.success(f"✅ SMS Gönderilen Numaralar: **{', '.join(success_list)}**")
            
            # Başarısız Gönderimler (Ekranda Kalıcı Durur)
            if failed_list:
                for no in failed_list:
                    st.error(f"❌ Okul No {no}: SMS Başarısız")

            # Bakiyeyi sessizce güncelle (Sayfayı yenilemeden)
            st.session_state["credit_amount"] = get_credit()
