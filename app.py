import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Eissa Tax", page_icon="💰", layout="centered")

st.title("💰 Eissa Tax Calculator")

# ---------------- INPUT ----------------
salary = st.number_input("💵 الراتب الشهري", min_value=0.0, step=500.0)
insurance = st.number_input("🛡️ التأمينات الشهرية", min_value=0.0, step=100.0)

annual_salary = salary * 12
net_income = annual_salary - (insurance * 12)

# ---------------- SIMPLE TAX ----------------
def calculate_tax(income):
    if income <= 60000:
        return 0
    elif income <= 200000:
        return (income - 60000) * 0.10
    elif income <= 400000:
        return 14000 + (income - 200000) * 0.15
    else:
        return 44000 + (income - 400000) * 0.20

tax = calculate_tax(net_income)
monthly_tax = tax / 12
net_monthly = salary - monthly_tax - insurance

# ---------------- RESULT ----------------
st.subheader("📊 النتائج")

st.write("صافي سنوي:", net_income)
st.write("الضريبة السنوية:", tax)
st.write("ضريبة شهرية:", monthly_tax)
st.success(f"💰 صافي المرتب الشهري: {net_monthly:.2f} EGP")
