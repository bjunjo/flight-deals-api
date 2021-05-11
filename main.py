# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
import requests
import datetime
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


# TODO: 1.Read and write data to your Google Sheet
# TODO: 2. Use the Sheety API to GET all the data in that sheet and print it out.
# TODO: 3. Try importing pretty print with the line from pprint import pprint and printing the data out again using pprint() to see it formatted.
# TODO: 4. Pass everything stored in the "prices" key back to the main.py file and store it in a variable called sheet_data,
#  so that you can print the sheet_data from main.py
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
sheety_response = requests.get(url=SHEETY_ENDPOINT)
sheet_data = sheety_response.json()['prices']

date_from = datetime.date.today() + datetime.timedelta(days=1)
date_to = datetime.date.today() + datetime.timedelta(days=180)

# TODO: 5. In main.py check if sheet_data contains any values for the "iataCode" key.
#  If not, then the IATA Codes column is empty in the Google Sheet.
#  In this case, pass each city name in sheet_data one-by-one to the FlightSearch class.
#  For now, the FlightSearch class can respond with "TESTING" instead of a real IATA code.
#  You should use the response from the FlightSearch class to update the sheet_data dictionary
flight_search = FlightSearch()
data_manager = DataManager()
for row in sheet_data:
    if row['iataCode'] == "":
        # TODO 7. Pass each city name in sheet_data one-by-one to the FlightSearch class
        #  to get the corresponding IATA code for that city using the Flight Search API.
        #  You should use the code you get back to update the sheet_data dictionary.
        row['iataCode'] = flight_search.get_iata_codes(row['city'])

        # TODO: 6. In the DataManager Class make a PUT request and use the row id
        #  from sheet_data to update the Google Sheet with the IATA codes. (Do this using code).
        #  HINT: Remember to check the checkbox to allow PUT requests in Sheety.
        data_manager.update_destination_codes(row['iataCode'], row['id'])

    # TODO 8. The next step is to search for the flight prices from London (LON)
    #  to all the destinations in the Google Sheet. In this project,
    #  we're looking only for direct flights, that leave anytime between tomorrow and in 6 months (6x30days) time.
    #  We're also looking for round trips that return between 7 and 28 days in length.
    #  The currency of the price we get back should be in GBP.
    tequila_api_lowest_price = flight_search.search_flight_prices(row['iataCode'], date_from, date_to)

    # TODO 9. The final step is to check if any of the flights found are
    #  cheaper than the Lowest Price listed in the Google Sheet.
    #  If so, then we should use the Twilio API to send an SMS with enough information to book the flight.
    #  You should use the NotificationManager for this job.
    if row['lowestPrice'] > tequila_api_lowest_price:
        notification_manager = NotificationManager()
        notification_manager.send_notifications(row['city'], tequila_api_lowest_price, row['lowestPrice'])

