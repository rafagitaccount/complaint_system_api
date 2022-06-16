import json
from decouple import config
from fastapi import HTTPException, status

import requests


class WiseService:
    def __init__(self):
        self.main_url = config("WISE_URL")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}"
        }
        self.profile_id = self._get_profile_id

    def _get_profile_id(self):
        url = self.main_url + "/v1/profiles"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return [el["id"] for el in resp if el["type"] == "personal"][0]
        print(resp)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            "Payment provider is not available at the moment")

    def create_quote(self, amount):
        url = self.main_url + "/v2/quotes"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": amount,
            "profile": self.profile_id
        }

        resp = requests.post(url, headers=self.headers, data=json.dumps(data))

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        print(resp)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            "Payment provider is not available at the moment")

if __name__ == "__main__":
    wise = WiseService()
    res = wise.create_quote(50)
    a = 5