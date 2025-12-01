class Results:

	file_name = ""
	bug_density = 0.0
	last_edit = ""

	def __init__(self, file, density, recent_commit_date):
		self.file_name = file
		self.bug_density = density
		self.last_edit = recent_commit_date

	def get_file(self):
		return str(self.fileName)
	
	def get_density(self):
		return str(self.bugDensity)
	
	def get_last_commit_date(self):
		return str(self.lastEdit)
