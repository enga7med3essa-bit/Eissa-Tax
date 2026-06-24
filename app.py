import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Eissa Tax", page_icon="💰", layout="centered")

# ---------------- UI ----------------
st.markdown("""
    <style>
    .main {background-color: #f7f9fc;}
    h1 {color: #1f4e79; text-align: center;}
    </style>
""", unsafe_allow_html=True)

st.title("💰 Eissa Tax Calculator")
st.write("حساب ضريبة كسب العمل بطريقة بسيطة واحترافية")

# ---------------- INPUT ----------------
salary = st.number_input("💵 الراتب الشهري", min_value=0.0, step=500.0)
insurance = st.number_input("🛡️ التأمينات الشهرية", min_value=0.0, step=100.0)

annual_salary = salary * 12
net_income = annual_salary - (insurance * 12)

# ---------------- TAX LOGIC ----------------
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

col1, col2, col3 = st.columns(3)
col1.metric("صافي سنوي", f"{net_income:,.0f} EGP")
col2.metric("الضريبة السنوية", f"{tax:,.0f} EGP")
col3.metric("ضريبة شهرية", f"{monthly_tax:,.0f} EGP")

st.success(f"💰 صافي المرتب الشهري بعد الضريبة: {net_monthly:,.2f} EGP")

# ---------------- EXPORT EXCEL ----------------
df = pd.DataFrame({
    "البيان": ["صافي سنوي", "الضريبة السنوية", "ضريبة شهرية", "صافي شهري"],
    "القيمة": [net_income, tax, monthly_tax, net_monthly]
})

excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False, engine="openpyxl")

st.download_button(
    "📥 تحميل Excel",
    data=excel_buffer.getvalue(),
    file_name="tax_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ---------------- EXPORT PDF ----------------
def create_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Eissa Tax Report", styles['Title']))
    content.append(Spacer(1, 12))

    for k, v in data.items():
        content.append(Paragraph(f"{k}: {v}", styles['Normal']))
        content.append(Spacer(1, 8))

    doc.build(content)
    buffer.seek(0)
    return buffer

pdf_data = {
    "صافي سنوي": f"{net_income:,.0f}",
    "ضريبة سنوية": f"{tax:,.0f}",
    "ضريبة شهرية": f"{monthly_tax:,.0f}",
    "صافي شهري": f"{net_monthly:,.2f}"
}

pdf_buffer = create_pdf(pdf_data)

st.download_button(
    "📄 تحميل PDF",
    data=pdf_buffer,
    file_name="tax_report.pdf",
    mime="application/pdf"
)
