class Connection:
	ws = None
	uuid = ""
	party_id = ""
	friends = []
	status = "OFFLINE"
	party_status = False

	def __init__(self, ws, uuid="", party_id="", friends=[], status="OFFLINE", party_status=False):
		self.ws = ws
		self.uuid = uuid
		self.party_id = party_id
		self.friends = friends
		self.status = status
		self.party_status = party_status

	def __hash__(self):
		return hash((self.ws,))

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()
