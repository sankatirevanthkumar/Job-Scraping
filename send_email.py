#!/usr/bin/env python3
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

smtp_port = 587
smtp_server = "smtp.gmail.com"

# Load sensitive credentials from environment variables
email_from = os.environ.get("EMAIL_FROM", "your_email@gmail.com")
password = os.environ.get("EMAIL_PASSWORD", "your_app_specific_password")
email_to = os.environ.get("EMAIL_TO", "recipient_email@gmail.com")
subj = "TODAY'S INTERNSHIP'S LIST"

body = """
Hello,

Attached is the CSV file containing company names, job titles, and links.
You can review the details and apply for internships accordingly.

Best regards,
Dharma Tej
"""

# Create the MIME message
msg = MIMEMultipart()
msg["From"] = email_from
msg["To"] = email_to
msg["Subject"] = subj

# Attach the plain text body
msg.attach(MIMEText(body, "plain"))

# Define the file to attach
filename = "filtered1_internships.csv"

try:
    with open(filename, "rb") as attachment:
        attachment_package = MIMEBase("application", "octet-stream")
        attachment_package.set_payload(attachment.read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(attachment_package)
except FileNotFoundError:
    print(f"Error: The file {filename} was not found.")
    exit(1)

# Connect to the SMTP server and send the email
try:
    print("Connecting to the SMTP server...")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_from, password)
    print("Connected successfully.")

    print(f"Sending email to {email_to}...")
    server.sendmail(email_from, email_to, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print("An error occurred:", e)
finally:
    server.quit()
