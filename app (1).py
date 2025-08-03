import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Refresh dell'app ogni secondo per aggiornare il timer locale
count = st_autorefresh(interval=1000, limit=None, key="timer_refresh")

# Funzione per inizializzare e caricare la data da Google Sheets una sola volta
def load_start_time():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(
        st.secrets["GSPREAD_CREDS"],
        scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1wGmd1x0DlCvBppFdnlckXiqPZ1Jagtxrq5aM9-puoMw").sheet1
    start_time_str = sheet.acell("A1").value
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    return start_time

# Carica start_time solo se non è già in session_state
if "start_time" not in st.session_state:
    try:
        st.session_state.start_time = load_start_time()
    except Exception as e:
        st.error(f"Errore nel caricamento del timer: {e}")
        st.stop()

# Calcola tempo trascorso localmente
now = datetime.now()
delta = now - st.session_state.start_time

days = delta.days
hours = delta.seconds // 3600
minutes = (delta.seconds % 3600) // 60
seconds = delta.seconds % 60

st.markdown(f"<h1 style='font-size: 48px;'>⏳ Giorni senza pizza: {days}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='font-size: 36px;'>{hours:02}:{minutes:02}:{seconds:02}</h2>", unsafe_allow_html=True)

if st.button("🔄 Resetta timer"):
    try:
        # Calcolo il tempo attuale al momento del click
        now_reset = datetime.now()

        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(
            st.secrets["GSPREAD_CREDS"],
            scopes=scope
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1wGmd1x0DlCvBppFdnlckXiqPZ1Jagtxrq5aM9-puoMw").sheet1

        now_str = now_reset.strftime("%Y-%m-%d %H:%M:%S")
        sheet.update("A1", [[now_str]])

        st.session_state.start_time = now_reset  # aggiorno la session state con il valore corretto
    except Exception as e:
        st.error(f"Errore nel resettare il timer: {e}")

