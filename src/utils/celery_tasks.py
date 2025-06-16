
from celery import Celery
from src.utils.mail import create_message, mail
from asgiref.sync import async_to_sync
celery_app = Celery()

celery_app.config_from_object("src.config")

@celery_app.task()
def send_email(recipients: list[str], subject:str, body:str):
    message = create_message(recipients,subject,body)
    async_to_sync(mail.send_message)(message)
    print("message sent")