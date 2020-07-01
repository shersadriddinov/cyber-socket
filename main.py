from sanic import Sanic
from sanic.response import json

app = Sanic("cyber_socket")


@app.route("/lobby")
async def test(request):
	return json({"hello": "World"})

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)
