from flask import Flask
from config import Config
import redis

print ("__init__")

app = Flask(__name__)
app.config.from_object(Config)



dbr = redis.Redis(host='localhost', port=6379, db=0)

from app import routes

