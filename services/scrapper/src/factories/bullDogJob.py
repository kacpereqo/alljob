import requests
import ujson
import locale
import time

from bs4 import BeautifulSoup

from offertFactory import OffertFactory
from utils.geoUtils import GeoUtils


class BullDogJob(OffertFactory):
    def get_offerts() -> dict:
        url = "https://bulldogjob.pl/graphql"

        def parse_locations(offert: dict) -> list:
            geo_u = GeoUtils()
            _locations = []

            for location in offert["locations"]:
                country = "Poland"
                city = location["location"].get("cityPl", None)
                street = location.get("address", None)
                # bullDogJob doesn't provide postal code

                geoLocation = geo_u.city_to_coords(city_name=city, country=country)

                final_location = geo_u.location_builder(
                    country=country,
                    city=city,
                    street=street,
                    geoLocation=geoLocation,
                )

                _locations.append(final_location)

            locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")

            _locations = sorted(_locations, key=lambda k: locale.strxfrm(k["city"]))

            return _locations

        def parse_employment_type(offert: dict) -> list:
            def _salary_parser(salary: dict) -> dict:
                if salary:
                    salary = salary.replace(" ", "")
                    salary_range = salary.split("-")
                    if len(salary_range) == 2:
                        min_salary = int(salary_range[0])
                        max_salary = int(salary_range[1])
                        return min_salary, max_salary
                return None, None

            def _contract_type_parser(**kwargs) -> str:
                if kwargs.get("contractB2b", None):
                    return "b2b"

                if kwargs.get("contractEmployment", None):
                    return "permament"

                if kwargs.get("contractOther", None):
                    return "other"

                return None

            def convert_to_pln(salary: dict, currency: str) -> dict:
                """
                Convert salary to PLN if not in PLN to allow sorting by salary

                Keyword arguments:
                salary -- {from: int, to: int} salary in given currency
                currency -- currency of salary
                Return: {from: int, to: int} salary in PLN
                """

                r = requests.get(
                    f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json"
                )

                json = ujson.loads(r.text)
                rate = json["rates"][0].get("mid", 0)

                if salary["from"] is not None and salary["to"] is not None:
                    return {
                        "from": round(salary["from"] * rate, -1),
                        "to": round(salary["to"] * rate, -1),
                    }

                return {
                    "from": 0,
                    "to": 0,
                }

            employment_types = []

            salary = {
                "type": None,
                "salary": {
                    "baseCurrency": None,
                    "pln": {
                        "from": 0,
                        "to": 0,
                    },
                },
            }

            salary["type"] = _contract_type_parser(
                contractB2b=offert.get("contractB2b", None),
                contractEmployment=offert.get("contractEmployment", None),
                contractOther=offert.get("contractOther", None),
            )

            salary["salary"] = {
                "baseCurrency": offert["denominatedSalaryLong"].get("currency", None),
            }

            if salary["salary"]["baseCurrency"] is None:
                employment_types.append(salary)
                return employment_types

            min_salary, max_salary = _salary_parser(
                offert["denominatedSalaryLong"].get("money", None)
            )

            salary["salary"][salary["salary"]["baseCurrency"]] = {
                "from": min_salary,
                "to": max_salary,
            }

            if (
                salary["salary"]["baseCurrency"] != "pln"
                and salary["salary"]["baseCurrency"] != "PLN"
            ):
                salary["salary"]["pln"] = convert_to_pln(
                    salary=salary["salary"][salary["salary"]["baseCurrency"]],
                    currency=salary["salary"]["baseCurrency"],
                )

            employment_types.append(salary)

            return employment_types

        def parse_description(offert: dict) -> str:
            url = "https://bulldogjob.pl/companies/jobs/" + offert.get("id", None)

            iters = 0
            passed = False
            r = None

            while iters < 3 or not passed:
                try:
                    r = requests.get(url, timeout=1)
                    if r.status_code == 200:
                        passed = True
                except requests.exceptions.RequestException:
                    time.sleep(1)

                iters += 1

            if r is None or r.status_code != 200 or not passed:
                return None

            soup = BeautifulSoup(r.text, "html.parser")
            description = soup.find_all(
                "div", class_=["content", "list--check", "mt-6", "-mb-6"]
            )

            if not description:
                return None

            description = str(description[0].parent)
            return description

        def parse_experienceLevel(offert: dict) -> str:
            d = {
                "junior": "junior",
                "medium": "mid",
                "senior": "senior",
            }

            return [d.get(offert["experienceLevel"], offert["experienceLevel"])]

        def parse_working_mode(offert: dict) -> str:
            if offert["environment"].get("remotePossible", 0):
                x = offert["environment"].get("remotePossible", 0)

                if x >= 100:
                    return "remote"

                if x < 10:
                    return "office"

                if x < 100:
                    return "partly_remote"

            return None

        def parse_offert(offert: dict) -> dict:
            url = "https://bulldogjob.pl/companies/jobs/" + offert["id"]

            technologies = [tag["name"] for tag in offert["technologies"]]
            locations = parse_locations(offert=offert)
            employement_types = parse_employment_type(offert=offert)
            seniorities = parse_experienceLevel(offert=offert)
            working_modes = parse_working_mode(offert=offert)
            description = parse_description(offert=offert)

            company_data = {
                "name": offert["company"].get("name", None),
                "url": offert["company"].get("url", None),
                "logo_url": offert["company"].get("logo", {}).get("url", None),
            }

            offert = OffertFactory.offert_builder(
                title=offert["position"],
                url=url,
                company=company_data,
                technologies=technologies,
                locations=locations,
                employmentTypes=employement_types,
                seniorities=seniorities,
                workingMode=working_modes,
                description=description,
                languages=None,
                site="bulldogjob.com",
            )

            return offert

        def execute_graphql_query(url: str, query: str, variables: dict) -> dict:
            headers = {"Content-Type": "application/json"}
            data = {"query": query, "variables": variables}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            return result

        def get_all_offerts() -> dict:
            _offerts = []

            q = """
            query searchJobs(
            $page: Int
            $perPage: Int
            $filters: JobFilters
            $order: JobsSearchOrderBy
            $language: LocaleEnum
            $boostWhere: BoostWhere
            $exclude: [ID!]
            ) {
            searchJobs(
                page: $page
                perPage: $perPage
                filters: $filters
                order: $order
                language: $language
                boostWhere: $boostWhere
                exclude: $exclude
            ) {
                totalCount
                nodes {
                id
                company {
                    name
                    visible
                    verified
                    logo {
                    url(style: "list")
                    __typename
                    }
                    __typename
                }
                denominatedSalaryLong {
                    money
                    currency
                    hidden
                    __typename
                }
                highlight
                city
                experienceLevel
                locations {
                    address
                    location {
                    cityPl
                    cityEn
                    __typename
                    }
                    __typename
                }
                hiddenBrackets
                matchingUserBrackets
                position
                remote
                environment {
                    remotePossible
                    __typename
                }
                endsAt
                recruitmentProcess
                showSalary
                technologies {
                    level
                    name
                    __typename
                }
                contractB2b
                contractEmployment
                contractOther
                locale
                applied
                __typename
                }
                __typename
            }
            }
            """

            v = {"filters": {}, "language": "pl", "page": 1, "perPage": 100}

            graphql = execute_graphql_query(url, q, v)

            if graphql is None:
                return []

            _total_offerts = graphql["data"]["searchJobs"]["totalCount"]
            _total_offerts_pages = _total_offerts // 100 + 1

            for page in range(1, _total_offerts_pages + 1):
                v["page"] = page
                graphql = execute_graphql_query(url, q, v)
                _offerts += graphql["data"]["searchJobs"]["nodes"]

            return _offerts

        # ------------
        # |-- BODY --|
        # ------------

        offerts = get_all_offerts()

        parsed_offerts = []

        for idx, offert in enumerate(offerts[:100]):
            parsed_offert = parse_offert(offert)
            if parsed_offert is not None:
                parsed_offerts.append(parsed_offert)
            print(
                f"Successfully parsed [{idx+1}/{len(offerts)}] offerts [bulldogjob.com]"
            )

        return parsed_offerts
