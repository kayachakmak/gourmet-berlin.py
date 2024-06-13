from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
import redis

load_dotenv()


app=Flask(__name__)
CORS(app, supports_credentials=True)

db_path = os.path.join(os.path.dirname(__file__), 'mydatabase.db')
print(f"Database will be created at: {db_path}")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
app.config["SQLALCHEMY_ECHO"]= True
app.config["SECRET_KEY"]=os.environ["SECRET_KEY"]
app.config["SESSION_TYPE"]= "redis"
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_USE_SIGNER"]= True
app.config["SESSION_REDIS"]= redis.from_url("redis://127.0.0.1:6379")


db=SQLAlchemy(app)