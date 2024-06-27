from sanic.response import text

from app import create_app
from app.apis import api
from config import Config, TTSConfig

app = create_app(Config, TTSConfig)
app.blueprint(api)


@app.route("/", methods={'GET', 'POST'})
async def hello_world(request):
    return text("Hello World")


@app.on_response
async def add_response_header(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = ("Accept, Content-Type, "
                                                        "Content-Length,"
                                                        "Accept-Encoding, X-CSRF-Token, "
                                                        "Authorization")

if __name__ == '__main__':
    app.run(**app.config['RUN_SETTING'])
