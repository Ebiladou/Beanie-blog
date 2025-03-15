import os
from dotenv import load_dotenv

load_dotenv()

cloud_name = os.environ.get("CLOUD_NAME")
cloud_api_key = os.environ.get("CLOUD_API_KEY")
cloud_api_secret = os.environ.get("CLOUD_API_SECRET")
cloudinary_url = os.environ.get("CLOUDINARY_URL")