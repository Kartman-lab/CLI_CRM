import sentry_sdk
from functools import wraps 
from dotenv import load_dotenv
import os

load_dotenv()

sentry_dsn = os.getenv("SENTRY_DSN")

sentry_sdk.init(
    dsn=sentry_dsn,
    send_default_pii=True
)

