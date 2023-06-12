from abc import ABC, abstractmethod


class OffertFactory(ABC):
    @abstractmethod
    def get_offerts() -> None:
        """
        Default method for getting offerts
        """

        pass

    @staticmethod
    def offert_builder(**kwargs) -> dict:
        """
        Build final offert dict

        Arguments:
            **kwargs -- kwargs
                title {str} -- offert title
                url {str} -- offert url
                company {dict} -- company dict
                technologies {list} -- list of technologies
                locations {list} -- list of locations
                employmentTypes {list} -- list of employment types
                seniority {str} -- seniority
                workingMode {str} -- working mode
                description {str} -- offert description
                site {str} -- site name

        Returns:
            dict -- final offert dict

        Schema:
            {
                "title": str,
                "url": str,
                "company": {
                    "name": str,
                    "url": str,
                    "logo_url": str,
                },
                "technologies": list,
                "locations": list,
                "employmentTypes": list,
                "seniority": str,
                "workingMode": str,
                "description": str,
                "site": str,
            }
        """

        offert = {
            "title": kwargs.get("title", None),
            "url": kwargs.get("url", None),
            "company": kwargs.get("company", None),
            "technologies": kwargs.get("technologies", None),
            "locations": kwargs.get("locations", None),
            "employmentTypes": kwargs.get("employmentTypes", None),
            "seniority": kwargs.get("seniority", None),
            "workingMode": kwargs.get("workingMode", None),
            "description": kwargs.get("description", None),
            "site": kwargs.get("site", None),
        }

        return offert
