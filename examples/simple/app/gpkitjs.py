# http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable

class Solution(object):
	""" A model of a component's power:

	"""
	def __init__(self):
		self.variables = {}
	def translateSol(self,sol,varDict):
		for variableKey in varDict:
			variable = varDict[variableKey]
			print(variable)
			self.variables[variableKey] = Variable(variable.key.descr["name"],sol(variable),variableKey)
		print(self.variables)
class Variable(object):
	def __init__(self,name,value,ID):
		self.name = name
		self.value = value
		self.ID = ID