import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN") or "random_token"
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
    RANGE_NAME = os.environ.get("RANGE_NAME")
