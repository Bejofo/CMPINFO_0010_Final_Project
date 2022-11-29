import math, csv

# Geographical information
KM_PER_LONGITUDE = 84.82    
KM_PER_LATITUDE = 111.64

# Calculate distance
def km_distance(lat1, lng1, lat2, lng2):
    x_dist = (lng2 - lng1) * KM_PER_LONGITUDE
    y_dist = (lat2 - lat1) * KM_PER_LATITUDE

    return math.sqrt(x_dist ** 2 + y_dist ** 2)

# Calculate incidents within radius of business
def incident_count(incidents, lat, lng, radius, lat_attr, lng_attr):
    count = 0

    for incident in incidents:
        lat2 = incident.get(lat_attr)
        lng2 = incident.get(lng_attr)

        if lng2 != "":
            if km_distance(lat, lng, float(lat2), float(lng2)) <= radius:
                count += 1
    
    return count

def get_nearby_incidents(business_list_path, incident_list_path, radius, lat_attr, lng_attr):
    output = []
    
    # Open data files
    with open(business_list_path, "r", encoding="utf-8-sig") as business_data:
        with open(incident_list_path, "r") as incident_data:
            business_list = csv.DictReader(business_data)
            incidents = [incident for incident in csv.DictReader(incident_data)]

            # For each business
            for business in business_list:
                place_id = business["place_id"]
                neighborhood = business["neighborhood"]
                lng = float(business["longitude"])
                lat = float(business["latitude"])
                count = incident_count(incidents, lat, lng, radius, lat_attr, lng_attr)
                    
                output.append([place_id, neighborhood, count])
    
    return output