import os
import json

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SESSION_TYPE = os.getenv('SESSION_TYPE', 'filesystem')
    CREDENTIALS_FILE = 'credentials.json'
    SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME', 'Wedding RSVPs')
    GUEST_LIST_SHEET_NAME = os.getenv('GUEST_LIST_SHEET_NAME', 'Guest List: Complete')
    RSVP_SHEET_NAME = os.getenv('RSVP_SHEET_NAME', 'RSVPs')