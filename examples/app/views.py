from flask import render_template, flash, redirect
from app import app
from gpkit import Variable, Model
from gpkit.feasibility import feasibility_model
import wtforms
from flask.ext.wtf import Form
from wtforms.validators import DataRequired
from flask import request
from json import JSONEncoder
import json
import gpkitjs 

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html',
                           title='gpkitjs',
                           )

@app.route('/simple', methods=['GET'])
def simple():
  return render_template('simple.html',
                           title='gpkitjs',
                           )

@app.route('/box', methods=['GET'])
def box():
  return render_template('box.html',
                           title='gpkitjs',
                           )

@app.route('/tank', methods=['GET'])
def tank():
  return render_template('tank.html',
                           title='gpkitjs',
                           )

@app.route('/simple', methods=['POST'])
@app.route('/box', methods=['POST'])
@app.route('/tank', methods=['POST'])
def solve():
  r= request.form
  print(r)
  for line in r:
  	resultString = str(line);
  solver = gpkitjs.Solver();
  solver.initFromRequest(request)
  return solver.solve()
