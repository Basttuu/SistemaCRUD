import os
import json
from firebase_admin import credentials, firestore, initialize_app

firebase_key = os.getenv("FIREBASE_KEY")

if firebase_key:
    # Railway
    cred_info = json.loads(firebase_key)
    cred = credentials.Certificate(cred_info)
else:
    # Local
    cred = credentials.Certificate("firebase-key.json")

initialize_app(cred)
db = firestore.client()
