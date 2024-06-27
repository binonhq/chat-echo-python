import time


class User:
    def __init__(self, _id='', first_name='', last_name='', email='', password=''):
        self._id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = int(time.time())
        self.updated_at = int(time.time())

    def to_dict(self):
        return {
            '_id': str(self._id),
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'password': self.password,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }

    def from_dict(self, json_dict: dict):
        self._id = json_dict.get('_id', self._id)
        self.first_name = json_dict.get('firstName', '')
        self.last_name = json_dict.get('lastName', '')
        self.email = json_dict.get('email', '')
        self.password = json_dict.get('password', '')
        self.created_at = json_dict.get('createdAt', int(time.time()))
        self.updated_at = json_dict.get('updatedAt', int(time.time()))
        return self
