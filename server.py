from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from cryptography.fernet import Fernet

import osrs
import base64

items = osrs.load_items() #load all items before startup
monsters = osrs.load_monsters()

item_count = {}
for item in items:
    item_count.update({item.lower(): 0})

monsters_count = {}
for monster in monsters:
     monsters_count.update({monster.lower(): 0})
    

# key = Fernet.generate_key() #generate encryption key
# fernet = Fernet(key)

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
    
    # encName = fernet.encrypt(item[0].encode())
    encName = base64.b64encode(item[0].encode())
    return jsonify({"name": encName.decode(), "img": item[1]})


#guess check API Route
@app.route("/guesscheck", methods = ['POST'])
def guessCheck():
    
        guess = request.get_json()
        name = guess["name"] # encrypted
        
        response = guess["guess"]

        # decName = fernet.decrypt(name).decode()
        decName = base64.b64decode(name).decode()
        decName = decName.lower()
        print(decName)
        
        
        if response.lower() == decName:

            if item_count.get(decName) != None:
                item_count[decName] = item_count.get(decName) + 1 # increase value by 1
                
            return jsonify({'correct': True, 'count': item_count[decName]})
        else:   
          
            return jsonify({'correct': False, 'count': item_count[decName]})

@app.route("/monster")
def get_random_monster():
    monster = osrs.random_monster(monsters)
    print(monster[0])
    
    
    # encName = fernet.encrypt(item[0].encode())
    encName = base64.b64encode(monster[0].encode())
    return jsonify({"name": encName.decode(), "img": monster[1]})

#guess check API Route
@app.route("/guesscheckmonster", methods = ['POST'])
def guessCheckMonster():
    
        guess = request.get_json()
        name = guess["name"] # encrypted
        
        response = guess["guess"]

        # decName = fernet.decrypt(name).decode()
        decName = base64.b64decode(name).decode()
        decName = decName.lower()
        print(decName)
        
        
        if response.lower() == decName:

            if monsters_count.get(decName) != None:
                monsters_count[decName] = monsters_count.get(decName) + 1 # increase value by 1
                
            return jsonify({'correct': True, 'count': monsters_count[decName]})
        else:   
          
            return jsonify({'correct': False, 'count': monsters_count[decName]})
        

if __name__ == "__main__":
    app.run()
    
