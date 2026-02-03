from datetime import datetime

class Note:
	def __init__(self, code, text) -> None:
		self.code = code
		self.text = text
		self.timestamp = datetime.now().timestamp()

	# Updates itself with inputted parameters
	def update(self, new_text):
		self.text = new_text
		
		# Renew the time the note was updated to current time
		self.timestamp = datetime.now().timestamp()

	def __str__(self) -> str:
		return "Note(%i, %s)" % (self.code, self.text)

	def __eq__(self, other) -> bool:
		return isinstance(other, Note) and self.code == other.code \
		and self.text == other.text
