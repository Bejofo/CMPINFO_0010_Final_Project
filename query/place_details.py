import json, csv
import googlemaps

# Query API
def get_details(id):
    while (True):
        try:
            response = gmaps.place(place_id=business[0])
        except:
            input("Request failed. Press enter to retry.")
                    
        if (response["status"] == "OK"):
            return response
        else:
            print("Request error. Status: " + response["status"])
            input("Press enter to retry.")

# Connect to Google Maps API
API_KEY = input("Enter the API key: ")
gmaps = googlemaps.Client(key = API_KEY, timeout=5)

# Import business list
file_name = input("CSV file location: ")
business_list = open(file_name, "r", encoding="utf-8-sig", newline="")
business_data = csv.reader(business_list)
next(business_data)

output = []

for business in business_data:
    response = get_details(business[0])
    output.append(response["result"])

# json
json_dump = open("data/place_details_unprocessed.json", "w", encoding="utf-8-sig")
json.dump(output, json_dump)

# write to csv
def write_to_csv(business):
    name = business.get("name")
    place_id = business.get("place_id")
    plus_code = business.get("plus_code").get("global_code")

    address_components = business.get("address_components")
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


    location = business.get("geometry").get("location")
    latitude = location.get("lat")
    longitude = location.get("lng")

    curbside_pickup = business.get("curbside_pickup")
    price_level = business.get("price_level")
    rating = business.get("rating")
    user_ratings_total = business.get("user_ratings_total")

    details = [place_id, name, plus_code, street_number, route, neighborhood, township, postal_code, latitude, longitude, curbside_pickup, price_level, rating, user_ratings_total]

    # WIP
    opening_hours = business.get("opening_hours")

    for day in opening_hours["periods"]:
        open = day["open"]["time"]
        close = day["close"]["time"]

        details.append(open)
        details.append(close)

    csv_writer.writerow(details)

# csv
data_output = open("data/place_details.csv", "w", encoding="utf-8-sig", newline='')
csv_writer = csv.writer(data_output)
csv_writer.writerow(["place_id", "name", "plus_code", "street_number", "route", "neighborhood", "township", "postal_code", "latitude", "longitude", "curbside_pickup", "price_level", "rating", "user_ratings_total", "mon_open", "mon_close", "tue_open", "tue_close", "wed_open", "wed_close", "thu_open", "thu_close", "fri_open", "fri_close", "sat_open", "sat_close", "sun_open", "sun_close"])

# Query businesses in list
for business in output:
    write_to_csv(business)

business_list.close()
json_dump.close()
data_output.close()