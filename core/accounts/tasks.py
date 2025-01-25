from celery import shared_task
from time import sleep

@shared_task
def sendEmail():
    # Simulate sending an email
    print("Sending email...")
    sleep(3)
    print("Email sent successfully!")
    