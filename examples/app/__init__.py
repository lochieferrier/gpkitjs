from flask import Flask
app = Flask(__name__,static_folder='../../../gpkitjs')
app.config.from_object('config')
from app import views