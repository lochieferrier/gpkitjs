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

@app.route('/testSolTable', methods=['GET'])
def box():
  return render_template('testSolTable.html',
                           title='gpkitjs',
                           )

@app.route('/testOperatorOverload', methods=['GET'])
def oper():
  return render_template('testOperatorOverload.html',
                           title='gpkitjs',
                           )

@app.route('/quadShoppingTest', methods=['GET'])
def quad():
  return render_template('quadShoppingTest.html',
                           title='gpkitjs',
                           )


@app.route('/testSolTable', methods=['POST'])
@app.route('/testOperatorOverload', methods=['POST'])
@app.route('/quadShoppingTest', methods=['POST'])
def solve():
  r= request.form
  print(r)
  for line in r:
  	resultString = str(line);
  solver = gpkitjs.Solver();
  solver.initFromRequest(request)
  return solver.solve()
