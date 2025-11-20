import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")  # <-- tu archivo JSON
    firebase_admin.initialize_app(cred)

# Crear el cliente de Firestore
db = firestore.client()
