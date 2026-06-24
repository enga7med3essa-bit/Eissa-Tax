
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Eissa Tax", layout="wide")

def init_db():
    conn=sqlite3.connect("eissatax.db")
    cur=conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS salaries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT,
    gross REAL,
    basic REAL,
    special REAL,
    tax REAL,
    net REAL)''')
    conn.commit()
    conn.close()

def calc_tax(gross,basic,special):
    total=basic+special
    monthly=gross-total
    annual=monthly*12
    taxable=max(annual-20000,0)
    tax=(max(min(taxable,55000)-40000,0)*0.10 +
         max(min(taxable,70000)-55000,0)*0.15 +
         max(min(taxable,200000)-70000,0)*0.20 +
         max(min(taxable,400000)-200000,0)*0.225 +
         max(taxable-400000,0)*0.25)
    return tax/12, gross-total-tax/12

init_db()

st.title("Eissa Tax")

tab1,tab2=st.tabs(["الحاسبة","السجل"])

with tab1:
    gross=st.number_input("إجمالي الاستحقاقات",0.0)
    basic=st.number_input("التأمين الأساسي",0.0)
    special=st.number_input("التأمينات الخاصة",0.0)
    month=st.text_input("الشهر")

    if st.button("احسب الضريبة"):
        tax,net=calc_tax(gross,basic,special)
        st.success(f"ضريبة كسب العمل: {tax:.2f} جنيه")
        st.info(f"صافي المرتب: {net:.2f} جنيه")

        conn=sqlite3.connect("eissatax.db")
        conn.execute("INSERT INTO salaries(month,gross,basic,special,tax,net) VALUES(?,?,?,?,?,?)",
                     (month,gross,basic,special,tax,net))
        conn.commit()
        conn.close()

with tab2:
    conn=sqlite3.connect("eissatax.db")
    df=pd.read_sql_query("SELECT * FROM salaries ORDER BY id DESC",conn)
    conn.close()
    st.dataframe(df,use_container_width=True)
