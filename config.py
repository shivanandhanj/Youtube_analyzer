from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv('API_KEY')