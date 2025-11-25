class Results:

	fileName = ""
	bugDensity = 0.0

	def __init__(self, file, density):
		self.fileName = file
		self.bugDensity = density

	def getFile(self):
		return str(self.fileName)
	
	def getDensity(self):
		return str(self.bugDensity)
