import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.title("AI-Powered Outreach and Follow-up")

st.sidebar.write("### Email Integration")
email_enabled = st.sidebar.checkbox("Enable Email Integration")
if email_enabled:
    smtp_server = st.sidebar.text_input("SMTP Server", "smtp.gmail.com")
    smtp_port = st.sidebar.number_input("SMTP Port", 587)
    sender_email = st.sidebar.text_input("Sender Email")
    sender_password = st.sidebar.text_input("Sender Password", type="password")
    recipient_email = st.sidebar.text_input("Recipient Email")

def generate_outreach_message(target_audience, product_service, tone):
    prompt = f"""
    You are a professional outreach specialist. Write a personalized outreach message for the following details:
    - Target Audience: {target_audience}
    - Product/Service: {product_service}
    - Tone: {tone}

    The message should be concise, engaging, and tailored to the target audience.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def generate_follow_up_email(initial_message, days_since_contact):
    prompt = f"""
    You are a professional outreach specialist. Write a follow-up email based on the following details:
    - Initial Message: {initial_message}
    - Days Since Last Contact: {days_since_contact}

    The follow-up email should be polite, non-intrusive, and encourage a response.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def send_email(subject, body, recipient_email, sender_email, sender_password, smtp_server, smtp_port):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

st.write("### Generate Outreach Message")
target_audience = st.text_input("Target Audience (e.g., small business owners, tech startups)")
product_service = st.text_input("Product/Service (e.g., AI-powered marketing tools)")
tone = st.selectbox("Tone", ["Professional", "Friendly", "Casual", "Persuasive"])

if st.button("Generate Outreach Message"):
    if target_audience and product_service:
        outreach_message = generate_outreach_message(target_audience, product_service, tone)
        st.write("### Outreach Message")
        st.write(outreach_message)

        st.download_button(
            label="Download Outreach Message",
            data=outreach_message,
            file_name="outreach_message.txt",
            mime="text/plain"
        )

        if email_enabled and recipient_email:
            send_email(
                subject="Outreach Message",
                body=outreach_message,
                recipient_email=recipient_email,
                sender_email=sender_email,
                sender_password=sender_password,
                smtp_server=smtp_server,
                smtp_port=smtp_port
            )
            st.success("Outreach message sent via email!")
    else:
        st.error("Please fill in all fields to generate the outreach message.")

st.write("### Generate Follow-up Email")
initial_message = st.text_area("Initial Outreach Message")
days_since_contact = st.number_input("Days Since Last Contact", min_value=1, value=7)

if st.button("Generate Follow-up Email"):
    if initial_message:
        follow_up_email = generate_follow_up_email(initial_message, days_since_contact)
        st.write("### Follow-up Email")
        st.write(follow_up_email)

        st.download_button(
            label="Download Follow-up Email",
            data=follow_up_email,
            file_name="follow_up_email.txt",
            mime="text/plain"
        )

        if email_enabled and recipient_email:
            send_email(
                subject="Follow-up Email",
                body=follow_up_email,
                recipient_email=recipient_email,
                sender_email=sender_email,
                sender_password=sender_password,
                smtp_server=smtp_server,
                smtp_port=smtp_port
            )
            st.success("Follow-up email sent via email!")
    else:
        st.error("Please provide the initial outreach message to generate the follow-up email.")