import sqlite3
import pycountry

from typing import Tuple
from geopy.geocoders import Nominatim


class GeoUtils:
    def __init__(self):
        self.cache = self.Cache()
        self.geolocator = Nominatim(user_agent="offerts")

    class Cache:
        def database(self) -> sqlite3.Connection:
            return sqlite3.connect("cities.sqlite3")

        def retrieve_city_cords(self, city_name: str, country: str = None) -> Tuple:
            """
            Returns tuple of (latitude, longitude) or None if not found

            Arguments:
                city_name {str} -- City name
                country {str} -- Country name

            Returns:
                tuple -- (latitude, longitude) or None if not found
            """
            db = self.database()
            curr = db.cursor()

            city_name = city_name.lower()
            country = country.lower()

            if country is None:
                curr.execute(
                    """
                SELECT latitude, longitude FROM cords WHERE city = ?
                """,
                    (city_name,),
                )
            else:
                curr.execute(
                    """
                SELECT latitude, longitude FROM cords WHERE city = ? AND country = ?
                """,
                    (city_name, country),
                )

            cords = curr.fetchone()

            if cords is None:
                return None

            return cords

        def save_city_cords(
            self, city_name: str, country: str, latitude: float, longitude: float
        ) -> None:
            """
            Saves city cords to database

            Arguments:
                city_name {str} -- City name
                country {str} -- Country name
                latitude {float} -- Latitude
                longitude {float} -- Longitude
            """
            db = self.database()
            curr = db.cursor()

            city_name = city_name.lower()
            country = country.lower()

            curr.execute(
                """
                INSERT INTO cords VALUES (?, ?, ?, ?)
                """,
                (city_name, country, latitude, longitude),
            )

            db.commit()

    def city_to_coords(self, city_name: str, country: str) -> Tuple:
        """
        Returns tuple of (latitude, longitude) or None if not found

        Arguments:
            city_name {str} -- City name
            country {str} -- Country name

        Returns:
            tuple -- (latitude, longitude) or None if not found
        """

        cords = self.cache.retrieve_city_cords(city_name, country)

        if cords is not None:
            return cords

        location = self.geolocator.geocode(country + " " + city_name)

        if location is None:
            return None

        self.cache.save_city_cords(
            city_name, country, location.latitude, location.longitude
        )

        return (location.latitude, location.longitude)

    def country_code_to_name(self, country_code: str) -> str:
        """
        Convert country code to name

        Arguments:
            country_code {str} -- country code

        Returns:
            str -- country name
        """

        return pycountry.countries.get(alpha_2=country_code).name

    # def coords_to_city(latitude, longitude):
    #     #
    #     # NA RAZIE NIE JEST POTRZEBNE
    #     #

    #     """
    #     Returns city name or None if not found for given coords (latitute, longitude)

    #     Arguments:
    #         latitude {float} -- Latitude
    #         longitude {float} -- Longitude

    #     Returns:
    #         str -- City name or None if not found
    #     """

    #     geolocator = Nominatim(user_agent="offerts", timeout=10)

    #     location = geolocator.reverse(
    #         f"{latitude}, {longitude}", addressdetails=True, namedetails=True
    #     )

    #     if location is None:
    #         return None

    #     return location.raw["address"]["town"]

    # def city_street_to_coords(city_name, street_name):
    #     """
    #     Returns tuple of (latitude, longitude) or None if not found for given city and street

    #     Arguments:
    #         city_name {str} -- City name
    #         street_name {str} -- Street name

    #     Returns:
    #         tuple -- (latitude, longitude) or None if not found
    #     """

    #     geolocator = Nominatim(user_agent="offerts")
    #     location = geolocator.geocode(f"{street_name}, {city_name}")

    #     if location is None:
    #         return None

    #     return (location.latitude, location.longitude)
