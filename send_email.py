"""
Google app password: zqmz hxoh vmdo mcke

"""
from email.message import EmailMessage
import smtplib
import ssl

SENDER = "vdefontscrape@gmail.com"
RECEIVER = "vdefontscrape@gmail.com"
PASSWORD = "zqmz hxoh vmdo mcke"

def send_email(msg: str) -> None:
    em = EmailMessage()
    em['From'] = SENDER
    em['To'] = RECEIVER
    em['Subject'] = "Daily Scrape Results"
    em.set_content(msg)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.sendmail(SENDER, RECEIVER, em.as_string())
