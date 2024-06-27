import time


class Channel:
    def __init__(self, _id='', user_ids=None, type='direct', seen_by=None, name=''):
        if user_ids is None:
            user_ids = []
        if seen_by is None:
            seen_by = []
        self._id = _id
        self.user_ids = user_ids
        self.type = type
        self.seen_by = seen_by
        self.name = name
        self.created_at = int(time.time())
        self.updated_at = int(time.time())

    def to_dict(self):
        return {
            '_id': self._id,
            'userIds': self.user_ids,
            'type': self.type,
            'seenBy': self.seen_by,
            'name': self.name,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }

    def from_dict(self, json_dict: dict):
        self._id = json_dict.get('_id', self._id)
        self.user_ids = json_dict.get('userIds', [])
        self.type = json_dict.get('type', 'direct')
        self.seen_by = json_dict.get('seenBy', [])
        self.name = json_dict.get('name', '')
        self.created_at = json_dict.get('createdAt', int(time.time()))
        self.updated_at = json_dict.get('updatedAt', int(time.time()))
        return self