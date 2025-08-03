import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

# Autenticazione
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(
    st.secrets["GSPREAD_CREDS"],
    scopes=scope
)

# Connessione a Google Sheets
client = gspread.authorize(creds)
sheet = client.open("timer_reset").sheet1

files = client.list_spreadsheet_files()
for f in files:
    st.write(f['name'])

# Leggi la data di inizio dalla cella A1
start_time_str = sheet.acell("A1").value
start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")

# Calcola il tempo trascorso
now = datetime.now()
delta = now - start_time

# Format del tempo trascorso
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return days, hours, minutes, seconds

days, hours, minutes, seconds = format_timedelta(delta)

# UI
st.markdown(f"<h1 style='font-size: 48px;'>🍕 Giorni senza pizza: {days}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='font-size: 36px;'>{hours:02}:{minutes:02}:{seconds:02}</h2>", unsafe_allow_html=True)

# Pulsante per il reset
if st.button("🔁 Resetta timer"):
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    sheet.update("A1", now_str)
    st.rerun()
