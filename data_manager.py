import os
import requests
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def update_destination_codes(self, code, id):
        body = {
            "price": {
                "iataCode": code
            }
        }
        return requests.put(url=f"{SHEETY_ENDPOINT}/{id}", json=body)