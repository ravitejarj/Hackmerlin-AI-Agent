import os
from dotenv import load_dotenv

load_dotenv()

SESSION = os.getenv("SESSION")
CF_CLEARANCE = os.getenv("CF_CLEARANCE")

COOKIES = {}
if SESSION:
    COOKIES["SESSION"] = SESSION
if CF_CLEARANCE:
    COOKIES["cf_clearance"] = CF_CLEARANCE
