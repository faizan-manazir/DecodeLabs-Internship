import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "development-only-change-me"
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    MAX_TEXT_LENGTH = 200_000
    JSON_SORT_KEYS = False
