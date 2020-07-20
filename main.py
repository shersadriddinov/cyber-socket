from sanic import Sanic
from sanic.websocket import WebSocketProtocol
import ujson as json

from config import default_settings
from connection import Connection


app = Sanic("cyber_socket")
app.config.from_object(default_settings)

CONNECTIONS = []


@app.websocket('/lobby')
async def connect(request, ws):
	running = True
	connection = Connection(ws=ws)
	CONNECTIONS.append(connection)

	while running:
		in_data = await ws.recv()
		data = json.loads(in_data)
		action = data.get('action', False)
		# Connection routine
		if action == 'connect':
			# TODO: write clear docs
			connection.uuid = data.get("uuid")
			connection.status = "ONLINE"
			connection.party_status = True
			connection.party_id = data.get("uuid")
			# TODO: notify every one in connection list that user is ONLINE
			# TODO: update player count

		# Notification routine
		if action == 'notification':
			print('hello')
			if data.get('type', 0) == 1:
				for user in CONNECTIONS:
					if user.uuid == data.get("uuid", False):
						try:
							await user.ws.send(json.dumps({
								"action": "notification"
							}))
						except:
							pass
		if action == 'friend_request_confirm':
			for user in CONNECTIONS:
				if user.uuid == data.get("uuid", False):
					try:
						await user.ws.send(json.dumps({
							"action": "friend_confirmed",
							"uuid": data.get("uuid"),
							"friend": data.get("friend")
						}))
					except:
						pass

	CONNECTIONS.remove(connection)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8003, protocol=WebSocketProtocol)
