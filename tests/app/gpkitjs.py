# http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
print ('importing gpkit')
from gpkit import Variable as gpkitVariable
from gpkit import Signomial as gpkitSignomial
from gpkit import Model as gpkitModel
from gpkit import SignomialsEnabled
from gpkit import units
from gpkit.feasibility import feasibility_model
print ('done importing gpkit')
print('importing json encoder')
from json import JSONEncoder
import json
print('done importing json')
print('importing numpy')
import numpy as np
print('done importing numpy')
from cvxshopping import ShoppingCart

debug = False

# Parse a Solution object into JSON, filtering for fixed or free variables
class MyEncoder(JSONEncoder):
    def default(self, o):
    	if o.solveMessage == "success":
	    	cleanVarResults = {}
	    	for varKey in o.variables:
	    		var = o.variables[varKey]
	    		# print type(var)
	    		# print type(var.valArr[0])
	    		# print var.name
	    		cleanVarResults[varKey] = {"name":var.name,"valArr":var.valArr,"units":var.units,"label":var.label}
	    	# print cleanVarResults
	    	return json.dumps({'variables':cleanVarResults})
        else:
        	return o.solveMessage

class Solution(object):

	def __init__(self):
		self.variables = {}
		self.varDict = {}
		self.solveMessage = ""
	def translateSol(self,sol,varDict):
		if sol != "failedSolve":
			self.solveMessage = "success"
			for variableKey in varDict:
				variable = varDict[variableKey]
				self.variables[variableKey] = initVarFromGPkitSol(variable,sol)
			self.varDict = varDict

		if sol=="failedSolve":
			self.solveMessage = sol

def initVarFromGPkitSol(gpkitVar,sol):
	# Sol will return one of two things when we query for a var, either a pint quantity
	# or a numpy.float64 when it's something being optimized
	# print gpkitVar.__dict__
	name = gpkitVar.key.descr["name"]
	# print type(sol(gpkitVar))
	if isinstance(sol(gpkitVar),np.float64) or isinstance(sol(gpkitVar),np.int64):
		valArr = [float(sol(gpkitVar))]
	else:
		magArr = float(sol(gpkitVar)._magnitude)
		valArr = [magArr]

	# Units come back as either a pint quantity of magnitude 1 in the units described,
	# or as a unicode string of the units, in the format that pint uses.
	if isinstance(gpkitVar.units,unicode):
		units = str(gpkitVar.units)
	else:
		units = str(gpkitVar.units.units)

	if "label" in gpkitVar.__dict__:
		label = gpkitVar.label
	else:
		label = ""

	returnVar = Variable(name,valArr,units,label)

	return returnVar


class Variable(object):
	def __init__(self,name,valArr,units,label):
		self.name = name
		self.valArr = valArr
		self.units = units
		self.label = label


def parseJSVar(jsVar, varDict,returnVar=False):

	if type(jsVar) == dict:
		# for varKey in varDict:
		# 	# if jsVar["name"] == str(varDict[varKey].exps[0].keys()[0]):
		# 	# 	arrNameAppend = True
		if "name" in jsVar:
			if "val" in jsVar:
				jsVar["value"] = jsVar.pop("val")
			tempVar = gpkitVariable(**jsVar)
			print tempVar
			# We have all these variables coming in, but need to track which is which, this was the point
			# of the ID assignment
			# We store variables in a dictionary under JS ID
			if "ID" in jsVar:
				if jsVar["ID"] not in varDict:
					varDict[jsVar["ID"]] = tempVar
				else:
					tempVar = varDict[jsVar["ID"]]
				if returnVar:
					return tempVar
				else:
					return tempVar.key

class Solver(object):
	def __init__(self):
		self.modelDict = {}
	def initFromRequest(self,request):
		  r= request.form
		  for line in r:
		  	resultString = str(line);
		  self.modelDict = json.loads(resultString)

	def createSignomial(self,JSinput,varDict):
		# print JSinput

		# Handle a JS monomial
		if "expArr" in JSinput:
			expDictList = []
			constantsList = []
			expDict = {}
  			constant = 1
  			for variableArr in JSinput["expArr"]:
  				jsVar = variableArr[0]

  				if type(jsVar) == dict:
  					tempVar = parseJSVar(jsVar,varDict)
			  		expDict[tempVar] = variableArr[1]
  				else:
  					# If there isn't a name, it musn't be a variable, but instead
  					# a raw number
  					# print jsVar
  					constant*=jsVar
  			expDictList += [expDict]
  			constantsList += [constant]
		else:
			# Handle a JS posynomial
		  	if not JSinput["isSignomial"]:

		  		expDictList = []
		  		constantsList = []

		  		for monomial in JSinput["monomialsArr"]:
		  			expDict = {}
		  			constant = 1
		  			for variableArr in monomial["expArr"]:
		  				jsVar = variableArr[0]

		  				if type(jsVar) == dict:
		  					tempVar = parseJSVar(jsVar,varDict)
					  		expDict[tempVar] = variableArr[1]
		  				else:
		  					# If there isn't a name, it musn't be a variable, but instead
		  					# a raw number
		  					# print jsVar
		  					constant*=jsVar


		  			expDictList += [expDict]
		  			constantsList += [constant]

		sig = gpkitSignomial(tuple(expDictList),tuple(constantsList))
		return sig

	def solve(self):

	  constraints = []
	  varDict = {}

	  for constraint in self.modelDict["constraints"]:
		if constraint['constraintType'] in ["equality","inequality"]:
			# Check for Monomial equality, if something else just make signomial inequality
			# print constraint
			left = self.createSignomial(constraint['left'],varDict)
			right = self.createSignomial(constraint['right'],varDict)

			with SignomialsEnabled():
				if constraint['oper'] == "leq":
					constraints+=[left<=right]
				if constraint['oper'] == "geq":
					constraints+=[left>=right]
    				if constraint['oper'] == "eq":
					constraints+=[left==right]
		if constraint['constraintType'] == "shopping-cart":
				goods = {}
				# print constraint
				for parameter in constraint['goods']:
					gpVariable = parseJSVar(parameter[0],varDict,returnVar=True)
					options = parameter[1]*getattr(units,parameter[2])
					print options.__dict__
					print type(options)
					print gpVariable.__dict__
					print type(gpVariable)
					goods[gpVariable] = options
				bads = {}
				for pair in constraint['bads']:
					gpVariable = parseJSVar(pair[0],varDict,returnVar=True)
					options = pair[1]*getattr(units,pair[2])
					print options.__dict__
					print type(options)
					print gpVariable.__dict__
					print type(gpVariable)
					bads[gpVariable] = options

				constraints+=ShoppingCart(goods=goods,bads=bads)

	  cost = self.createSignomial(self.modelDict["cost"],varDict)

	  m = gpkitModel(cost, constraints)
	  so2 = feasibility_model(m.gp(),"max")
	  # try

	  try:
	  	  print 'presolve'
		  sol = m.solve(verbosity=3,solver="cvxopt")
		  print 'solved'
	  except (RuntimeError, TypeError, NameError, ValueError, RuntimeWarning),e:
	      print 'exception: ' + str(e)
	      sol="failedSolve"

	  # print('solution dict')
	  # print(sol.program.result["variables"])
	  jsSol = Solution()
	  jsSol.translateSol(sol,varDict)

	  output = MyEncoder().encode(jsSol)
	  # print output
	  return output
