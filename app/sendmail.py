import settings
import logger
import smtplib
from email.message import EmailMessage


csmtp = settings.smtp
cport = settings.port
caccount = settings.account
cpassword = settings.password
sendAlert = settings.sendAlerts


def send_alert(subject, message, destination):
    server = smtplib.SMTP(csmtp, cport)
    server.starttls()
    server.login(caccount, cpassword)
    if sendAlert:
        try:
            msg = EmailMessage()
            message = f'{message}\n'
            msg.set_content(message)
            msg['Subject'] = subject
            msg['From'] = 'transfer@kristijan.me'
            msg['To'] = destination
            server.send_message(msg)
            logger.log("File transfer success, confirmation sent via e-mail!")
            print("File transfer success, confirmation sent via e-mail!")
        except:
            logger.log("Something went wrong. Confirmation is not sent!")
            print("Something went wrong. Confirmation is not sent!")
    else:
        logger.log('Sending e-mail alerts is currently disabled in config.yaml file, please set "send-alerts" to "true" if you want to send e-mails!')
        print('Sending e-mail alerts is currently disabled in config.yaml file, please set "send-alerts" to "true" if you want to send e-mails!')


def email_test():
    recipient = settings.testEmail
    subject_alert = "Email test"
    message_alert = "This is an automated email test. Email is successfully delivered. Congrats!"
    send_alert(subject_alert, message_alert, recipient)
