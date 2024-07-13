import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    RUN_SETTING = {
        'host': os.environ.get('SERVER_HOST', 'localhost'),
        'port': int(os.environ.get('SERVER_PORT', 8000)),
        'debug': False,
        "access_log": True,
        "auto_reload": False,
        'workers': 0,
        'single_process': True,
    }


class MongoDBConfig:
    USERNAME = os.environ.get("MONGO_USERNAME") or "nhquan239"
    PASSWORD = os.environ.get("MONGO_PASSWORD") or "admin123"
    HOST = os.environ.get("MONGO_HOST") or "chat-echo.gowp8zb.mongodb.net/"
    PORT = os.environ.get("MONGO_PORT") or "27017"
    DATABASE = os.environ.get("MONGO_DATABASE") or "chat-echo"
    URI = os.environ.get("MONGO_URI") or f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
