import requests
import utils
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def get_anime_character_image():
    response = requests.get("https://api.jikan.moe/v4/characters/117909/pictures")
    search_results = response.json()
    image_url = search_results["data"][0]["jpg"]["image_url"]
    return render_template('index.html', image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
