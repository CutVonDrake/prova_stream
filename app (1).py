import streamlit as st
import gspread
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# refresh ogni secondo
st_autorefresh(interval=1000, key="auto-refresh")

# Autenticazione
gc = gspread.service_account(filename="service_account.json")
sh = gc.open("timer_reset")
worksheet = sh.sheet1

# Funzioni
def get_timestamp(voce):
    records = worksheet.get_all_records()
    for row in records:
        if row["voce"] == voce:
            return datetime.fromisoformat(row["timestamp"])
    return datetime.now()  # fallback se non trova nulla

def reset_timestamp(voce):
    cell = worksheet.find(voce)
    worksheet.update_cell(cell.row, 2, datetime.now().isoformat())

def format_timedelta(td):
    days = td.days
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    return days, hours, minutes, seconds

# App
st.title("⏱️ Timer senza pizza e gelato")

for voce, emoji in [("pizza", "🍕"), ("gelato", "🍦")]:
    st.subheader(f"{emoji} Tempo senza mangiare {voce}:")
    last_reset = get_timestamp(voce)
    elapsed = datetime.now() - last_reset
    d, h, m, s = format_timedelta(elapsed)
    st.markdown(f"<h3>Giorni: {d:02}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2>{h:02}:{m:02}:{s:02}</h2>", unsafe_allow_html=True)

    if st.button(f"Resetta {voce}", key=f"reset_{voce}"):
        reset_timestamp(voce)
        st.experimental_rerun()
