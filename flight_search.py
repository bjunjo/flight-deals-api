import os
import requests

TEQUILA_ENDPOINT = os.environ.get("TEQUILA_ENDPOINT")
TEQUILA_APIKEY = os.environ.get("TEQUILA_APIKEY")

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_iata_codes(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        header = {
            "apikey": TEQUILA_APIKEY
        }
        query = {
            "term": city_name,
            "location_types": "airport"
        }
        teq_location_response = requests.get(url=location_endpoint, params=query, headers=header)
        location_data = teq_location_response.json()['locations']
        code = location_data[0]['code']
        return code

    def search_flight_prices(self, code, date_from, date_to):
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        header = {"apikey": TEQUILA_APIKEY}
        query = {
            "fly_from": "LON",
            "fly_to": code,
            "max_stopovers": 0,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "curr": "GBP"
        }
        searching_for_flights = requests.get(url=search_endpoint, params=query, headers=header)
        flight_data = searching_for_flights.json()['data']
        # print(f"{flight_data[0]['cityTo']}: £{flight_data[0]['price']}")
        return flight_data[0]['price']

