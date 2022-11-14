import json
from shapely.geometry import shape, Point

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