from api_clients.adswizz_client import AdswizzClient
from api_clients.placements_client import PlacementsClient

def main():
    placements = PlacementsClient()
    adswizz = AdswizzClient()

    campaign_id = "635022"
    campaign_data = placements.get_campaign_data(campaign_id)

    if campaign_data:
        result = adswizz.send_campaign_data(campaign_data)
        if result:
            print("Campaign successfully sent to Adswizz.")
        else:
            print("Failed to send campaign to Adswizz.")
    else:
        print("Failed to retrieve campaign from Placements.")

if __name__ == "__main__":
    main()
