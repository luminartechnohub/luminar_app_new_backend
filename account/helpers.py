from django.conf import settings
from twilio.rest import Client

class MessageHandler:
    phone_number= None
    otp = None
    def __init__(self,phone_number,otp) -> None:
        self.phone_number=phone_number
        self.otp = otp
    def send_otp_on_phone(self):
        client = Client(settings.SID,settings.TWILIO_TOKEN) 
        message = client.messages.create(
            body=f'Your otp is {self.otp}',
            from_= settings.ACTIVE_NUMBER,
            to=f'+91{self.phone_number}'

        )
        print(message.sid)