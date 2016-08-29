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

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__  

@app.route('/')
@app.route('/index')
def index():
  flash('hello world')
  a = Variable('x')
  print(a)
  flash(a)
  return render_template('index.html',
                           title='gpkitjs',
                           )

@app.route('/index', methods=['POST'])
def indexUpdate():
  r= request.form
  print(r)
  for line in r:
  	resultString = str(line);
  ModelDict = json.loads(resultString)
  constraints = []
  varDict = {}
  for constraint in ModelDict["constraints"]:
  	if type(constraint["left"]) == dict:
  		varProperties = constraint["left"]
  		# inputVarsDict[varProperties["ID"]] = varProperties
  		tempVar = Variable(varProperties["name"])
  		constraint["left"] = tempVar
  		print(varProperties["ID"])
  		varDict[varProperties["ID"]] = tempVar
  	if constraint["oper"] == "geq":
  		constraints +=[constraint["left"] >= constraint["right"]]
  costDict = ModelDict["cost"]
  cost = varDict[costDict["ID"]]
  # costVar = Variable(cost["name"])
  # constraint["left"] = tempVar
  print('final inputs to normal model')
  x = Variable('x')
  constraintsNormal = []
  constraintsNormal += [x>=1]
  objectiveNormal = x
  print(objectiveNormal)
  print(constraintsNormal)

  mNormal = Model(objectiveNormal,constraintsNormal)
 
  print('final inputs to JS model')
  print(cost)
  print(constraints)
  m = Model(cost,constraints)
  sol = m.solve(verbosity=1)
  jsSol = gpkitjs.Solution()
  jsSol.translateSol(sol,varDict)
  output = MyEncoder().encode(jsSol)
  print output
  # print(varDict)
  # print r 
  # # print r[0]
  # a = []
  # for line in r:
  #   print 'new line'

  #   a = (json.loads(line))
  # print(str(a))
  # return str(a)
  return output
