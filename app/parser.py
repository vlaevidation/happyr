import os
import requests
from requests.auth import HTTPBasicAuth

IBM_API_URL = "https://gateway.watsonplatform.net/tone-analyzer/api"
IBM_API_KEY = os.environ.get("IBM_API_KEY")


def parse(message):
    # Given a message, return an int 1-5 happiness score, or something
    resp = requests.get(
        "{}/v3/tone".format(IBM_API_URL),
        params={
            "text": message,
            "sentences": False,
            "version": "2017-09-21"
        },
        auth=HTTPBasicAuth('apikey', IBM_API_KEY)
    )
    data = resp.json()
    print("Received data: {}".format(data))

    happiness = 3     # neutral
    if "document_tone" in data:
        for tone in data["document_tone"]["tones"]:
            if tone["tone_id"] == "joy":
                happiness += tone["score"] * 2
            elif tone["tone_id"] in ["sadness", "anger", "fear"]:
                happiness -= tone["score"] * 2

    if happiness > 5:
        happiness = 5
    if happiness < 0:
        happiness = 0
    return happiness


def respond_to(score):
    responses = {
        1: "Wow that is, literally, the worst.",
        2: "I'm sorry to hear that.",
        3: "Cool cool",
        4: "Great!",
        5: "Holy happiness Batman that's amazing!"
    }
    return responses.get(score, "")



