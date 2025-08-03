import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import gspread
from google.oauth2.service_account import Credentials

# Aggiorna ogni secondo
st_autorefresh(interval=1000, limit=None, key="auto_refresh")

# Setup credenziali Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(
    st.secrets["GSPREAD_CREDS"],
    scopes=scope
)
client = gspread.authorize(creds)
sheet = client.open_by_key("1wGmd1x0DlCvBppFdnlckXiqPZ1Jagtxrq5aM9-puoMw").sheet1

# Funzione per ottenere timestamp da una cella
def get_timestamp(cell):
    ts = sheet.acell(cell).value
    return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

# Funzione per aggiornare timestamp
def set_timestamp(cell):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.update(cell, now_str)
    st.rerun()

# Recupero timestamp
last_reset_pizza = get_timestamp("A1")
last_reset_gelato = get_timestamp("A2")

# Calcolo tempo trascorso
def elapsed_time(since):
    delta = datetime.now() - since
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    return days, hours, minutes, seconds

days_p, hours_p, minutes_p, seconds_p = elapsed_time(last_reset_pizza)
days_g, hours_g, minutes_g, seconds_g = elapsed_time(last_reset_gelato)

# UI
st.title("⏱️ Timer senza...")

st.subheader("😠👊 Tempo senza litigare:")
st.markdown(f"<h3>Giorni: {days_p:02}</h3>", unsafe_allow_html=True)
st.markdown(f"<h2>{hours_p:02}:{minutes_p:02}:{seconds_p:02}</h2>", unsafe_allow_html=True)
if st.button("Resetta litigi"):
    set_timestamp("A1")

st.subheader("🥰😘 Tempo senza fare l'amore:")
st.markdown(f"<h3>Giorni: {days_g:02}</h3>", unsafe_allow_html=True)
st.markdown(f"<h2>{hours_g:02}:{minutes_g:02}:{seconds_g:02}</h2>", unsafe_allow_html=True)
if st.button("Resetta sesso"):
    set_timestamp("A2")
