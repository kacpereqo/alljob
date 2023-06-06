#
# USED ONLY FOR STATS PURPOSES
#

import sqlite3

from offerts.geoUtils import GeoUtils

geo_u = GeoUtils()

x = geo_u.city_to_coords("Trzebinia", "Poland")
print(x)


# from database.db import DB


# def most_common():
#     x = DB.get_offerts_cities()

#     stats = {}

#     for i in x:
#         # print(i, end="\n\n")
#         for a in i["locations"]:
#             # print(a["city"])
#             if a["city"] == None:
#                 continue

#             if a["city"] in stats:
#                 stats[a["city"]] += 1
#             else:
#                 stats[a["city"]] = 1

#             # if a["city"] == None:
#             #     print(i)

#     stats = {k: v for k, v in sorted(stats.items(), key=lambda item: item[1])}

#     return stats

#     # for a, b in stats.items():
#     #     print(a, b)


# def get_cities():
#     x = DB.get_offerts_cities()

#     offert_locations = []  # [ [CITY, COUNTRY] ]

#     for i in x:
#         for a in i["locations"]:
#             if a["city"] == None:
#                 continue

#             offert_locations.append([a["city"], a["country"]])

#     return offert_locations


# def create_db(local_db):
#     local_db.execute(
#         """
#         CREATE TABLE IF NOT EXISTS cords (
#             city TEXT,
#             country TEXT,
#             latitude REAL,
#             longitude REAL
#         )
#     """
#     )

#     local_db.commit()


# stats = get_cities()
# local_db = sqlite3.connect("mostcommoncities.db")
# curr = local_db.cursor()

# create_db(local_db)

# for data in stats:
#     if (
#         data[0] == None
#         or data[1] == None
#         or data[0] == ""
#         or data[1] == ""
#         or data == []
#     ):
#         continue

#     city = data[0]
#     country = data[1]

#     city = city.lower()
#     country = country.lower()

#     curr.execute(
#         """
#         SELECT latitude, longitude FROM cords WHERE city = ? AND country = ?
#     """,
#         (city, country),
#     )

#     if curr.fetchone() is not None:
#         print("Already in db")
#         print(city, curr.fetchone())
#         print()
#         continue

#     cords = GeoUtils.city_to_coords(city, country)

#     if cords is None:
#         continue

#     curr.execute(
#         """
#         INSERT INTO cords VALUES (?, ?, ?,?)
#     """,
#         (city, country, cords[0], cords[1]),
#     )

#     print("Added to db")
#     print(city, cords)
#     print()

#     local_db.commit()

#     # curr.execute(
#     #     """
#     #     SELECT latitude, longitude FROM cords WHERE city = ? AND country_code = ?
#     # """,
#     #     (city, "PL"),
#     # )

#     # # if local_db.fetchone() is not None:
#     # #     print("Already in db")
#     # #     print(city, local_db.fetchone())
#     # #     continue

#     # cords = GeoUtils.city_to_coords(city)

#     # if cords is None:
#     #     continue

#     # curr.execute(
#     #     """
#     #     INSERT INTO cords VALUES (?, ?, ?,?)
#     # """,
#     #     (city, cords[0], cords[1]),
#     # )

#     # local_db.commit()
