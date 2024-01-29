from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from cryptography.fernet import Fernet

import osrs

items = osrs.load_items() #load all items before startup

item_count = {}
for item in items:
    item_count.update({item.lower(): 0})
# print(item_count)
    

key = Fernet.generate_key() #generate encryption key
fernet = Fernet(key)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    item = osrs.random_item(items)
    print(item[0])
    return jsonify({"item": item[0]})

#item API Route
@app.route("/item")
def get_random_item():
    item = osrs.random_item(items)
    print(item[0])
    
    encName = fernet.encrypt(item[0].encode())

    return jsonify({"name": encName.decode("utf-8"), "img": item[1]})

#guess check API Route
@app.route("/guesscheck", methods = ['POST'])

def guessCheck():
    
    guess = request.get_json()

    name = guess["name"] # encrypted
    response = guess["guess"]
    decName = fernet.decrypt(name).decode().lower()
    
    if response.lower() == decName:
        
        if item_count.get(decName) != None:
            item_count[decName] = item_count.get(decName) + 1 # increase value by 1
            
        return jsonify({'correct': True, 'count': item_count[decName]})
    
    else:
        return jsonify({'correct': False, 'count': item_count[decName]})
    

if __name__ == "__main__":
    app.run()
    
