class Results:

	fileName = ""
	bugDensity = 0.0
	lastEdit = ""

	def __init__(self, file, density, recentCommitDate):
		self.fileName = file
		self.bugDensity = density
		self.lastEdit = recentCommitDate

	def getFile(self):
		return str(self.fileName)
	
	def getDensity(self):
		return str(self.bugDensity)
	
	def getLastCommitDate(self):
		return str(self.lastEdit)
