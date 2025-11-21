from pydantic import BaseModel
from typing import Optional

# --------------------------
# MODELOS PARA CLIENTES
# --------------------------
class Cliente(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


# --------------------------
# MODELOS PARA PRODUCTOS
# --------------------------
class Producto(BaseModel):
    name: str
    price: float
    stock: Optional[int] = 0


# --------------------------
# MODELOS PARA FACTURAS
# --------------------------
class Factura(BaseModel):
    client_id: str
    date: str
    total: float
    items: Optional[list] = []
