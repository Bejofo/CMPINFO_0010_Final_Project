import json, time
import googlemaps
from shapely.geometry import shape, Point

class API_Session:
    def __init__(self, api_key):
        self.client = googlemaps.Client(key = api_key, timeout=5)
        self.calls = 0

    def call(self, func_name, *args):
        while (True):
            try:
                response = getattr(self, func_name)(*args)
                self.calls += 1
                
                if (response["status"] == "OK"):
                    return response
                else:
                    print("Request error. Status: " + response["status"])
                    input("Press enter to retry.")
            except:
                input("Request failed. Press enter to retry.")

    def first_page(self, latitude, longitude, search_radius, types):
        return self.client.places(location=(latitude, longitude), radius=search_radius, type=types)

    def next_page(self, token):
        return self.client.places(page_token=token)

    def place_details(self, id):
        return self.client.place(place_id=id)

    def get_pages(self, latitude, longitude, search_radius, type, id_list):
        pages = []

        # First page
        page1 = self.call("first_page", latitude, longitude, search_radius, type)
        current_page = page1
        pages.append(page1["results"])

        # Additional pages
        while True:
            token = current_page.get("next_page_token")

            if self.duplicate_count(id_list, current_page["results"]) == 20 or token == None:
                break
            
            time.sleep(2)

            current_page = self.call("next_page", token)
            pages.append(current_page["results"])
        
        return pages

    def duplicate_count(id_list, page):
        count = 0
        
        for business in page:
            place_id = business["place_id"]

            if place_id in id_list:
                count += 1
            else:
                id_list.append(place_id)

        return count

class Reverse_Geocoder:
    def __init__(self, file_path, region_name_attr = None):
        self.regions = []

        with open(file_path, "r") as map:
            data = json.load(map)
            features = data["features"]

            for feature in features:
                region_name = feature["properties"][region_name_attr] if region_name_attr != None else None
                coordinates = feature["geometry"]
                polygon = shape(coordinates)

                self.regions.append({"name": region_name, "shape": polygon})

    def contains(self, latitude, longitude):
        for region in self.regions:
            point = Point(longitude, latitude)
            
            if region["shape"].contains(point):
                return True
        
        return False

    def get_region(self, latitude, longitude):
        for region in self.regions:
            point = Point(longitude, latitude)

            if region["shape"].contains(point):
                return region["name"]
        
        return None