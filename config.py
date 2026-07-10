import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# CSV File
CSV_FILE = "products.csv"

# Number of products to show
MAX_RESULTS = 5

# Bot Name
BOT_NAME = "UrbanAce Shopping Assistant"
