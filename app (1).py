import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(st.secrets["GSPREAD_CREDS"], scopes=scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("1wGmd1x0DlCvBppFdnlckXiqPZ1Jagtxrq5aM9-puoMw").sheet1
val = sheet.acell('A1').value

st.write("Valore in A1:", val)
