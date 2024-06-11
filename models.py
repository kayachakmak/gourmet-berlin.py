from config import db
from sqlalchemy import JSON
from uuid import uuid4

class Restaurant(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(250), unique=False, nullable=False)
    type= db.Column(db.String(20), unique=False, nullable=False)
    address= db.Column(db.String(1000), unique=False, nullable=False)
    link= db.Column(db.String(250), unique=False)
    menu= db.Column(db.String(250), unique=False)
    image= db.Column(db.String(1000), unique=False)
    is_child_friendly= db.Column(db.Boolean, unique=False)
    is_animal_friendly= db.Column(db.Boolean, unique=False)
    coordinates=db.Column(JSON, unique= True,)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "type":self.type,
            "address":self.address,
            "link":self.link,
            "menu":self.menu,
            "image":self.image,
            "isChildFriendly":self.is_child_friendly,
            "isAnimalFriendly":self.is_animal_friendly,
            "coordinates":self.coordinates,
        }
    
class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255), nullable=False)
    comment=db.Column(db.Text, nullable=False)
    date=db.Column(db.String(255), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)    
    edit_date=db.Column(db.String(255), unique=False)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "comment":self.comment,
            "date":self.date,
            "restaurantID":self.restaurant_id,
            "editDate":self.edit_date,
        }

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.String(32),primary_key=True, unique= True, default=get_uuid)
    email=db.Column(db.String(345), unique=True)
    password=db.Column(db.Text, nullable=False)
    name=db.Column(db.String(300), unique=True)

