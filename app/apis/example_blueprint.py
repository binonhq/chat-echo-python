from sanic import Blueprint
from sanic import response

from app.database.mongodb import MongoDB
from app.utils.parse_json import parse_json

example = Blueprint('example_blueprint', url_prefix='/example')
_db = MongoDB()


@example.route('/')
async def bp_root(request):
    return response.json({'example': 'blueprint'})


@example.route('/test')
async def bp_test(request):
    listMessage = _db.get_messages()
    mes = [message.to_dict() for message in listMessage]
    return response.json(parse_json(mes))


