import os
import json

class Settings:
	def __init__(self, file='settings.json'):
		# First, perform a check whether the file does exist
		if not os.path.isfile(file):
			print("[ERROR] Settings file {} not found".format(file))

		with open(file, 'r') as file:
			content = file.read()
		self.settings = json.loads(content)

	def get_input_device(self, name):
		return int(self.settings["input"][name].split("-")[0])

	def get_input_button(self, name):
		return int(self.settings["input"][name].split("-")[1])
	def get_gameplay_var(self, name):
		return self.settings["gameplay"][name]