import json
from models import Restaurant
from config import db

def load_data():
    if Restaurant.query.first():
        return
    
    with open('restaurants.json') as file:
        data = json.load(file)

    for restaurant_data in data:
        restaurant = Restaurant(
            name=restaurant_data.get('name'),
            type=restaurant_data.get('type'),
            address=restaurant_data.get('address'),  # Make sure the key matches the updated attribute
            link=restaurant_data.get('link'),
            menu=restaurant_data.get('menu'),
            image=restaurant_data.get('image'),
            is_child_friendly=restaurant_data.get('isChildFriendly'),
            is_animal_friendly=restaurant_data.get('isAnimalFriendly'),
            coordinates=restaurant_data.get('coordinates')
        )
        db.session.add(restaurant)
    
    db.session.commit()
