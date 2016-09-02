# http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
import gpkit
from json import JSONEncoder
import json

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__ 

class Solution(object):
	""" A model of a component's power:

	"""
	def __init__(self):
		self.variables = {}
	def translateSol(self,sol,varDict):
		for variableKey in varDict:
			variable = varDict[variableKey]
			# print(variable)
			self.variables[variableKey] = Variable(variable.key.descr["name"],sol(variable),variableKey)
		# print(self.variables)
class Variable(object):
	def __init__(self,name,value,ID):
		self.name = name
		self.value = value
		self.ID = ID

class Solver(object):
	def __init__(self):
		self.modelDict = {}
	def initFromRequest(self,request):
		  r= request.form
		  for line in r:
		  	resultString = str(line);
		  self.modelDict = json.loads(resultString)
	def createSignomial(self,JSsignomial,varDict):


	  	# expArr = leftSide["expArr"]
	  	if not JSsignomial["isSignomial"]:
	  		# print leftSide["monomialsArr"]
	  		expDictList = []
	  		constantsList = []
	  		# print 'printing js signomial'
	  		# print JSsignomial
	  		for monomial in JSsignomial["monomialsArr"]:
	  			expDict = {}
	  			# print monomial["expArr"]
	  			constant = 1
	  			for variableArr in monomial["expArr"]:
	  				# print variableArr

	  				jsVar = variableArr[0]
	  				# print 'printing jsvar'
	  				# print jsVar

	  				# print(type(jsVar))
	  				if "name" in jsVar:
	  					# This means we got 
	  					tempVar = gpkit.Variable(jsVar["name"])
	  					if "units" in jsVar:
		  					tempVar.units = jsVar["units"]
		  				if "val" in jsVar:
		  					tempVar = gpkit.Variable(str(tempVar.exps[0].keys()[0]),jsVar["val"],jsVar["units"])

		  				if "label" in jsVar:
		  					tempVar.label = jsVar["label"]
		  				# print tempVar
		  				# We have all these variables coming in, but need to track which is which, this was the point
		  				# of the ID assignment
		  				# We store variables in a dictionary under JS ID
		  				if "ID" in jsVar:
			  				if jsVar["ID"] not in varDict:
			  					varDict[jsVar["ID"]] = tempVar
			  				else:
			  					tempVar = varDict[jsVar["ID"]]
			  				expDict[tempVar] = variableArr[1]  
	  				else:
	  					# If there isn't a name, it musn't be a variable, but instead
	  					# a raw number
	  					# print jsVar
	  					constant*=jsVar

	  				
	  			expDictList += [expDict]
	  			constantsList += [constant]
	  			# print(constantsList)
	  		# print tuple(expDictList)
	  		# print tuple(constantsList)
	  		return gpkit.Signomial(tuple(expDictList),tuple(constantsList))

	  			# print expDict
	def solve(self):

	  constraints = []
	  varDict = {}
	  
	  for constraint in self.modelDict["constraints"]:
	  	left = self.createSignomial(constraint['left'],varDict)
	  	# print varDict
	  	right = self.createSignomial(constraint['right'],varDict)
	  	# print varDict
	  	if constraint['oper'] == "leq":
	  		constraints+=[left<=right]
	  	if constraint['oper'] == "geq":
	  		constraints+=[left>=right]

	  print constraints
	  print "model dict"
	  print self.modelDict["cost"]
	  # print self.createSignomial(self.modelDict["cost"],varDict)

	  costDict = self.modelDict["cost"]
	  cost = varDict[costDict["ID"]]
	  # costVar = Variable(cost["name"])
	  # constraint["left"] = tempVar
	  print('final inputs to normal model')
	  x = gpkit.Variable('x')
	  constraintsNormal = []
	  constraintsNormal += [x>=1]
	  objectiveNormal = x
	  print(objectiveNormal)
	  print(constraintsNormal)

	  mNormal = gpkit.Model(objectiveNormal,constraintsNormal)
	 
	  print('final inputs to JS model')
	  print(cost)
	  print(constraints)
	  m = gpkit.Model(cost,constraints)
	  sol = m.solve(verbosity=1)
	  print('solution dict')
	  print(sol.program.result["variables"])
	  jsSol = Solution()
	  jsSol.translateSol(sol,varDict)
	  output = MyEncoder().encode(jsSol)
	  return output