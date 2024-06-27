from pymongo import MongoClient
import gridfs
from app.constants.mongodb_constants import MongoCollections
from app.utils.logger_utils import get_logger
from app.models.message import Message
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None):
        if connection_url is None:
            connection_url = MongoDBConfig.URI
        self.connection_url = connection_url.split('@')[-1]
        self.client = MongoClient(connection_url, tls=True, tlsAllowInvalidCertificates=True)
        logger.info('MongoDB connected')
        self.db = self.client[MongoDBConfig.DATABASE]
        self.message_col = self.db[MongoCollections.messages]
        self.user_col = self.db[MongoCollections.users]
        self.voice_setting = gridfs.GridFS(self.db, collection=MongoCollections.voice_settings)
        self.voice_generated = gridfs.GridFS(self.db, collection=MongoCollections.voice_generated)

    def get_messages(self, filter_=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self.message_col.find(filter_)
            data = []
            for doc in cursor:
                data.append(Message().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []

    def get_message_by_id(self, message_id):
        try:
            filter_ = {'_id': message_id}
            cursor = self.message_col.find(filter_)
            data = []
            for doc in cursor:
                data.append(Message().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []

