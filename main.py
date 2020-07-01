from sanic import Sanic
from sanic.websocket import WebSocketProtocol

app = Sanic("cyber_socket")


@app.websocket('/lobby')
async def feed(request, ws):
	while True:
		data = 'hello!'
		print('Sending: ' + data)
		await ws.send(data)
		data = await ws.recv()
		print('Received: ' + data)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)
