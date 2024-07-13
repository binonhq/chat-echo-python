from sanic import Blueprint

from app.apis.text_to_speech_blueprint import tts_bp

api = Blueprint.group(tts_bp)

