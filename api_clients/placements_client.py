import os
import requests
from dotenv import load_dotenv

load_dotenv()
PLACEMENTS_BASE_URL=os.getenv("PLACEMENTS_BASE_URL")

class PlacementsClient:
    def __init__(self):
        self.token = os.getenv("PLACEMENTS_TOKEN")
        print(self.token)
        if not self.token:
            raise EnvironmentError("Missing Placements API key.")

    def get_campaign_data(self, campaign_id):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        try:
            response = requests.get(f"{PLACEMENTS_BASE_URL}/campaigns/{campaign_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"[Placements] Authentication or HTTP error: {e}")
        except Exception as e:
            print(f"[Placements] Unexpected error: {e}")
