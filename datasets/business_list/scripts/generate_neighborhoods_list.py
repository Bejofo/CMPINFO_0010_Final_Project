import csv

neighborhoods_google = []

with open("datasets/business_list/assets/neighborhood_list.txt", "w", encoding="utf-8") as out:
    with open("datasets/business_list/business_list.csv", "r", encoding="utf-8-sig") as list:
        businesses = csv.DictReader(list)

        for business in businesses:
            neighborhood_name = business["neighborhood"]

            if neighborhood_name != "" and neighborhood_name not in neighborhoods_google:
                neighborhoods_google.append(neighborhood_name)
                out.write(neighborhood_name + "\n")