import os
import json
from firebase_admin import credentials, firestore, initialize_app

# Cargar FIREBASE_KEY desde variable de entorno en Railway
firebase_key = os.getenv("FIREBASE_KEY")

cred_info = json.loads(firebase_key)
cred = credentials.Certificate(cred_info)
initialize_app(cred)

db = firestore.client()
