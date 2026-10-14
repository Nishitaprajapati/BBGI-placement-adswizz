import os
import requests
from dotenv import load_dotenv

load_dotenv()
ADSWIZZ_BASE_URL=os.getenv("ADSWIZZ_BASE_URL")

class AdswizzClient:
    def __init__(self):
        self.api_key = os.getenv("ADSWIZZ_API_KEY")
        if not self.api_key:
            raise EnvironmentError("Missing Adswizz API key.")

    def send_campaign_data(self, data):
        headers = {
            "x-api-key": self.api_key,  
            "agency":str(10)
        }
        campaign_json = data["data"]

        attributes = campaign_json["attributes"]
        relationships = campaign_json["relationships"]

        payload = {
            "campaign_id": campaign_json["id"],
            "name": attributes["name"],
            "start_date": attributes["start-date"].split("T")[0],  # Only 'YYYY-MM-DD'
            "end_date": attributes["end-date"].split("T")[0],
            "budget": float(attributes["budget"]),
            "currency": attributes["currency-code"],
            "status": "DRAFT" if attributes["approval-status"] == "draft" else "ACTIVE",
            "time_zone": attributes["time-zone"],
            "advertiser_id": relationships["advertiser"]["data"]["id"] if relationships["advertiser"]["data"] else None,
            "agency_id": relationships["agency"]["data"]["id"] if relationships["agency"]["data"] else None,
            "owner_id": relationships["owner"]["data"]["id"] if relationships["owner"]["data"] else None,
            "bill_to_account": relationships["bill-to-account"]["data"]["id"] if relationships["bill-to-account"]["data"] else None,
            "line_items_url": relationships["line-items"]["links"]["related"],
            "groups_url": relationships["groups"]["links"]["related"],
        }
        print("----payload--------",payload)

        try:
            response = requests.post(f"{ADSWIZZ_BASE_URL}/campaigns", json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"[Adswizz] Authentication or HTTP error: {e}")
        except Exception as e:
            print(f"[Adswizz] Unexpected error: {e}")
