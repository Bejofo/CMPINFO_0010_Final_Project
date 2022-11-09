import math, json, csv
from PIL import Image
import googlemaps

# Config
SPACING = 1

# Connect to Google Maps API
API_KEY = input("Enter the API key: ")
gmaps = googlemaps.Client(key = API_KEY, timeout=5)

# Geographical information
SOUTH_LIMIT = 40.361370
WEST_LIMIT = -80.095286
NORTH_LIMIT = 40.500925
EAST_LIMIT = -79.865750
WEST_EAST_DIST_DEG = EAST_LIMIT - WEST_LIMIT
WEST_EAST_DIST_KM = 19.47 # 85 km per degree longitude
SOUTH_NORTH_DIST_DEG = NORTH_LIMIT - SOUTH_LIMIT
SOUTH_NORTH_DIST_KM = 15.58 # 111 km per degree latitude

# Calculate parameters
RADIUS = SPACING / 2 * math.sqrt(2)
RADIUS_M = SPACING * 1000
X_INTERVALS = math.floor(WEST_EAST_DIST_KM / SPACING)
X_START = 1 / X_INTERVALS / 2
Y_INTERVALS = math.floor(SOUTH_NORTH_DIST_KM / SPACING)
Y_START = 1 / Y_INTERVALS / 2

# Import map
map = Image.open("query/pittsburgh.png")
map.load()

# json output
json_dump = open("data/search_nearby_unprocessed.json", "w", encoding="utf-8-sig")
json_export = []

# csv output
data_output = open("data/search_nearby.csv", "w", encoding="utf-8-sig", newline='')
csv_writer = csv.writer(data_output)
csv_writer.writerow(["place_id", "name", "business_status", "formatted_address", "latitude", "longitude", "price_level", "rating", "user_ratings_total"])

# Longitude
for x in range(X_INTERVALS):
    x_prop = X_START + x / X_INTERVALS
    pixel_x = math.floor(x_prop * (map.width - 1))
    longitude = WEST_LIMIT + x_prop * WEST_EAST_DIST_DEG

    # Latitude
    for y in range(Y_INTERVALS):
        y_prop = Y_START + y / Y_INTERVALS
        pixel_y = math.floor(y_prop * (map.height - 1))
        latitude = NORTH_LIMIT - y_prop * SOUTH_NORTH_DIST_DEG

        # Check intersection
        if (map.getpixel((pixel_x, pixel_y)) == (0, 0, 0, 255)):
            # Check API call status
            while (True):
                try:
                    response = gmaps.places(location=(latitude, longitude), radius=RADIUS_M, type="restaurant")
                except:
                    input("Request failed. Press enter to retry.")
            
                if (response["status"] == "OK"):
                    break
                else:
                    print("Request failed! Status: " + response["status"])
                    input("Press enter to retry.")

            # Process data
            data = response["results"]

            # json
            json_export.append(data)

            # csv
            for business in data:
                name = business.get("name")
                place_id = business.get("place_id")
                business_status = business.get("business_status")
                formatted_address = business.get("formatted_address")

                location = business.get("geometry").get("location")
                latitude = location.get("lat")
                longitude = location.get("lng")

                price_level = business.get("price_level")
                rating = business.get("rating")
                user_ratings_total = business.get("user_ratings_total")

                csv_writer.writerow([place_id, name, business_status, formatted_address, latitude, longitude, price_level, rating, user_ratings_total])

json.dump(json_export, json_dump)

map.close()
json_dump.close()
data_output.close()