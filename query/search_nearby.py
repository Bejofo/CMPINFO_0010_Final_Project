import math, json, csv, time
from PIL import Image
import googlemaps

# Geographical information
SOUTH_LIMIT = 40.361370
WEST_LIMIT = -80.095286
NORTH_LIMIT = 40.500925
EAST_LIMIT = -79.865750
WEST_EAST_DIST_DEG = EAST_LIMIT - WEST_LIMIT
WEST_EAST_DIST_KM = 19.47 # 85 km per degree longitude
SOUTH_NORTH_DIST_DEG = NORTH_LIMIT - SOUTH_LIMIT
SOUTH_NORTH_DIST_KM = 15.58 # 111 km per degree latitude

# Query API
id_list = []

def get_pages(latitude, longitude, search_radius):
    pages = []

    # First page
    page1 = gmaps.places(location=(latitude, longitude), radius=search_radius, type="restaurant")
    current_page = page1
    pages.append(page1["results"])

    # Additional pages
    while True:
        token = current_page.get("next_page_token")

        if duplicate_count(current_page["results"]) == 20 or token == None:
            break
        
        time.sleep(2)

        current_page = gmaps.places(page_token=token)
        pages.append(current_page["results"])
    
    return pages

def first_page(latitude, longitude):
    while (True):
        try:
            response = gmaps.places(location=(latitude, longitude), radius=RADIUS_M, type="restaurant")
            
            if (response["status"] == "OK"):
                return response
            else:
                print("Request error. Status: " + response["status"])
                input("Press enter to retry.")
        except:
            input("Request failed. Press enter to retry.")

def next_page(token):
    while (True):
        try:
            response = gmaps.places(page_token=token)
            
            if (response["status"] == "OK"):
                return response
            else:
                print("Request error. Status: " + response["status"])
                input("Press enter to retry.")
        except:
            input("Request failed. Press enter to retry.")

def duplicate_count(page):
    count = 0
    
    for business in page:
        place_id = business["place_id"]

        if place_id in id_list:
            count += 1
        else:
            id_list.append(place_id)

    return count

# Connect to Google Maps API
API_KEY = input("Enter the API key: ")
gmaps = googlemaps.Client(key = API_KEY, timeout=5)

# Import map
map = Image.open("query/pittsburgh.png")
map.load()

# Search options
SPACING = float(input("Spacing (km): "))

# Calculate parameters
RADIUS = SPACING / 2
RADIUS_M = SPACING * 1000
X_INTERVALS = math.floor(WEST_EAST_DIST_KM / SPACING)
X_START = 1 / X_INTERVALS / 2
Y_INTERVALS = math.floor(SOUTH_NORTH_DIST_KM / SPACING)
Y_START = 1 / Y_INTERVALS / 2

output = []

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
            # API call
            pages = get_pages(latitude, longitude, RADIUS_M)

            for page in pages:
                output.append(page)

# json dump
json_dump = open("data/search_nearby_unprocessed_" + str(SPACING) + ".json", "w", encoding="utf-8-sig")
json.dump(output, json_dump)

# csv output
def write_to_csv(business):
    place_id = business.get("place_id")
    name = business.get("name")
    business_status = business.get("business_status")
    formatted_address = business.get("formatted_address")

    location = business.get("geometry").get("location")
    latitude = location.get("lat")
    longitude = location.get("lng")

    price_level = business.get("price_level")
    rating = business.get("rating")
    user_ratings_total = business.get("user_ratings_total")

    csv_writer.writerow([place_id, name, business_status, formatted_address, latitude, longitude, price_level, rating, user_ratings_total])

# write to csv
data_output = open("data/search_nearby_" + str(SPACING) + ".csv", "w", encoding="utf-8-sig", newline="")
csv_writer = csv.writer(data_output)
csv_writer.writerow(["place_id", "name", "business_status", "formatted_address", "latitude", "longitude", "price_level", "rating", "user_ratings_total"])

id_list = []

for page in output:
    for business in page:
        place_id = business["place_id"]

        # ignore duplicates
        if (place_id not in id_list):
            id_list.append(place_id)
            write_to_csv(business)

map.close()
json_dump.close()
data_output.close()