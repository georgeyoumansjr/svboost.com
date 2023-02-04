import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv

ROOT = '/home/tnhlabsc/svboost.com'

os.environ['OPENBLAS_NUM_THREADS'] = '1'

dotenv_path = join(ROOT+'/.env')
load_dotenv(dotenv_path)

PATH_TO_CHROMEDRIVER = os.getenv('PATH_TO_CHROMEDRIVER')

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

SECRET_KEY = os.getenv('YOUTUBE_API_KEY')
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
STRIP_API_KEY = os.getenv("STRIP_API_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
TAG_SEARCH_PRICE_ID = os.getenv("TAG_SEARCH_PRICE_ID")
USER_ADMIN = os.getenv("USER_ADMIN")
PASSWORD_ADMIN = os.getenv("PASSWORD_ADMIN")
ENVIRONMENT = os.getenv("ENVIRONMENT")
USERNAMEDB = os.getenv("USERNAMEDB")
PASSWORDDB = os.getenv("PASSWORDDB")
SERVERDB = os.getenv("SERVERDB")
NAMEDB = os.getenv("NAMEDB")

