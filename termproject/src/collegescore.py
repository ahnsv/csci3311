import os
import requests


class CollegeScorecardClient:
    def __init__(self, api_key=None):
        self.base_url = "https://api.data.gov/ed/collegescorecard/v1/"
        self.api_key = api_key or "your_api_key_here"

    def get_data(self, endpoint, params=None):
        """
        Get data from the College Scorecard API

        Args:
            endpoint (str): API endpoint to query
            params (dict): Query parameters

        Returns:
            dict: JSON response from the API
        """
        if params is None:
            params = {}

        params["api_key"] = self.api_key

        response = requests.get(self.base_url + endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_institutions(self, fields=None, filters=None, page=0, per_page=100):
        """
        Get institution-level data

        Args:
            fields (list): Fields to return
            filters (dict): Filters to apply
            page (int): Page number
            per_page (int): Results per page

        Returns:
            dict: Institution data
        """
        params = {"page": page, "per_page": per_page}

        if fields:
            params["fields"] = ",".join(fields)

        if filters:
            for key, value in filters.items():
                params[key] = value

        return self.get_data("schools", params)


client = CollegeScorecardClient(api_key=os.getenv("COLLEGE_SCORECARD_API_KEY"))
