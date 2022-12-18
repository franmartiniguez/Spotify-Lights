BASE_64 = 'MTVkYjdkOWQwYTU2NDhkNWE2MTk4YzMyMzZjYjg2OTM6MDQ2NmI4NmVjNTZkNDYyOTkzNGU2NmViYTQ4NzJjNzk='
REFRESH_TOKEN = 'AQBCjhrIpqdm1u-OM-Ad2AJ8m5NwIDin7l2-BLDoBoxSoC0-S-s1aW42JnymtlqTPXi4SXfJj4Cb57aX0vOG2Rs6SW4lBu-rPggVvbMkyd4bShKyLq2tKKcpEwDosGaVUUo'
import requests
import json

class Refresh:

    def  __init__(self):
        self.refresh_token = REFRESH_TOKEN
        self.base64 = BASE_64
    
    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
                                data={"grant_type":"refresh_token","refresh_token":REFRESH_TOKEN},
                                headers={"Authorization": "Basic " + BASE_64})
        return response.json()['access_token']

a = Refresh()
print(a.refresh())