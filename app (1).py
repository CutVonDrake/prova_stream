import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

count = st_autorefresh(interval=1000, limit=None, key="timer")

def get_last_reset(key):
    if key not in st.session_state:
        st.session_state[key] = datetime.now()
    return st.session_state[key]

def reset_timer(key):
    st.session_state[key] = datetime.now()

st.title("⏱️ Timer senza...")

last_reset_pizza = get_last_reset("pizza")
elapsed_pizza = datetime.now() - last_reset_pizza
days_p = elapsed_pizza.days
hours_p = elapsed_pizza.seconds // 3600
minutes_p = (elapsed_pizza.seconds % 3600) // 60
seconds_p = elapsed_pizza.seconds % 60

st.subheader("😠👊 Tempo senza litigare:")
st.markdown(f"<h3>Giorni: {days_p:02}</h3>", unsafe_allow_html=True)
st.markdown(f"<h2>{hours_p:02}:{minutes_p:02}:{seconds_p:02}</h2>", unsafe_allow_html=True)
if st.button("Resetta litigi"):
    reset_timer("pizza")
    st.experimental_rerun()

last_reset_gelato = get_last_reset("gelato")
elapsed_gelato = datetime.now() - last_reset_gelato
days_g = elapsed_gelato.days
hours_g = elapsed_gelato.seconds // 3600
minutes_g = (elapsed_gelato.seconds % 3600) // 60
seconds_g = elapsed_gelato.seconds % 60

st.subheader("🥰😘 Tempo senza fare l'amore:")
st.markdown(f"<h3>Giorni: {days_g:02}</h3>", unsafe_allow_html=True)
st.markdown(f"<h2>{hours_g:02}:{minutes_g:02}:{seconds_g:02}</h2>", unsafe_allow_html=True)
if st.button("Resetta sesso"):
    reset_timer("gelato")
    st.experimental_rerun()
