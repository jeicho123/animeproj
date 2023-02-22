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
    global char_name, quote

    if request.method == 'POST':
        post = request.form['search_query']    
        if anichan_request(post):
            char_name, quote = [*anichan_request(post)]
     
    mycursor.execute(f"SELECT img FROM Jikan WHERE name = '{char_name}'")
    image_url = mycursor.fetchone()[0]

    return render_template('index.html', image_url=image_url, quote=quote, char_name=char_name)

if __name__ == "__main__":
    app.run(debug=True)
