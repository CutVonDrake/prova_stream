import streamlit as st
import datetime
import time
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Autenticazione con Google Sheets
creds = json.loads(st.secrets["GSPREAD_CREDS"])
gc = gspread.service_account_from_dict(creds)
sh = gc.open("timer_reset")
worksheet = sh.sheet1

# Funzione per ottenere la data di partenza dal foglio
@st.cache_data(ttl=10)
def get_start_time():
    value = worksheet.acell("A1").value
    return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

# Funzione per impostare la data di partenza nel foglio
def set_start_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.update("A1", now)

# Funzione per formattare il tempo trascorso
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return days, hours, minutes, seconds

# Layout Streamlit
st.title("⏱️ Timer condiviso")

# Mostra il tempo trascorso
start_time = get_start_time()
now = datetime.datetime.now()
delta = now - start_time
days, hours, minutes, seconds = format_timedelta(delta)

st.markdown(f"### Giorni: `{days}`")
st.markdown(f"## {hours:02}:{minutes:02}:{seconds:02}")

# Bottone per resettare
if st.button("Resetta timer", key="reset"):
    set_start_time()
    st.experimental_rerun()
