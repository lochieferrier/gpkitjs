# http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
import gpkit
from json import JSONEncoder
import json
import numpy as np

# Parse a Solution object into JSON, filtering for fixed or free variables
class MyEncoder(JSONEncoder):
    def default(self, o):
    	
    	cleanVarResults = {}
    	for varKey in o.variables:
    		# print type(o.variables[varKey].value)
    		if type(o.variables[varKey].value) != np.float64:
    			# print float(o.variables[varKey].value._magnitude)
    			cleanVarResults[varKey] = float(o.variables[varKey].value._magnitude)
    		else:
    			# print(float(o.variables[varKey].value))
    			cleanVarResults[varKey] = float(o.variables[varKey].value)
    		# print varDict[varKey].__dict__
    	return json.dumps({'variables':cleanVarResults})
        

class Solution(object):

	def __init__(self):
		self.variables = {}
		self.varDict = {}
	def translateSol(self,sol,varDict):
		for variableKey in varDict:
			variable = varDict[variableKey]
			# print(variable)
			self.variables[variableKey] = Variable(variable.key.descr["name"],sol(variable),variableKey)
		self.varDict = varDict
		# print(self.variables)
class Variable(object):
	def __init__(self,name,value,ID):
		self.name = name
		self.value = value
		self.ID = ID
def parseJSVar(jsVar, varDict):

	if type(jsVar) == dict:
		if "name" in jsVar:
			# This means we got 
			tempVar = gpkit.Variable(jsVar["name"])
			if "units" in jsVar:
				tempVar.units = jsVar["units"]
			if "val" in jsVar:
				tempVar = gpkit.Variable(str(tempVar.exps[0].keys()[0]),jsVar["val"],jsVar["units"])

			if "label" in jsVar:
				tempVar.label = jsVar["label"]
			# We have all these variables coming in, but need to track which is which, this was the point
			# of the ID assignment
			# We store variables in a dictionary under JS ID
			if "ID" in jsVar:
				if jsVar["ID"] not in varDict:
					varDict[jsVar["ID"]] = tempVar
				else:
					tempVar = varDict[jsVar["ID"]]
				return tempVar

class Solver(object):
	def __init__(self):
		self.modelDict = {}
	def initFromRequest(self,request):
		  r= request.form
		  for line in r:
		  	resultString = str(line);
		  self.modelDict = json.loads(resultString)
	def createSignomial(self,JSsignomial,varDict):

	  	if not JSsignomial["isSignomial"]:

	  		expDictList = []
	  		constantsList = []

	  		for monomial in JSsignomial["monomialsArr"]:
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

	  		return gpkit.Signomial(tuple(expDictList),tuple(constantsList))

	def solve(self):

	  constraints = []
	  varDict = {}
	  
	  for constraint in self.modelDict["constraints"]:
	  	left = self.createSignomial(constraint['left'],varDict)
	  	right = self.createSignomial(constraint['right'],varDict)
	  	if constraint['oper'] == "leq":
	  		constraints+=[left<=right]
	  	if constraint['oper'] == "geq":
	  		constraints+=[left>=right]
	  # for equality in self.modelDict["equalities"]:
	  # 	# print equality["left"]
	  # 	left = self.createSignomial(equality['left'],varDict)
	  # 	# print varDict
	  # 	right = self.createSignomial(equality['right'],varDict)
	  # 	# print varDict
	  # 	left = right
	  # print constraints
	  # print self.modelDict["cost"]
	  cost = self.createSignomial(self.modelDict["cost"],varDict)
	  # print cost
	  # print('final inputs to JS model')
	  
	  # print(constraints)

	  m = gpkit.Model(cost,constraints)
	  sol = m.solve(verbosity=1)
	  # print('solution dict')
	  # print(sol.program.result["variables"])
	  jsSol = Solution()
	  jsSol.translateSol(sol,varDict)

	  output = MyEncoder().encode(jsSol)
	  # print output
	  return output