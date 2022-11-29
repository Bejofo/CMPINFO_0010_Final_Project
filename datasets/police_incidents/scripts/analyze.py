import csv
from nearby_incidents import get_nearby_incidents

# CONFIG
RADIUS = 1

output = get_nearby_incidents("datasets/business_list/business_list.csv", "datasets/police_incidents/assets/police_incidents.csv", RADIUS, "Y", "X")

# write to csv
with open("datasets/police_incidents/nearby_police_incidents.csv", "w", encoding="utf-8-sig", newline="") as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(["place_id", "neighborhood", "count"])
    csv_writer.writerows(output)