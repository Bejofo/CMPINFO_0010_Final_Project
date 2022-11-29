import csv
from nearby_incidents import get_nearby_incidents

# CONFIG
RADIUS = 1

output = get_nearby_incidents("datasets/business_list/business_list.csv", "datasets/fire_incidents/assets/fire_incidents.csv", RADIUS, "latitude", "longitude")

# write to csv
with open("datasets/fire_incidents/nearby_fire_incidents.csv", "w", encoding="utf-8-sig", newline="") as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(["place_id", "neighborhood", "count"])
    csv_writer.writerows(output)