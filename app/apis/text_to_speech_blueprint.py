import tempfile
import os
from sanic import Blueprint
from sanic import response
from app.database.mongodb import MongoDB
from bson.objectid import ObjectId
from app.service.tts import TTSService

tts_bp = Blueprint('text-to-speech_blueprint', url_prefix='/text-to-speech')

_db = MongoDB()
_tts = TTSService()


@tts_bp.route('/play-message', methods={'GET'})
async def play_voice_message(request):
    message_id = request.args.get('messageId')
    if not message_id:
        return response.json({'error': 'Missing data'}, status=400)

    message = _db.message_col.find_one({'_id': ObjectId(message_id)})

    if not message:
        return response.json({'error': 'Message not found'}, status=404)

    sender_id = message.get('senderId')

    if not sender_id:
        return {'error': 'Sender ID not found in message'}, 404

    # Find the user document by the senderId
    user = _db.user_col.find_one({'_id': ObjectId(sender_id)})

    if not user:
        return {'error': 'User not found'}, 404

    voice_setting_id = user.get('voiceSettingId')

    if not voice_setting_id:
        return {
            'error': 'Voice setting ID not found',
            'status': 'NOT_HAVE_VOICE_SETTING'
        }, 404

    voice_setting = _db.voice_setting.get(ObjectId(voice_setting_id))

    if not voice_setting:
        return {
            'error': 'Voice setting not found',
            'status': 'NOT_HAVE_VOICE_SETTING'
        }, 404

    exist_voice = _db.voice_generated.find_one({
        'voice_id': message_id + "_" + voice_setting_id
    })
    if exist_voice:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(exist_voice.read())
            temp_file_path = temp_file.name

        try:
            return await response.file(temp_file_path, mime_type="audio/wav")
        finally:
            os.remove(temp_file_path)

    output_file = await _tts.get_own_voice_audio(message.get('content'),
                                                 voice_setting.read())
    if not output_file:
        return response.json({'error': 'Error processing the request'}, status=500)

    _db.voice_generated.put(data=output_file.getvalue(), filename=f"{message_id}.wav", user_id=sender_id,
                            voice_id=str(message_id) + "_" + str(voice_setting_id))

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(output_file.getvalue())
        temp_file_path = temp_file.name

    try:
        return await response.file(temp_file_path, mime_type="audio/wav")
    finally:
        os.remove(temp_file_path)


@tts_bp.route('/play_voice_setting', methods={'GET'})
async def play_void_setting(request):
    voice_setting_id = request.args.get('voice_setting_id')
    if not voice_setting_id:
        return response.json({'error': 'Missing data'}, status=400)

    voice_setting = _db.voice_setting.get(ObjectId(voice_setting_id))

    if not voice_setting:
        return response.json({'error': 'Voice setting not found'}, status=404)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(voice_setting.read())
        temp_file_path = temp_file.name

    try:
        return await response.file(temp_file_path, mime_type="audio/wav")
    finally:
        os.remove(temp_file_path)

# @tts_bp.route('/play-message-v2', methods={'GET'})
# async def play_voice_message_v2(request):
#     message_id = request.args.get('messageId')
#     if not message_id:
#         return response.json({'error': 'Missing data'}, status=400)
#
#     message = _db.message_col.find_one({'_id': ObjectId(message_id)})
#
#     if not message:
#         return response.json({'error': 'Message not found'}, status=404)
#
#     sender_id = message.get('senderId')
#
#     if not sender_id:
#         return {'error': 'Sender ID not found in message'}, 404
#
#     # Find the user document by the senderId
#     user = _db.user_col.find_one({'_id': ObjectId(sender_id)})
#
#     if not user:
#         return {'error': 'User not found'}, 404
#
#     voice_setting_id = user.get('voiceSettingId')
#
#     if not voice_setting_id:
#         return {
#             'error': 'Voice setting ID not found',
#             'status': 'NOT_HAVE_VOICE_SETTING'
#         }, 404
#
#     voice_setting = _db.voice_setting.get(ObjectId(voice_setting_id))
#
#     if not voice_setting:
#         return {
#             'error': 'Voice setting not found',
#             'status': 'NOT_HAVE_VOICE_SETTING'
#         }, 404
#
#     output_file = await _tts.get_own_voice_audio_v2(message.get('content'), 'en',
#                                                     voice_setting.read())
#     if not output_file:
#         return response.json({'error': 'Error processing the request'}, status=500)
#
#     _db.voice_generated.put(data=output_file.getvalue(), filename=f"{message_id}.wav", user_id=sender_id,
#                             voice_id=str(message_id) + "_" + str(voice_setting_id))
#
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
#         temp_file.write(output_file.getvalue())
#         temp_file_path = temp_file.name
#
#     try:
#         return await response.file(temp_file_path, mime_type="audio/wav")
#     finally:
#         os.remove(temp_file_path)
