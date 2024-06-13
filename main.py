from flask import request, jsonify, session
from flask_bcrypt import Bcrypt
from config import app, db
from models import Comment, Restaurant, User
from load_data import load_data
from flask_session import Session

bcrypt= Bcrypt(app)
server_session=Session(app)

@app.route("/",methods=["GET"])
def get_restaurants():
    type=request.args.get("type")
    is_animal_friendly=request.args.get("animalFriendly")
    is_child_friendly = request.args.get('childFriendly')

    query=Restaurant.query
    
    if type:
        query=query.filter_by(type=type)
    if is_animal_friendly:
        query=query.filter_by(is_animal_friendly=True)
    if is_child_friendly:
        query=query.filter_by(is_child_friendly=True)
    
    restaurants=query.all()

    restaurants_json=[restaurant.to_json() for restaurant in restaurants]

    return jsonify(restaurants_json),200

    
   
@app.route("/<int:id>", methods=["GET","POST"])
def filter_restaurants(id):
    restaurant=Restaurant.query.get(id)

    if not restaurant:
        return jsonify({"message": "Restaurant not found"}), 404    
    
    comments=Comment.query.filter_by(restaurant_id=id).all()
    restaurant_json=restaurant.to_json()
    comments_json=[comment.to_json() for comment in comments]

    return jsonify({"restaurant": restaurant_json, "comments": comments_json}), 200

@app.route("/register", methods=["POST"])
def register_user():
    email=request.json["email"]
    password=request.json["password"]
    name=request.json["name"]

    user_exists=User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error":"User already exists"}),409

    hashed_password=bcrypt.generate_password_hash(password)
    new_user=User(email=email, password=hashed_password, name=name)
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    response = jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name
    }), 201


    return response

@app.route("/login", methods=["POST"])
def login():
    email=request.json["email"]
    password=request.json["password"]

    user=User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error":"Unauthorized"}),401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error":"Unauthorized"}),401
    
    session["user_id"]= user.id
    
    return jsonify({
        "id": user.id,
        "email": user.email
    })
         
@app.route("/@me")
def get_current_user():
    user_id=session.get("user_id")
    if not user_id:
        return jsonify({"error":"Unauthorized"}),401
    user=User.query.filter_by(id=user_id).first() 

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name":user.name
    })

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id")
    return "200"

@app.route("/create", methods=["POST"])
def create_restaurant():
    try:
        coordinates = request.json.get('coordinates')

        existing_location = Restaurant.query.filter_by(
            coordinates=coordinates
        ).first()

        if existing_location:
            return jsonify({"message": "Restaurant already exists"}), 409
        else:
            restaurant = Restaurant(
                name=request.json['name'],
                type=request.json['type'],
                menu=request.json.get("menu", ""),  # Used .get() for optional fields
                link=request.json.get("link", ""),  # Used .get() for optional fields
                image=request.json.get("image", ""),  # Used .get() for optional fields
                is_animal_friendly=request.json.get("isAnimalFriendly", False),  # Used .get() for optional fields
                is_child_friendly=request.json.get("isChildFriendly", False),  # Used .get() for optional fields
                coordinates=request.json.get('coordinates'),
                address=request.json["address"]
            )

            db.session.add(restaurant)
            db.session.commit()
            return jsonify({"message": "Restaurant successfully created"}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e), "message": "Please enter valid restaurant details"}), 400

@app.route("/comments", methods=["POST", "DELETE", "GET","PUT"])
def comments():
    if request.method == "POST":
        try:
            comment = Comment(
                name=request.json.get("name"),
                comment=request.json.get("comment"),
                date=request.json.get("date"),
                restaurant_id=request.json.get("restaurantID"),
                edit_date=request.json.get("editDate")
            )
            db.session.add(comment)
            db.session.commit()
            return jsonify({"message": "Comment added"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == "DELETE":
        try:
            id = request.json.get("id")
            comment = Comment.query.get(id)
            if comment:
                db.session.delete(comment)
                db.session.commit()
                return jsonify({"message": "Comment deleted"}), 200
            else:
                return jsonify({"message": "Comment not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == "GET":
        try:
            query=request.query.get("restaurantID")
            comments = Comment.query.filter_by(restaurant_id=query).all()
            comments_list = [
                {
                    "id": comment.id,
                    "name": comment.name,
                    "comment": comment.comment,
                    "date": comment.date,
                    "restaurant_id": comment.restaurant_id,
                    "edit_date": comment.edit_date,
                } for comment in comments
            ]
            return jsonify(comments_list), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method=="PUT":
        try:
            data=request.json
            id = data.get("id")
            comment = Comment.query.get(id)
            if comment:
                comment.comment=data.get("comment")
                comment.edit_date=data.get("editDate")
                db.session.commit()
                return jsonify({"message": "Comment updated"}), 200
            else:
                return jsonify({"message": "Comment not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

def reset_database():
    with app.app_context():
        db.drop_all()
        
        db.create_all()


if __name__=="__main__":
    with app.app_context():
        load_data()
    app.run(debug=True)
