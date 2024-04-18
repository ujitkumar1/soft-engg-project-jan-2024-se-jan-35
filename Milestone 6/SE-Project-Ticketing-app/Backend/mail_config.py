import os
import smtplib
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "teamFMM@developer.com"
SENDER_PASSWORD = ""


def send_email(to: str, subject: str, msg: str, attachment=None):
    '''Funtion to send Email
        * `to`: The reciever's email address
        * `subject`: The mail's subject
        * `msg`: The body of the mail
        * `attachment` (optional): Send files with the mail as attachment
    '''
    mail = MIMEMultipart()
    mail["From"] = SENDER_ADDRESS
    mail["Subject"] = subject
    mail["To"] = to

    mail.attach(MIMEText(msg, "html"))

    if attachment is not None:
        # adding attachment file to mail body
        with open(attachment, "rb") as attachment_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())
            encode_base64(part)

        part.add_header("Content-Disposition",
                        f"attachment; filename={attachment}")
        mail.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()

    # Remove the files from server space
    if attachment is not None:
        os.remove(attachment)

    return 'Email Sent Successfully'
