# multi_agent_analytics/app.py

try:
    import streamlit as st
except ModuleNotFoundError:
    raise ImportError("streamlit is not installed. Please run: pip install streamlit")

import pandas as pd
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="E-commerce Analytics", layout="centered")

st.title("📊 Multi-Agent E-commerce Analytics")
st.markdown("Upload your e-commerce sales data to generate automated business insights.")

uploaded_file = st.file_uploader("📤 Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    # Simulated Agent 1: Sales Analysis
    total_sales = df["sales"].sum()
    avg_order_value = df["sales"].mean()

    # Simulated Agent 2: Top Category Detection
    top_category = df["category"].value_counts().idxmax()

    # Simulated Agent 3: Anomaly Detection (very simple)
    daily_sales = df.groupby("date")["sales"].sum()
    mean_sales = daily_sales.mean()
    anomaly_days = daily_sales[daily_sales < mean_sales * 0.5].index.tolist()

    st.subheader("🧠 Agent Insights")
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Average Order Value", f"${avg_order_value:,.2f}")
    st.markdown(f"**Top Selling Category:** {top_category}")

    if anomaly_days:
        st.warning(f"🚨 Anomalies Detected on: {', '.join(anomaly_days)}")
    else:
        st.success("✅ No anomalies detected in daily sales.")

    # Simulated Agent 4: Report Generation
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="E-commerce Sales Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Sales: ${total_sales:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Average Order Value: ${avg_order_value:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Top Category: {top_category}", ln=True)
    if anomaly_days:
        pdf.cell(200, 10, txt=f"Anomalies Detected on: {', '.join(anomaly_days)}", ln=True)
    else:
        pdf.cell(200, 10, txt="No anomalies detected.", ln=True)

    # Save to temp file and provide download button
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        tmp_file_path = tmp_file.name

    with open(tmp_file_path, "rb") as f:
        st.download_button("📄 Download PDF Report", f, file_name="report.pdf")

else:
    st.info("📂 Please upload a CSV file with 'date', 'category', and 'sales' columns.")
