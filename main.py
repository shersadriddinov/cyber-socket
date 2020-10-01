from sanic import Sanic
from sanic.log import logger
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
	logger.info("New connection from " + request.ip)
	CONNECTIONS.append(connection)

	while running:
		in_data = await ws.recv()
		data = json.loads(in_data)
		action = data.get('action', False)
		uuid = data.get("uuid", False)
		# Connection routine
		logger.info(request.ip + "'s action is [" + action + "]")
		if action == 'connect':
			# TODO: write clear docs
			connection.uuid = uuid
			connection.status = "ONLINE"
			connection.party_status = True
			connection.party_id = uuid
			# TODO: notify every one in connection list that user is ONLINE
			# TODO: update player count
			for user in CONNECTIONS:
				if user.uuid == uuid:
					try:
						await user.ws.send(json.dumps({
								"action": "connect",
								"error": 0
						}))
						logger.info(request.ip + "'s [" + action + "] success")
					except:
						logger.error(request.ip + "'s [" + action + "] failed")
		# Notification routine
		elif action == 'notification':
			if data.get('type', 0) == 1:
				for user in CONNECTIONS:
					if user.uuid == uuid:
						try:
							await user.ws.send(json.dumps({
								"action": "notification"
							}))
							logger.info(request.ip + "'s [" + action + "] success")
						except:
							logger.error(request.ip + "'s [" + action + "] failed: cannot send")
		elif action == 'friend_request_confirm':
			friend = data.get("friend", False)
			for user in CONNECTIONS:
				if user.uuid == uuid:
					try:
						await user.ws.send(json.dumps({
							"action": "friend_confirmed",
							"uuid": uuid,
							"friend": friend
						}))
						logger.info("Friend Request Confirm sent from " + friend + " to " + uuid)
					except:
						logger.error(request.ip + "'s [" + action + "] failed: cannot send")
			else:
				logger.error("User with uuid=[" + uuid + "] is not online")
		elif action == 'new_server': # Check if uuid required
			for user in CONNECTIONS:
				try:
					await user.ws.send(json.dumps({
						"action": "new_server",
					}))
					logger.info(request.ip + "'s [" + action + "] success")
				except:
					logger.error(request.ip + "'s [" + action + "] failed: cannot send")
					pass
		elif action == 'invite':
			inviter = data.get("inviter")
			for user in CONNECTIONS:
				if user.uuid == uuid:
					try:
						await user.ws.send(json.dumps({
							"action": "invite",
							"inviter": inviter
						}))
						logger.info(request.ip + "'s [" + action + "] success")
					except:
						logger.error(request.ip + "'s [" + action + "] failed: cannot send")

	CONNECTIONS.remove(connection)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8003, protocol=WebSocketProtocol, debug=True, access_log=True)
