from dotenv import load_dotenv
import os

load_dotenv()


class GoogleOAuth:
    GOOGLE_CLIENT_ID = os.getenv('OAUTH_GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('OAUTH_GOOGLE_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('AWS_REGION')
    ALLOWED_EMAILS = ['joaojacomedev@gmail.com']