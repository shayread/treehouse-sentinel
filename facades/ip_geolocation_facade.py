import requests

# Documentation: https://ip-api.com/docs/api:json
class IPGeolocationFacade:

    ENDPOINT = "http://ip-api.com/json"

    def get_coordinates(self):
        response = requests.get(url=self.ENDPOINT)
        if response.ok:
            response_json = response.json()
            return response_json['lat'], response_json['lon']
        else:
            # Return null values since analyzer can function without coordinates
            print(f"WARNING: IP Geolocation request failed with status code {response.status_code} and "
                  f"reason {response.reason}. Proceeding to data collection without coordinates...")
            return None, None
        
    def get_location_info(self):
        response = requests.get(url=self.ENDPOINT)
        if response.ok:
            response_json = response.json()
            return {
                "country": response_json['country'],
                "region": response_json['regionName'],
                "city": response_json['city']
            }
        else:
            # Return "UNKNOWN" placeholder values to allow data collection to continue
            print(f"WARNING: IP Geolocation request failed with status code {response.status_code} and "
                  f"reason {response.reason}. Storing species identification without location information...")
            return {
                "country": "UNKNOWN",
                "region": "UNKNOWN",
                "city": "UNKNOWN"
            }
