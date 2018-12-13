import os
import requests
from requests.auth import HTTPBasicAuth

IBM_API_URL = "https://gateway.watsonplatform.net/tone-analyzer/api"
IBM_API_KEY = os.environ.get("IBM_API_KEY")


def parse(message):
    # Given a message, return an int 1-5 happiness score, or something
    resp = requests.get(
        "{}/v3/tone".format(IBM_API_URL),
        params={"text": message, "sentences": False},
        auth=HTTPBasicAuth('apikey', IBM_API_KEY)
    )
    data = resp.json()
    print("Received data: {}".format(data))
    return 0



