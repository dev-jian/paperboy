import os
import smtplib
import requests
import schedule
import time
from jinja2 import Template
from email.mime.text import MIMEText
from datetime import datetime

SENDER_EMAIL = os.environ.get("PAPERBOY_SENDER_EMAIL", "not_found")
SENDER_APP_PASSWORD = os.environ.get("PAPERBOY_SENDER_APP_PASSWORD", "not_found")
SEND_TIME = "08:00"

def main():
    # greetings
    initialize()

    # set schedule
    schedule.every().day.at(SEND_TIME).do(deliver_paper_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def deliver_paper_job():
    # making paper
    paper = make_paper()

    # send paper at specific schedule
    deliver_paper(paper)

def initialize():
    # Welcome UI
    print()
    print("=============================")
    print("PaperBoy v0.2")
    print("=============================")
    print(f"Sender Email: [{SENDER_EMAIL}]")
    print(f"App Password: [{SENDER_APP_PASSWORD}]")
    print(f"Send it every day at {SEND_TIME}")
    print()

    # Guide when Env doesn't set.
    if (SENDER_EMAIL == "not_found" or SENDER_APP_PASSWORD == "not_found"):
        print("Please set ENV Variables to login SMTP. key=PAPERBOY_SENDER_EMAIL, PAPERBOY_SENDER_APP_PASSWORD")
        return

def make_paper():
    current_datetime = datetime.now()

    # setting subject, body, sender, recipients
    subject = current_datetime.strftime("%Y년 %m월 %d일 아침 뉴스입니다 !")
    body = render_html_with_template()
    sender = SENDER_EMAIL
    recipients = ["devjian1123@gmail.com", "handsomekey1123@gmail.com", "devjian1123@12cm.co.kr"]

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

def render_html_with_template():
    with open("paper.html", "r", encoding='UTF8') as paper_html:
        template = Template(paper_html.read())

    context = {
        "advice": get_advice()
    }

    return template.render(context)

def get_advice():
    url = "https://api.adviceslip.com/advice"

    print("Get advice from API ...")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Success to get advice!")
        print()
        return data["slip"]["advice"]
    else:
        print("Fail to get advice from API")

main()
