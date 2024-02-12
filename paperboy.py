import os
import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = os.environ.get("PAPERBOY_SENDER_EMAIL", "not_found@gmail.com")
SENDER_APP_PASSWORD = os.environ.get("PAPERBOY_SENDER_APP_PASSWORD", "not_found")

def main():
    # greetings
    print_about_app()

    # making paper
    paper = make_paper()

    # send paper at specific schedule
    deliver_paper(paper)

def make_paper():
    # setting subject, body, sender, recipients
    subject = "테스트 이메일입니다."
    body = "파이썬으로 이메일 발송 테스트입니다."
    sender = SENDER_EMAIL
    recipients = ["devjian1123@gmail.com"]

    # build paper and return
    paper = MIMEText(body)
    paper["Subject"] = subject
    paper["From"] = sender
    paper["To"] = ", ".join(recipients)

    return paper

def deliver_paper(paper):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        smtp_server.sendmail(SENDER_EMAIL, paper["To"].split(", "), paper.as_string())
    
    print("Email Sent !")

def print_about_app():
    print()
    print("=============================")
    print("PaperBoy v0.1")
    print("=============================")
    print(f"Sender Email: [{SENDER_EMAIL}]")
    print(f"App Password: [{SENDER_APP_PASSWORD}]")
    print()

main()
