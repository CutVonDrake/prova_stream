import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Definisci lo scope corretto per i fogli Google
scope = ["https://www.googleapis.com/auth/spreadsheets"]

# Prendi le credenziali dal secret di Streamlit e crea l'oggetto Credentials
creds = Credentials.from_service_account_info(
    st.secrets["GSPREAD_CREDS"],
    scopes=scope
)

# Autorizza il client gspread
client = gspread.authorize(creds)

# Apri il foglio "timer_reset"
sheet = client.open_by_key("1wGmd1x0DlCvBppFdnlckXiqPZ1Jagtxrq5aM9-puoMw").sheet1

# Leggi la data/ora dalla cella A1
start_time_str = sheet.acell("A1").value
start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")

# Calcola il tempo trascorso
now = datetime.now()
delta = now - start_time

# Funzione per formattare timedelta
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return days, hours, minutes, seconds

days, hours, minutes, seconds = format_timedelta(delta)

# Mostra il timer in Streamlit
st.markdown(f"<h1 style='font-size: 48px;'>Giorni senza pizza: {days}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='font-size: 36px;'>{hours:02}:{minutes:02}:{seconds:02}</h2>", unsafe_allow_html=True)

# Pulsante reset
if st.button("Reset timer"):
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    sheet.update("A1", now_str)
    st.experimental_rerun()
