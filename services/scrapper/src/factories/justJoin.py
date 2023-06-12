import requests
import ujson
import locale

from offertFactory import OffertFactory
from utils.geoUtils import GeoUtils


class JustJoinOfferts(OffertFactory):
    def get_offerts() -> dict:
        def parse_offert(offert: dict) -> dict:
            """
            Parse offerts to format that is used in database to allow inserting to database

            Arguments:
                offert {dict} -- offert data in json format

            Returns:
                dict -- offert in format that is used in database
            """

            employmentType = parse_employment_type(offert["employment_types"])

            technologies = [tag["name"] for tag in offert["skills"]]
            locations = parse_locations(
                offert=offert
            )  # [location["city"] for location in offert["multilocation"]]
            url = "https://justjoin.it/offers/" + offert["id"]

            offert = OffertFactory.offert_builder(
                title=offert["title"],
                url=url,
                company={
                    "name": offert["company_name"],
                    "url": offert["company_url"],
                    "logo_url": offert["company_logo_url"],
                },
                technologies=technologies,
                locations=locations,
                employmentTypes=employmentType,
                seniority=offert["experience_level"],
                workingMode=offert["workplace_type"],
                description=offert["body"],
                site="justjoin.it",
            )

            # offert = {
            #     "title": offert["title"],
            #     "url": url,
            #     "company": {
            #         "name": offert["company_name"],
            #         "url": offert["company_url"],
            #         "logo_url": offert["company_logo_url"],
            #     },
            #     "technologies": technologies,
            #     "locations": locations,
            #     "employmentTypes": employmentType,
            #     "seniority": offert["experience_level"],
            #     "workingMode": offert["workplace_type"],
            #     "description": offert["body"],
            #     "site": "justjoin.it",
            # }

            return offert

        def parse_locations(offert: dict) -> list:
            """
            Parse locations to format that is used in database

            Arguments:
                offert {dict} -- offert data in json format

            Returns:
                list -- list of locations in format that is used in database
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
                    geo_u.location_builder(
                        country=country,
                        city=city,
                        street=street,
                        geoLocation=geoLocation,
                    )
                )

            locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")

            _locations = sorted(_locations, key=lambda k: locale.strxfrm(k["city"]))

            return _locations

        def parse_employment_type(employment_types):
            """
            Parse employment types to format that is used in database

            Arguments:
                employment_types {list} -- list of employment types

            Returns:
                list -- list of employment types in format that is used in database
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
            """
            Convert salary to PLN

            Arguments:
                salary {dict} -- salary in format that is used in database
                currency {str} -- currency of salary

            Returns:
                dict -- salary in PLN [from, to]
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
