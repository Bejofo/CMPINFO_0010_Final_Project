import csv
import pandas
from scipy.interpolate import LinearNDInterpolator

# Only use data from 2022
air_quality = pandas.read_csv("datasets/air_quality/assets/air_quality.csv")
sensors = pandas.read_csv("datasets/air_quality/assets/sites.csv")

# Some filtering
air_quality = air_quality.tail(7097) # Use only 2022 data
sensors = sensors[sensors["latitude"].notnull()]

# Group and merge
air_quality = air_quality.groupby(["site", "parameter"]).mean(numeric_only = True).groupby("site").max()
air_quality = air_quality.merge(sensors, left_on="site", right_on="site_name")
air_quality = air_quality[air_quality["index_value"].notnull()]
air_quality = air_quality[air_quality["site_name"].notnull()]

# Create model and create interpolated values
longitude = air_quality["longitude"]
latitude = air_quality["latitude"]
value = air_quality["index_value"]
model = LinearNDInterpolator(list(zip(longitude, latitude)), value)

# Calculate AQI for each business
output = []

with open("datasets/business_list/business_list.csv", "r", encoding="utf-8-sig") as business_data:
    business_list = csv.DictReader(business_data)

    for business in business_list:
        place_id = business["place_id"]
        neighborhood = business["neighborhood"]
        lng = float(business["longitude"])
        lat = float(business["latitude"])
        aqi = model(lng, lat)

        output.append([place_id, neighborhood, aqi])

# write to csv
with open("datasets/air_quality/air_quality.csv", "w", encoding="utf-8-sig", newline="") as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(["place_id", "neighborhood", "index_value"])
    csv_writer.writerows(output)