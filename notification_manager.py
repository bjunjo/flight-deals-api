import os
from twilio.rest import Client

# Twilio
account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
my_twilio_num = os.environ.get("my_twilio_num")
my_num = os.environ.get("my_num")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def send_notifications(self, city, tequila_api_lowest_price, lowestPrice):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"For trip to {city}\n=> Tequila API Price: ￡{tequila_api_lowest_price}\nvs My Low Price: ￡{lowestPrice}\n",
            from_=my_twilio_num,
            to=my_num
        )
        print(message.status)