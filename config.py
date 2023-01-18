import os
from dotenv import load_dotenv

load_dotenv()


TG_TOKEN = os.getenv('TELEGRAM_TOKEN', None)
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', None)
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY', None)

TEST_BINANCE_API_KEY = os.getenv('TEST_BINANCE_API_KEY', None)
TEST_BINANCE_SECRET_KEY = os.getenv('TEST_BINANCE_SECRET_KEY', None)

