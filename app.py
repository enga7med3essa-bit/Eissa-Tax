import streamlit as st

st.title("💰 Eissa Tax Calculator")

salary = st.number_input("الراتب الشهري", min_value=0.0)
insurance = st.number_input("التأمينات الشهرية", min_value=0.0)

annual = salary * 12
net = annual - insurance * 12

st.write("صافي سنوي:", net)
