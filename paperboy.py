import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

SENDER_EMAIL = os.environ.get("PAPERBOY_SENDER_EMAIL", "not_found")
SENDER_APP_PASSWORD = os.environ.get("PAPERBOY_SENDER_APP_PASSWORD", "not_found")

def main():
    # greetings
    initialize()

    # making paper
    paper = make_paper()

    # send paper at specific schedule
    deliver_paper(paper)

def make_paper():
    current_datetime = datetime.now()

    # setting subject, body, sender, recipients
    subject = current_datetime.strftime("%Y년 %m월 %d일 아침 뉴스입니다 !")
    body = "기본 내용입니다."
    with open("paper.html", "r", encoding='UTF8') as paper_html:
        body = paper_html.read()
    sender = SENDER_EMAIL
    recipients = ["devjian1123@gmail.com", "handsomekey1123@gmail.com"]

    # build paper and return
    paper = MIMEText(body, "html")
    paper["Subject"] = subject
    paper["From"] = sender
    paper["To"] = ", ".join(recipients)

    return paper

def deliver_paper(paper):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        smtp_server.sendmail(SENDER_EMAIL, paper["To"].split(", "), paper.as_string())
    
    print("Email Sent !")

def initialize():
    print()
    print("=============================")
    print("PaperBoy v0.2")
    print("=============================")
    print(f"Sender Email: [{SENDER_EMAIL}]")
    print(f"App Password: [{SENDER_APP_PASSWORD}]")
    print()

    if (SENDER_EMAIL == "not_found" or SENDER_APP_PASSWORD == "not_found"):
        print("Please set ENV Variables to login SMTP. key=PAPERBOY_SENDER_EMAIL, PAPERBOY_SENDER_APP_PASSWORD")
        return
    
main()
