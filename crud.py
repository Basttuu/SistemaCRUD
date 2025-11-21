from database import db
from google.cloud.firestore import DocumentReference

# --------------------------
# CLIENTES
# --------------------------
def crear_cliente(data: dict):
    ref = db.collection("clients").add(data)
    return ref

def obtener_clientes():
    docs = db.collection("clients").stream()
    return [{ "id": d.id, **d.to_dict() } for d in docs]

def obtener_cliente(id: str):
    doc = db.collection("clients").document(id).get()
    if doc.exists:
        return { "id": doc.id, **doc.to_dict() }
    return None


# --------------------------
# PRODUCTOS
# --------------------------
def crear_producto(data: dict):
    ref = db.collection("products").add(data)
    return ref

def obtener_productos():
    docs = db.collection("products").stream()
    return [{ "id": d.id, **d.to_dict() } for d in docs]

def obtener_producto(id: str):
    doc = db.collection("products").document(id).get()
    if doc.exists:
        return { "id": doc.id, **doc.to_dict() }
    return None


# --------------------------
# FACTURAS
# --------------------------
def crear_factura(data: dict):
    ref = db.collection("invoices").add(data)
    return ref

def obtener_facturas():
    docs = db.collection("invoices").stream()
    return [{ "id": d.id, **d.to_dict() } for d in docs]

def obtener_factura(id: str):
    doc = db.collection("invoices").document(id).get()
    if doc.exists:
        return { "id": doc.id, **doc.to_dict() }
    return None
