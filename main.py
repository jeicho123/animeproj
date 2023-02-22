import requests
import mysql.connector
from flask import Flask, render_template, request


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="anime"
    )

mycursor = db.cursor()
mycursor.execute(f"SELECT name FROM Jikan")
db_name = set([row[0] for row in mycursor.fetchall()])

def anichan_request(char_name="Spike Spiegel"):
    anichan_response = requests.get("https://animechan.vercel.app/api/random/character?name=" + char_name)
    if anichan_response.status_code == 200:
        parse = anichan_response.json()
        if parse["character"] in db_name:
            return (parse["character"], parse["quote"])
        else:
            return 
    return 

char_name, quote = [*anichan_request()]

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
