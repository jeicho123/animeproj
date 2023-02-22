import requests
import json
import mysql.connector
import time

with open('character_cache.json', 'r') as f:
    cache = json.load(f)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
    )

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS anime")
mycursor.execute("USE anime")
mycursor.execute("DROP TABLE IF EXISTS Jikan")
mycursor.execute("CREATE TABLE Jikan ("
                 "ID INT AUTO_INCREMENT PRIMARY KEY, "
                 "name VARCHAR(50), "
                 "img VARCHAR(100)"
                 ") AUTO_INCREMENT=1")

for id in cache["ids"][:10]:
    response = requests.get(f"https://api.jikan.moe/v4/characters/{id}").json()["data"]
    insert_query = "INSERT INTO Jikan (name, img) VALUES (%s, %s)"
    data_tuple = (response["name"], response["images"]["jpg"]["image_url"])
    mycursor.execute(insert_query, data_tuple)
    time.sleep(3)
  
db.commit()


