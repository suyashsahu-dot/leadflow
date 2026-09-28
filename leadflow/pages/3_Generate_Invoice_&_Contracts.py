import streamlit as st
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import pandas as pd

st.title("Generate Invoice & Contracts")

if "items" not in st.session_state:
    st.session_state.items = []

option = st.sidebar.radio("Choose an option", ["Generate Invoice", "Generate Contract"])

st.sidebar.write("### Custom Templates")
uploaded_invoice_template = st.sidebar.file_uploader("Upload Invoice Template (HTML)", type=["html"])
uploaded_contract_template = st.sidebar.file_uploader("Upload Contract Template (HTML)", type=["html"])

st.sidebar.write("### Email Integration")
email_enabled = st.sidebar.checkbox("Enable Email Integration")
if email_enabled:
    smtp_server = st.sidebar.text_input("SMTP Server", "smtp.gmail.com")
    smtp_port = st.sidebar.number_input("SMTP Port", 587)
    sender_email = st.sidebar.text_input("Sender Email")
    sender_password = st.sidebar.text_input("Sender Password", type="password")
    recipient_email = st.sidebar.text_input("Recipient Email")

def send_email(file_path, recipient_email, sender_email, sender_password, smtp_server, smtp_port):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "Generated Document"

    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(file_path)}",
        )
        msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if option == "Generate Invoice":
    st.subheader("Generate Invoice")

    st.write("### Your Details")
    your_name = st.text_input("Your Name/Company Name")
    your_address = st.text_input("Your Address")
    your_email = st.text_input("Your Email")
    your_phone = st.text_input("Your Phone Number")

    st.write("### Client Details")
    client_name = st.text_input("Client Name/Company Name")
    client_address = st.text_input("Client Address")
    client_email = st.text_input("Client Email")
    client_phone = st.text_input("Client Phone Number")

    st.write("### Invoice Details")
    invoice_number = st.text_input("Invoice Number")
    invoice_date = st.date_input("Invoice Date")
    due_date = st.date_input("Due Date")

    st.write("### Items")
    with st.form("item_form"):
        st.write("Add an item:")
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        rate = st.number_input("Rate (per unit)", min_value=0.0, value=0.0)
        submitted = st.form_submit_button("Add Item")

        if submitted:
            st.session_state.items.append({
                "Item Name": item_name,
                "Quantity": quantity,
                "Rate": rate,
                "Total": quantity * rate
            })
            st.success("Item added!")

    if st.session_state.items:
        st.write("### Items List")
        items_df = pd.DataFrame(st.session_state.items)
        st.dataframe(items_df)

        total_amount = items_df["Total"].sum()
        st.write(f"**Total Amount:** ${total_amount:.2f}")

        if st.button("Generate Invoice PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt=f"Invoice From: {your_name}", ln=True)
            pdf.cell(200, 10, txt=f"Address: {your_address}", ln=True)
            pdf.cell(200, 10, txt=f"Email: {your_email}", ln=True)
            pdf.cell(200, 10, txt=f"Phone: {your_phone}", ln=True)
            pdf.ln(10)

            pdf.cell(200, 10, txt=f"Invoice To: {client_name}", ln=True)
            pdf.cell(200, 10, txt=f"Address: {client_address}", ln=True)
            pdf.cell(200, 10, txt=f"Email: {client_email}", ln=True)
            pdf.cell(200, 10, txt=f"Phone: {client_phone}", ln=True)
            pdf.ln(10)

            pdf.cell(200, 10, txt=f"Invoice Number: {invoice_number}", ln=True)
            pdf.cell(200, 10, txt=f"Invoice Date: {invoice_date}", ln=True)
            pdf.cell(200, 10, txt=f"Due Date: {due_date}", ln=True)
            pdf.ln(10)

            pdf.cell(200, 10, txt="Items:", ln=True)
            pdf.cell(50, 10, txt="Item Name", border=1)
            pdf.cell(30, 10, txt="Quantity", border=1)
            pdf.cell(30, 10, txt="Rate", border=1)
            pdf.cell(30, 10, txt="Total", border=1, ln=True)
            for item in st.session_state.items:
                pdf.cell(50, 10, txt=item["Item Name"], border=1)
                pdf.cell(30, 10, txt=str(item["Quantity"]), border=1)
                pdf.cell(30, 10, txt=f"${item['Rate']:.2f}", border=1)
                pdf.cell(30, 10, txt=f"${item['Total']:.2f}", border=1, ln=True)

            pdf.cell(200, 10, txt=f"Total Amount: ${total_amount:.2f}", ln=True)

            pdf_output = pdf.output(dest="S").encode("latin1")
            with open("invoice.pdf", "wb") as f:
                f.write(pdf_output)

            with open("invoice.pdf", "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="Download Invoice as PDF",
                data=pdf_bytes,
                file_name="invoice.pdf",
                mime="application/pdf"
            )

            if email_enabled and recipient_email:
                send_email("invoice.pdf", recipient_email, sender_email, sender_password, smtp_server, smtp_port)
                st.success("Invoice sent via email!")

elif option == "Generate Contract":
    st.subheader("Generate Contract")

    st.write("### Your Details")
    your_name = st.text_input("Your Name/Company Name")
    your_address = st.text_input("Your Address")
    your_email = st.text_input("Your Email")
    your_phone = st.text_input("Your Phone Number")

    st.write("### Client Details")
    client_name = st.text_input("Client Name/Company Name")
    client_address = st.text_input("Client Address")
    client_email = st.text_input("Client Email")
    client_phone = st.text_input("Client Phone Number")

    st.write("### Contract Terms")
    project_scope = st.text_area("Project Scope")
    payment_terms = st.text_area("Payment Terms")
    contract_date = st.date_input("Contract Date")

    if st.button("Generate Contract PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Contract From: {your_name}", ln=True)
        pdf.cell(200, 10, txt=f"Address: {your_address}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {your_email}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {your_phone}", ln=True)
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Contract To: {client_name}", ln=True)
        pdf.cell(200, 10, txt=f"Address: {client_address}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {client_email}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {client_phone}", ln=True)
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Contract Date: {contract_date}", ln=True)
        pdf.multi_cell(200, 10, txt=f"Project Scope: {project_scope}")
        pdf.multi_cell(200, 10, txt=f"Payment Terms: {payment_terms}")

        pdf_output = pdf.output(dest="S").encode("latin1")
        with open("contract.pdf", "wb") as f:
            f.write(pdf_output)

        with open("contract.pdf", "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="Download Contract as PDF",
            data=pdf_bytes,
            file_name="contract.pdf",
            mime="application/pdf"
        )

        if email_enabled and recipient_email:
            send_email("contract.pdf", recipient_email, sender_email, sender_password, smtp_server, smtp_port)
            st.success("Contract sent via email!")