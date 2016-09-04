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

@app.route('/simple-IO', methods=['GET'])
def simpleIO():
  return render_template('simple-IO.html',
                           title='gpkitjs',
                           )

@app.route('/box', methods=['GET'])
def box():
  return render_template('box.html',
                           title='gpkitjs',
                           )
@app.route('/box-IO', methods=['GET'])
def boxIO():
  return render_template('box-IO.html',
                           title='gpkitjs',
                           )

@app.route('/tank', methods=['GET'])
def tank():
  return render_template('tank.html',
                           title='gpkitjs',
                           )

@app.route('/tank-IO', methods=['GET'])
def tankIO():
  return render_template('tank-IO.html',
                           title='gpkitjs',
                           )

@app.route('/wing', methods=['GET'])
def wing():
  return render_template('wing.html',
                           title='gpkitjs',
                           )

@app.route('/wing-IO', methods=['GET'])
def wingIO():
  return render_template('wing-IO.html',
                           title='gpkitjs',
                           )

@app.route('/beam', methods=['GET'])
def beam():
  return render_template('beam.html',
                           title='gpkitjs',
                           )

@app.route('/beam-IO', methods=['GET'])
def beamIO():
  return render_template('beam-IO.html',
                           title='gpkitjs',
                           )


@app.route('/simple', methods=['POST'])
@app.route('/box', methods=['POST'])
@app.route('/tank', methods=['POST'])
@app.route('/wing', methods=['POST'])
@app.route('/beam', methods=['POST'])
@app.route('/simple-IO', methods=['POST'])
@app.route('/box-IO', methods=['POST'])
@app.route('/tank-IO', methods=['POST'])
@app.route('/wing-IO', methods=['POST'])
@app.route('/beam-IO', methods=['POST'])
def solve():
  r= request.form
  print(r)
  for line in r:
  	resultString = str(line);
  solver = gpkitjs.Solver();
  solver.initFromRequest(request)
  return solver.solve()
