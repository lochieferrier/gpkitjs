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
	def solve(self):

	  constraints = []
	  varDict = {}
	  for constraint in self.modelDict["constraints"]:
	  	# print type(constraint)
	  	print ('processing left hand side')
	  	leftSide = constraint["left"]
	  	expArr = leftSide["expArr"]
	  	
	  	# if type(constraint["left"]) == dict:
	  	# 	varProperties = constraint["left"]
	  	# 	# inputVarsDict[varProperties["ID"]] = varProperties
	  	# 	tempVar = gpkit.Variable(varProperties["name"])
	  	# 	constraint["left"] = tempVar
	  	# 	print(varProperties["ID"])
	  	# 	varDict[varProperties["ID"]] = tempVar
	  	# if constraint["oper"] == "geq":
	  	# 	constraints +=[constraint["left"] >= constraint["right"]]
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