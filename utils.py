import requests


response = requests.get("https://api.jikan.moe/v4/characters").json()

char_id = {}

for char in response["data"]:
    char_id[char["name"]] = char["mal_id"]
