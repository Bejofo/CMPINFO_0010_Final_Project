import csv, math

# CONFIG
RADIUS = 1

# Geographical information
KM_PER_LONGITUDE = 84.82
KM_PER_LATITUDE = 111.64

# Calculate incidents within radius
def km_distance(lng1, lat1, lng2, lat2):
    x_dist = (lng2 - lng1) * KM_PER_LONGITUDE
    y_dist = (lat2 - lat1) * KM_PER_LATITUDE

    return math.sqrt(x_dist ** 2 + y_dist ** 2)

def incident_count(fire_incidents, lat, lng, radius):
    count = 0

    # count nearby incidents
    for incident in fire_incidents:
        lng2 = incident.get("X")
        lat2 = incident.get("Y")

        if lng2 != "":
            if km_distance(lng, lat, float(lng2), float(lat2)) <= radius:
                count += 1
    
    return count

output = []

# load datasets
with open("datasets/business_list/business_list.csv", "r", encoding="utf-8-sig") as business_data:
    with open("datasets/police_incidents/assets/police_incidents.csv", "r") as fire_data:
        business_list = csv.DictReader(business_data)
        fire_incidents = [incident for incident in csv.DictReader(fire_data)]

        for business in business_list:
            place_id = business["place_id"]
            lng = float(business["longitude"])
            lat = float(business["latitude"])
            count = incident_count(fire_incidents, lat, lng, RADIUS)
                
            output.append([place_id, count])

# csv
with open("datasets/police_incidents/nearby_police_incidents.csv", "w", encoding="utf-8-sig", newline="") as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(["place_id", "count"])
    csv_writer.writerows(output)