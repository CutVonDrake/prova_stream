import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
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
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

# Caricamento timer litigi da A1
if "start_time_litigi" not in st.session_state:
    try:
        st.session_state.start_time_litigi = load_time_from_sheet("A1")
    except Exception as e:
        st.error(f"Errore nel caricamento del timer litigi: {e}")
        st.stop()

# Caricamento timer gelato da B1
if "start_time_gelato" not in st.session_state:
    try:
        st.session_state.start_time_gelato = load_time_from_sheet("B1")
    except Exception as e:
        st.error(f"Errore nel caricamento del timer gelato: {e}")
        st.stop()

def format_delta(delta):
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    return days, hours, minutes, seconds

now = datetime.now()

# Calcola delta litigi
delta_litigi = now - st.session_state.start_time_litigi
days_l, hours_l, minutes_l, seconds_l = format_delta(delta_litigi)

st.markdown(f"<h1 style='font-size: 48px;'>⏳ Giorni senza litigare: {days_l}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='font-size: 36px;'>{hours_l:02}:{minutes_l:02}:{seconds_l:02}</h2>", unsafe_allow_html=True)

# Calcola delta gelato
delta_gelato = now - st.session_state.start_time_gelato
days_g, hours_g, minutes_g, seconds_g = format_delta(delta_gelato)

st.markdown(f"<h1 style='font-size: 48px;'>🍦 Giorni senza gelato: {days_g}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='font-size: 36px;'>{hours_g:02}:{minutes_g:02}:{seconds_g:02}</h2>", unsafe_allow_html=True)

def reset_timer(cell, session_key):
    try:
        now_reset = datetime.now()
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(
            st.secrets["GSPREAD_CREDS"],
            scopes=scope
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1wGmd1x0DlCvBppFdnlckXiqPZ1Jagtxrq5aM9-puoMw").sheet1
        now_str = now_reset.strftime("%Y-%m-%d %H:%M:%S")
        sheet.update(cell, [[now_str]])
        st.session_state[session_key] = now_reset
    except Exception as e:
        st.error(f"Errore nel resettare il timer: {e}")

if st.button("🔄 Resetta timer litigi"):
    reset_timer("A1", "start_time_litigi")

if st.button("🔄 Resetta timer gelato"):
    reset_timer("B1", "start_time_gelato")
