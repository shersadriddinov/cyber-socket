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
		action = data.get('action')
		# Connection routine
		if action == 'connect':
			stat = connection.status
			await connection.ws.send(json.dumps({"OK": 200, "object": stat}))

		if CONNECTIONS:
			CONNECTIONS.remove(connection)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)
