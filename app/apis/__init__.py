from sanic import Blueprint

from app.apis.example_blueprint import example
from app.apis.text_to_speech_blueprint import tts_bp

api = Blueprint.group(example, tts_bp)

