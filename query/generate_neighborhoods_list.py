import csv

neighborhoods_google = []

with open("query/neighborhood_list.txt", "w", encoding="utf-8") as out:
    with open("data/business_list.csv", "r", encoding="utf-8-sig") as list:
        businesses = csv.reader(list)
        next(businesses)

        for business in businesses:
            neighborhood_name = business[7]

            if neighborhood_name != "" and neighborhood_name not in neighborhoods_google:
                neighborhoods_google.append(neighborhood_name)
                out.write(neighborhood_name + "\n")