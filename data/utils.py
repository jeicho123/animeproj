import requests
import json
import time

with open('character_cache.json', 'r') as f:
    cache = json.load(f)

char_id = {}


for id in cache["ids"][:10]:
    response = requests.get(f"https://api.jikan.moe/v4/characters/{id}").json()
    char_id[response["data"]["name"]] = id
    time.sleep(2)

with open('char_id.json', 'w') as f:
    json.dump(char_id, f)