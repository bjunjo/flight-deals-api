# flight-deals-api
## Problem: Get the best flight deals using Sheety, Tequila, and Twilio API
## Solutions
1. Read and write data to your Google Sheet. Use the Sheety API to GET all the data in that sheet and print it out.
Try importing pretty print with the line from pprint import pprint and printing the data out again using `pprint()` to see it formatted.
Pass everything stored in the "prices" key back to the main.py file and store it in a variable called sheet_data,
```
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
sheety_response = requests.get(url=SHEETY_ENDPOINT)
sheet_data = sheety_response.json()['prices']
```
2. In main.py check if sheet_data contains any values for the "iataCode" key.
If not, then the IATA Codes column is empty in the Google Sheet.
In this case, pass each city name in sheet_data one-by-one to the FlightSearch class.
For now, the FlightSearch class can respond with "TESTING" instead of a real IATA code.
You should use the response from the FlightSearch class to update the sheet_data dictionary
```
# In main.py
flight_search = FlightSearch()
data_manager = DataManager()
```
```
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
```
3. In the DataManager Class make a PUT request and use the row id from sheet_data to update the Google Sheet with the IATA codes. (Do this using code).
HINT: Remember to check the checkbox to allow PUT requests in Sheety.
Pass each city name in sheet_data one-by-one to the FlightSearch class to get the corresponding IATA code for that city using the Flight Search API.
You should use the code you get back to update the sheet_data dictionary.
```
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
```
4. The next step is to search for the flight prices from London (LON) to all the destinations in the Google Sheet. In this project, we're looking only for direct flights, that leave anytime between tomorrow and in 6 months (6x30days) time.
We're also looking for round trips that return between 7 and 28 days in length. The currency of the price we get back should be in GBP.
```
tequila_api_lowest_price = flight_search.search_flight_prices(row['iataCode'], date_from, date_to)
```
5. The final step is to check if any of the flights found are cheaper than the Lowest Price listed in the Google Sheet.
If so, then we should use the Twilio API to send an SMS with enough information to book the flight.
You should use the NotificationManager for this job.
```
if row['lowestPrice'] > tequila_api_lowest_price:
    notification_manager = NotificationManager()
    notification_manager.send_notifications(row['city'], tequila_api_lowest_price, row['lowestPrice'])
```
## Lessons
1. Slow down.
2. Don't copy others code. Solve each problem from the first principles.
3. Took me 2 good days to sort these out--feeling great!
