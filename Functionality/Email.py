import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def email_excel_document(file_path, recipients):
    recipients, subject, body = recipients.split(", "), "SFX List", "Here is the SFX list"
    session = make_session()
    for recipient in recipients:
        msg = make_message(recipient, subject, body)
        attach_invoice_to_msg(file_path, msg)
        session.send_message(msg)
        del msg


def make_session():
    s = smtplib.SMTP(host="smtp.gmail.com", port=587)
    s.starttls()
    s.login("brinkman.utilities@gmail.com", 'BU119ssd!')
    return s


def make_message(recipient, subject, body):
    m = MIMEMultipart()
    m['From'] = "brinkman.utilities@gmail.com"
    m["To"] = recipient
    m["Subject"] = subject
    m.attach(MIMEText(body, 'plain'))
    return m


def attach_invoice_to_msg(file_path, msg):
    with open(file_path, 'rb') as f:
        part = MIMEBase('application', 'vnd.ms-excel')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    file_name = os.path.basename(file_path)
    part.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(part)

