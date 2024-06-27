import time


class VoiceGenerated:
    def __init__(self, _id, message_id, audio):
        self._id = _id
        self.message_id = message_id
        self.audio = audio
        self.created_at = int(time.time())

    def to_dict(self):
        return {
            '_id': self._id,
            'messageId': self.message_id,
            'audio': self.audio,
            'createdAt': self.created_at
        }

    def from_dict(self, json_dict: dict):
        self._id = json_dict.get('_id', self._id)
        self.message_id = json_dict.get('messageId', '')
        self.audio = json_dict.get('audio', '')
        self.created_at = json_dict.get('createdAt', int(time.time()))
        return self
