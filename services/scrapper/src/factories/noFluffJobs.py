import requests
import ujson
import locale

from offertFactory import OffertFactory
from utils.geoUtils import GeoUtils


class NoFluffJobs(OffertFactory):
    def get_offerts() -> dict:
        def parse_offert(offert: dict, offert_details: dict = None) -> dict:
            """
            Parse offert to format that is used in database

            Arguments:
                offert -- non parsed offert in JSON format
                offert_details -- not necessary -- collected at run time

            Returns:
                dict -- parsed offert in format that is used in database
            """

            try:
                r = requests.get(
                    f'https://nofluffjobs.com/api/posting/{offert["id"]}', timeout=60
                )
            except requests.exceptions.Timeout:
                return None

            if r.status_code != 200:
                return None

            offert_details = ujson.loads(r.text)

            url = "https://nofluffjobs.com/pl/job/" + offert["id"]
            technologies = parse_technologies(offert_details)
            locations = parse_locations(offert)
            senitorities = parse_seniorities(offert)
            employement_types = parse_employment_type(offert)
            languages = parse_languages(offert_details)
            logo_url = (
                f"https://static.nofluffjobs.com/{offert['logo']['original']}"
                if offert.get("logo", None) is not None
                else None
            )

            company_data = {
                "name": offert_details["company"].get("name", None),
                "url": offert_details["company"].get("url", None),
                "logo_url": logo_url,
            }

            offert = OffertFactory.offert_builder(
                title=offert["title"],
                url=url,
                company=company_data,
                technologies=technologies,
                locations=locations,
                employmentTypes=employement_types,
                seniority=senitorities,
                workingMode=offert["salary"]["type"],
                description=offert_details["details"]["description"],
                languages=languages,
                site="nofluffjobs.com",
            )

            return offert

        def parse_languages(offert_details: dict) -> list:
            """
            Parse languages to format that is used in database

            Arguments:
                offert_details -- offert details in json format

            Returns:
                list -- list of languages in format that is used in database
            """

            _languages = []

            offert_details = offert_details.get("requirements", None)

            if offert_details is None:
                return _languages

            if offert_details.get("languages", None) is None:
                return _languages

            for lang in offert_details["languages"]:
                _languages.append({"type": lang["type"], "code": lang["code"]})

            return _languages

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

        def parse_employment_type(offert: dict) -> list:
            """
            Parse employment types to format that is used in database

            Arguments:
                offert -- offert data in json format

            Returns:
                list -- list of employment types in format that is used in database
            """

            result = []

            offert = offert.get("salary", None)

            if offert is None:
                return result

            r = {}

            if offert.get("type", None) is not None:
                r["type"] = offert["type"]

            if offert.get("currency", None) is not None:
                r["salary"] = {"baseCurrency": str(offert["currency"]).upper()}

                if (
                    offert.get("from", None) is not None
                    and offert.get("to", None) is not None
                ):
                    r["salary"][r["salary"]["baseCurrency"]] = {
                        "from": offert["from"],
                        "to": offert["to"],
                    }

                    if offert["currency"].upper() != "PLN":
                        r["salary"]["pln"] = convert_to_pln(
                            r["salary"][offert["currency"].upper()],
                            r["salary"]["baseCurrency"],
                        )

            result.append(r)

            return result

        def parse_seniorities(offert: dict) -> list:
            """
            Parse seniorities to format that is used in database

            Arguments:
                offert -- offert data in json format

            Returns:
                list -- list of seniorities in format that is used in database
            """

            _seniorities = []

            seniorities = offert.get("seniority", None)

            if seniorities is None:
                return _seniorities

            for seniority in seniorities:
                _seniorities.append(seniority)

            return _seniorities

        def parse_technologies(offert_details: dict) -> list:
            """
            Parse technologies to format that is used in database

            Arguments:
                offert_details {dict} -- offert details in json format

            Returns:
                list -- list of technologies in format that is used in database
            """

            _technologies = []

            offert_details = offert_details.get("requirements", None)

            if offert_details is None:
                return _technologies

            if offert_details.get("musts", None) is None:
                return _technologies

            for technology in offert_details["musts"]:
                _technologies.append(technology["value"])

            return _technologies

        def parse_locations(offert: dict) -> list:
            """
            Parse locations to format that is used in database

            Arguments:
                offert -- offert data in json format

            Returns:
                list -- list of locations in format that is used in database
            """

            geo_u = GeoUtils()

            _locations = []

            locations = offert.get("location", None)
            if locations is None:
                return _locations

            for location in locations["places"]:
                if location.get("country", None) is None:
                    continue

                city = location.get("city", None)
                street = location.get("street", None)
                postal_code = location.get("postalCode", None)

                country = location.get("country", None)
                if country is not None:
                    country = country.get("name", None)

                if city is None or country is None:
                    return geo_u.location_builder()

                geoLocation = location.get("geoLocation", None)

                if geoLocation is None:
                    _cords = geo_u.city_to_coords(city_name=city, country=country)

                    if _cords is not None:
                        geoLocation = {
                            "latitude": _cords[0],
                            "longitude": _cords[1],
                        }

                final_location = geo_u.location_builder(
                    country=country,
                    city=city,
                    street=street,
                    postalCode=postal_code,
                    geoLocation=geoLocation,
                )

                _locations.append(final_location)

            locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")

            _locations = sorted(_locations, key=lambda k: locale.strxfrm(k["city"]))

            return _locations

        # ------------
        # |-- BODY --|
        # ------------

        r = requests.get(
            "https://nofluffjobs.com/api/posting/",
            timeout=60,
            headers={"Content-Encoding": "gzip"},
        )
        json = ujson.loads(r.text)

        parsed_offerts = []

        offerts_length = len(json["postings"])

        for idx, offert in enumerate(json["postings"][:100]):
            parsed_offert = parse_offert(offert)
            if parsed_offert is not None:
                parsed_offerts.append(parsed_offert)
            print(
                f"Successfully parsed [{idx+1}/{offerts_length}] offerts [nofluffjobs.com]"
            )

        return parsed_offerts
