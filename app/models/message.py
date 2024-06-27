import time


class Message:
    def __init__(self, _id='', sender_id='', channel_id='', content='', sticker_id=''):
        self._id = _id
        self.sender_id = sender_id
        self.channel_id = channel_id
        self.content = content
        self.sticker_id = sticker_id
        self.created_at = int(time.time())
        self.updated_at = int(time.time())

    def to_dict(self):
        return {
            '_id': self._id,
            'senderId': self.sender_id,
            'channelId': self.channel_id,
            'content': self.content,
            'stickerId': self.sticker_id,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }

    def from_dict(self, json_dict: dict):
        self._id = json_dict.get('_id', self._id)
        self.sender_id = json_dict.get('senderId', '')
        self.channel_id = json_dict.get('channelId', '')
        self.content = json_dict.get('content', '')
        self.sticker_id = json_dict.get('stickerId', '')
        self.created_at = json_dict.get('createdAt', int(time.time()))
        self.updated_at = json_dict.get('updatedAt', int(time.time()))
        return self
