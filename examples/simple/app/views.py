from flask import render_template, flash, redirect
from app import app
from gpkit import Variable, Model
from gpkit.feasibility import feasibility_model
import wtforms
from flask.ext.wtf import Form
from wtforms.validators import DataRequired
from flask import request
import json

@app.route('/')
@app.route('/index')
def index():
  flash('hello world')
  
  return render_template('base.html',
                           title='gpkitjs',
                           )