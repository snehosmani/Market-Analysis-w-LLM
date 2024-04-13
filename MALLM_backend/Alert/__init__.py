# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import smtplib
from dotenv import load_dotenv
import os
load_dotenv()

def send_email(body):
    app_psswd=os.environ['Google_app_password_mail']
    send_email_id='bappasnehal@gmail.com'
    recv_email_id='hosmanisnehal@gmail.com'

    subject="Market Analysis Report!!"

    mail=f"Subject: {subject}\n\n{body}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(send_email_id,app_psswd)
    server.sendmail(send_email_id,recv_email_id,mail)
    return True

def main(load):
    body=f"Analysis from Google Search over the past 1 year from {load['model']} model: \n\n"
    #body='Analysis from Google Search over the past 1 year: \n\n'
    for item in load['results']:
        if item['Analysis']!='none':
            url=item['url']
            content=item['Analysis']
            content = content.encode('ascii', 'ignore')
            content=content.decode('ascii')
            
            body+=f'\n\nThe article at {url} says: \n\n {content}\n\n'
        else:
            continue
    
    mail=send_email(body)
    return body

