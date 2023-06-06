import requests
import ujson

from offertFactory import OffertFactory
from geoUtils import GeoUtils


class JustJoinOfferts(OffertFactory):
    def get_offerts() -> dict:
        def parse_offert(offert: dict) -> dict:
            """Parse offerts to format that is used in database to allow inserting to database

            Keyword arguments:
            offert -- non parsed offert in JSON format
            Return: parsed offert in format that is used in database
            """

            employmentType = parse_employment_type(offert["employment_types"])

            technologies = [tag["name"] for tag in offert["skills"]]
            locations = parse_locations(
                offert=offert
            )  # [location["city"] for location in offert["multilocation"]]
            url = "https://justjoin.it/offers/" + offert["id"]

            offert = {
                "title": offert["title"],
                "url": url,
                "company": {
                    "name": offert["company_name"],
                    "url": offert["company_url"],
                    "logo_url": offert["company_logo_url"],
                },
                "technologies": technologies,
                "locations": locations,
                "employmentTypes": employmentType,
                "seniority": offert["experience_level"],
                "workingMode": offert["workplace_type"],
                "description": offert["body"],
                "site": "justjoin.it",
            }

            return offert

        def _final_location_builder(**kwargs) -> dict:
            """
            Build final location dict

            Arguments:
                **kwargs -- kwargs

            Returns:
                dict -- final location dict
            """

            _default_geolocation = {
                "latitude": None,
                "longitude": None,
            }

            final_location = {
                "country": kwargs.get("country", None),
                "city": kwargs.get("city", None),
                "street": kwargs.get("street", None),
                "postalCode": kwargs.get("postalCode", None),
                "geoLocation": kwargs.get("geoLocation", _default_geolocation),
            }

            return final_location

        def parse_locations(offert: dict) -> list:
            """Parse locations to format that is used in database

            Keyword arguments:
            offert -- offert data in json format
            Return: list of locations in format that is used in database
            """

            geo_u = GeoUtils()

            _locations = []

            country = offert.get("country_code", None)
            if country is not None:
                country = geo_u.country_code_to_name(country)

            for location in offert.get("multilocation", []):
                city = location.get("city", None)
                street = location.get("street", None)

                if city is None or country is None:
                    continue

                geoLocation = geo_u.city_to_coords(city_name=city, country=country)

                _locations.append(
                    _final_location_builder(
                        country=country,
                        city=city,
                        street=street,
                        geoLocation=geoLocation,
                    )
                )

            return _locations

        def parse_employment_type(employment_types):
            """parse employment types to format that is used in database

            Keyword arguments:
            employment_types -- description of employment types in JSON format
            Return: parsed employment types in format that is used in database
            """

            result = []

            for employment_type in employment_types:
                if employment_type.get("salary", None) is not None:
                    currency = employment_type["salary"]["currency"]

                    result.append(
                        {
                            "type": employment_type["type"],
                            "salary": {
                                "baseCurrency": currency,
                                currency: {
                                    "from": employment_type["salary"]["from"],
                                    "to": employment_type["salary"]["to"],
                                },
                            },
                        }
                    )

                    if currency != "pln":
                        result[-1]["salary"]["pln"] = convert_to_pln(
                            result[-1]["salary"][currency], currency
                        )
                else:
                    result.append({"type": employment_type["type"]})

            return result

        def convert_to_pln(salary: dict, currency: str) -> dict:
            """Convert salary to PLN if not in PLN to allow sorting by salary

            Keyword arguments:
            salary -- {from: int, to: int} salary in given currency
            currency -- currency of salary
            Return: {from: int, to: int} salary in PLN
            """

            r = requests.get(
                f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json"
            )

            json = ujson.loads(r.text)
            rate = json["rates"][0]["mid"]

            return {
                "from": round(salary["from"] * rate, -1),
                "to": round(salary["to"] * rate, -1),
            }

        def get_details(offert_url: str) -> dict:
            r = requests.get(offert_url)
            json = ujson.loads(r.text)

            return parse_offert(json)

        # ------------
        # |-- BODY --|
        # ------------

        r = requests.get("https://justjoin.it/api/offers")
        json = ujson.loads(r.text)

        parsed_offerts = []
        for i, offert in enumerate(json[:10]):
            detailed_offert = get_details(
                "https://justjoin.it/api/offers/" + offert["id"]
            )
            parsed_offerts.append(detailed_offert)
            print(f"Successfully parsed [{i+1}/1000] offerts [justjoin.it]")

        return parsed_offerts
