import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

count = st_autorefresh(interval=1000, limit=None, key="timer_refresh")

def load_time_from_sheet(cell):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(
        st.secrets["GSPREAD_CREDS"],
        scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1wGmd1x0DlCvBppFdnlckXiqPZ1Jagtxrq5aM9-puoMw").sheet1
    time_str = sheet.acell(cell).value
    if time_str is None:
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        sheet.update(cell, [[now_str]])
        return now
    else:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

# Carica dati da Google Sheets solo se:
# - Non presenti in session_state
# - Oppure è passato più di 60 secondi dall’ultimo caricamento
if "last_fetch" not in st.session_state or (datetime.now() - st.session_state.last_fetch) > timedelta(seconds=60):
    try:
        st.session_state.start_time_litigi = load_time_from_sheet("A1")
        st.session_state.start_time_gelato = load_time_from_sheet("B1")
        st.session_state.last_fetch = datetime.now()
    except Exception as e:
        st.error(f"Errore nel caricamento del timer litigi o gelato: {e}")
        st.stop()

now = datetime.now()

# Calcola tempi trascorsi senza fare una nuova chiamata all'API
delta_litigi = now - st.session_state.start_time_litigi
delta_gelato = now - st.session_state.start_time_gelato

# Funzione per estrarre giorni, ore, minuti, secondi
def format_delta(td):
    days = td.days
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    return days, hours, minutes, seconds

days_l, hours_l, minutes_l, seconds_l = format_delta(delta_litigi)
days_g, hours_g, minutes_g, seconds_g = format_delta(delta_gelato)

st.markdown(f"<h1>😠👊 Giorni senza litigare: {days_l}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2>{hours_l:02}:{minutes_l:02}:{seconds_l:02}</h2>", unsafe_allow_html=True)

if st.button("🔄 Resetta timer litigi"):
    try:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(
            st.secrets["GSPREAD_CREDS"],
            scopes=scope
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1wGmd1x0DlCvBppFdnlckXiqPZ1Jagtxrq5aM9-puoMw").sheet1
        sheet.update("A1", [[now_str]])
        st.session_state.start_time_litigi = datetime.now()
    except Exception as e:
        st.error(f"Errore nel resettare il timer litigi: {e}")

st.markdown(f"<h1>🥰😘 Giorni senza fare l'amore: {days_g}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2>{hours_g:02}:{minutes_g:02}:{seconds_g:02}</h2>", unsafe_allow_html=True)

if st.button("🔄 Resetta timer sesso"):
    try:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(
            st.secrets["GSPREAD_CREDS"],
            scopes=scope
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1wGmd1x0DlCvBppFdnlckXiqPZ1Jagtxrq5aM9-puoMw").sheet1
        sheet.update("B1", [[now_str]])
        st.session_state.start_time_gelato = datetime.now()
    except Exception as e:
        st.error(f"Errore nel resettare il timer gelato: {e}")
