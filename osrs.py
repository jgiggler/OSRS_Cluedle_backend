from osrsbox import items_api, monsters_api


import random

def load_monsters():
    # load monsters from osrsbox api
    monsters = monsters_api.load()
    monsters_no_dupe = {}

    print("adding monsters to no dupes dictionary")
    for i in monsters:
        if i.name not in monsters_no_dupe:
            monsters_no_dupe[i.name] = i.examine

    return monsters_no_dupe

def random_monster(monsters_no_dupe):
    # select random monster
    return random.choice(list(monsters_no_dupe.items()))

def load_items():
    # load items from osrsbox api
    items = items_api.load()
    items_no_dupe = {}
    
    print("adding items to no dupes dictionary")
    for i in items:
        if i.name not in items_no_dupe:
            items_no_dupe[i.name] = i.icon

    return items_no_dupe

def random_item(items_no_dupe):
    # select random item
    return random.choice(list(items_no_dupe.items()))

