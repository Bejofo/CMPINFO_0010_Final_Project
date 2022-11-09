import json, csv
import googlemaps

# Connect to Google Maps API
API_KEY = input("Enter the API key: ")
gmaps = googlemaps.Client(key = API_KEY, timeout=5)

# Import business list
business_list = open("data/search_nearby.csv", "r", encoding="utf-8-sig", newline='')
business_data = csv.reader(business_list)
next(business_data)

# json
json_dump = open("data/place_details_unprocessed.json", "w", encoding="utf-8-sig")
json_export = []

# csv
data_output = open("data/place_details.csv", "w", encoding="utf-8-sig", newline='')
csv_writer = csv.writer(data_output)
csv_writer.writerow(["place_id", "name", "plus_code", "street_number", "route", "neighborhood", "township", "postal_code", "latitude", "longitude", "curbside_pickup", "price_level", "rating", "user_ratings_total", "mon_open", "mon_close", "tue_open", "tue_close", "wed_open", "wed_close", "thu_open", "thu_close", "fri_open", "fri_close", "sat_open", "sat_close", "sun_open", "sun_close"])

# Query businesses in list
for business in business_data:
    # Check API call status
    while (True):
        try:
            response = gmaps.place(place_id=business[0])
        except:
            input("Request failed. Press enter to retry.")
                    
        if (response["status"] == "OK"):
            break
        else:
            print("Request failed! Status: " + response["status"])
            input("Press enter to retry.")
    
    # Process data
    data = response["result"]

    # json
    json_export.append(response)

    # csv
    name = data.get("name")
    place_id = data.get("place_id")
    plus_code = data.get("plus_code").get("global_code")

    address_components = data.get("address_components")
    neighborhood = None
    township = None

    for component in address_components:
        level = component["types"][0]

        if level == "street_number":
            street_number = component.get("long_name")
        elif level == "route":
            route = component.get("long_name")
        elif level == "neighborhood":
            neighborhood = component.get("long_name")
        elif level == "locality":
            pass
        elif level == "administrative_area_level_3": # Township
            township = component.get("long_name")
        elif level == "administrative_area_level_2": # County
            pass
        elif level == "administrative_area_level_1": # State
            pass
        elif level == "country":
            pass
        elif level == "postal_code":
            postal_code = component.get("long_name")


    location = data.get("geometry").get("location")
    latitude = location.get("lat")
    longitude = location.get("lng")

    curbside_pickup = data.get("curbside_pickup")
    price_level = data.get("price_level")
    rating = data.get("rating")
    user_ratings_total = data.get("user_ratings_total")

    details = [place_id, name, plus_code, street_number, route, neighborhood, township, postal_code, latitude, longitude, curbside_pickup, price_level, rating, user_ratings_total]

    # WIP
    opening_hours = data.get("opening_hours")

    for day in opening_hours["periods"]:
        open = day["open"]["time"]
        close = day["close"]["time"]

        details.append(open)
        details.append(close)

    csv_writer.writerow(details)

json.dump(json_export, json_dump)

business_list.close()
json_dump.close()
data_output.close()