import requests
import json
from flask import Flask, render_template, request

with open('data/char_id.json', 'r') as f:
    cache = json.load(f)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    char_name = "Spike"

    if request.method == 'POST':
        char_name = request.form['search_query']

    anichan_response = requests.get("https://animechan.vercel.app/api/random/character?name=" + char_name)
    parsed_quote = anichan_response.json()
    quote = parsed_quote["quote"] 
    char_name = parsed_quote["character"]  
    id = cache[char_name]

    jikan_response = requests.get("https://api.jikan.moe/v4/characters/" + str(id) + "/pictures")
    parsed_img = jikan_response.json()
    image_url = parsed_img["data"][0]["jpg"]["image_url"]

    return render_template('index.html', image_url=image_url, quote=quote, char_name=char_name)

if __name__ == "__main__":
    app.run(debug=True)
