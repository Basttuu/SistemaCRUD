from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from database import db

app = FastAPI(title="API Maestro/Detalle")

# Mapeo para URLs
COLLECTIONS_MAP = {
    "clientes": "clients",
    "productos": "products",
    "facturas": "invoices"
}

# Campos que se mostrarán en MAESTRO (resumido)
MAESTRO_FIELDS = {
    "clientes": ["id", "name", "email"],
    "productos": ["id", "name", "price"],
    "facturas": ["id", "date", "client_id"]
}

# -------------------------------
# Función HTML para MAESTRO POR MÓDULO
# -------------------------------
def html_table_maestro(items, title, fields, collection):
    html = f"""
    <html>
    <head>
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            :root {{ --bg:#f3f6fb; --card:#ffffff; --accent:#556ee6; --muted:#6b7280; --accent-2:#8e44ad; }}
            body {{ font-family: 'Segoe UI', Roboto, Arial, sans-serif; background: linear-gradient(180deg,#eef2ff 0%,#f8fafc 100%); padding: 20px; color:#111827; }}
            .container {{ max-width:1100px; margin:20px auto; padding:20px; }}
            .topbar {{ display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:20px; }}
            .brand {{ display:flex; align-items:center; gap:12px; text-decoration:none; color:var(--accent); font-weight:700; }}
            .logo {{ width:44px; height:44px; background:var(--accent); border-radius:10px; display:inline-flex; align-items:center; justify-content:center; color:white; font-weight:700; box-shadow:0 6px 18px rgba(85,110,230,0.12); }}
            .btn {{ padding:10px 14px; border-radius:8px; text-decoration:none; font-weight:600; display:inline-block; }}
            .btn-primary {{ background:var(--accent); color:white; box-shadow:0 6px 18px rgba(85,110,230,0.12); }}
            .btn-ghost {{ background:transparent; color:var(--muted); border:1px solid rgba(0,0,0,0.06); }}
            .card {{ background:var(--card); border-radius:12px; padding:18px; box-shadow: 0 8px 24px rgba(15,23,42,0.06); }}
            h2 {{ margin:0 0 14px 0; color:#111827; }}
            table {{ width:100%; border-collapse:separate; border-spacing:0; border-radius:10px; overflow:hidden; }}
            thead th {{ text-align:left; padding:12px 16px; background:linear-gradient(90deg,var(--accent-2),var(--accent)); color:white; font-weight:700; }}
            tbody tr {{ border-bottom:1px solid #eef2ff; }}
            td {{ padding:12px 16px; background:transparent; color:#111827; }}
            tbody tr:hover td {{ background: #fbfdff; transform: translateY(-1px); }}
            .action-link {{ color:var(--accent); font-weight:700; text-decoration:none; }}
            .meta {{ color:var(--muted); font-size:13px; }}
            @media (max-width:720px) {{ thead {{ display:none; }} table, tbody, tr, td {{ display:block; width:100%; }} td {{ box-sizing:border-box; padding:12px; }} tr {{ margin-bottom:12px; }} td:before {{ content:attr(data-label); font-weight:700; display:block; color:var(--muted); margin-bottom:6px; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="topbar">
                <a class="brand" href="/api/maestro">
                    <span class="logo">M</span>
                    <span>API Maestro</span>
                </a>
                <div>
                    <a class="btn btn-primary" href="/api/maestro">Menú principal</a>
                </div>
            </div>

            <div class="card">
                <h2>{title}</h2>
                <div class="meta">Listado resumido de {collection.capitalize()}</div>
                <table>
                    <thead>
                        <tr>
    """
    for column in fields:
        html += f"<th>{column}</th>"
    html += "<th>Acción</th></tr></thead><tbody>"

    for item in items:
        html += "<tr>"
        for column in fields:
            html += f"<td data-label=\"{column}\">{item.get(column, '')}</td>"
        html += f"<td data-label=\"Acción\"><a class=\"action-link\" href='/api/detalle/{collection}/{item['id']}'>Ver detalle</a></td></tr>"

    html += "</tbody></table></div></div></body></html>"
    return HTMLResponse(html)

# -------------------------------
# Función HTML para DETALLE
# -------------------------------
def html_table_detalle(item, collection):
    html = f"""
    <html>
    <head>
        <title>Detalle - {collection}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            :root {{ --bg:#f3f6fb; --card:#ffffff; --accent:#556ee6; --muted:#6b7280; --accent-2:#8e44ad; }}
            body {{ font-family: 'Segoe UI', Roboto, Arial, sans-serif; background: linear-gradient(180deg,#eef2ff 0%,#f8fafc 100%); padding: 20px; color:#111827; }}
            .container {{ max-width:800px; margin:20px auto; padding:20px; }}
            .topbar {{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:20px; }}
            .brand {{ display:flex; align-items:center; gap:10px; text-decoration:none; color:var(--accent); font-weight:700; }}
            .logo {{ width:40px; height:40px; background:var(--accent); border-radius:8px; display:inline-flex; align-items:center; justify-content:center; color:white; font-weight:700; }}
            .btn {{ padding:10px 14px; border-radius:8px; text-decoration:none; font-weight:600; display:inline-block; }}
            .btn-primary {{ background:var(--accent); color:white; box-shadow:0 6px 18px rgba(85,110,230,0.12); }}
            .btn-secondary {{ background:var(--accent-2); color:white; margin-left:8px; }}
            .card {{ background:var(--card); border-radius:12px; padding:18px; box-shadow: 0 8px 24px rgba(15,23,42,0.06); }}
            table {{ width:100%; border-collapse:collapse; margin-top:12px; }}
            th {{ text-align:left; padding:10px 12px; width:35%; background:#fafafa; color:#111827; }}
            td {{ padding:10px 12px; border-top:1px solid #f1f5f9; }}
            .meta {{ color:var(--muted); font-size:13px; }}
            @media (max-width:720px) {{ th, td {{ display:block; width:100%; }}}}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="topbar">
                <a class="brand" href="/api/maestro">
                    <span class="logo">M</span>
                    <span>API Maestro</span>
                </a>
                <div>
                    <a class="btn btn-primary" href="/api/maestro">Menú principal</a>
                    <a class="btn btn-secondary" href="/api/maestro/{collection}">Volver a {collection.capitalize()}</a>
                </div>
            </div>

            <div class="card">
                <h2>Detalle - {collection.capitalize()}</h2>
                <div class="meta">ID: {item.get('id')}</div>
                <table>
    """

    for key, value in item.items():
        html += f"<tr><th>{key}</th><td>{value}</td></tr>"

    html += "</table></div></div></body></html>"

    return HTMLResponse(html)

# -------------------------------
# ENDPOINT MAESTRO POR MÓDULO
# -------------------------------
@app.get("/api/maestro/{collection}", response_class=HTMLResponse)
def maestro(collection: str):
    if collection not in COLLECTIONS_MAP:
        raise HTTPException(404, "Colección no encontrada")

    firebase_name = COLLECTIONS_MAP[collection]
    docs = db.collection(firebase_name).stream()

    items = [{"id": d.id, **d.to_dict()} for d in docs]

    # Mostrar solo campos del maestro
    fields = MAESTRO_FIELDS[collection]

    filtered_items = []
    for item in items:
        filtered_items.append({
            field: item.get(field, "")
            for field in fields
        })

    return html_table_maestro(
        filtered_items,
        f"Maestro - {collection.capitalize()}",
        fields,
        collection
    )

# -------------------------------
# ENDPOINT DETALLE POR MÓDULO
# -------------------------------
@app.get("/api/detalle/{collection}/{item_id}", response_class=HTMLResponse)
def detalle(collection: str, item_id: str):
    if collection not in COLLECTIONS_MAP:
        raise HTTPException(404, "Colección no encontrada")

    firebase_name = COLLECTIONS_MAP[collection]
    doc = db.collection(firebase_name).document(item_id).get()

    if not doc.exists:
        raise HTTPException(404, "Elemento no encontrado")

    item = {"id": doc.id, **doc.to_dict()}
    return html_table_detalle(item, collection)

# -------------------------------
# ENDPOINT MAESTRO GENERAL
# -------------------------------
@app.get("/api/maestro", response_class=HTMLResponse)
def maestro_general():
    html = f"""
    <html>
    <head>
        <title>Maestro General</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            :root {{ --bg:#f3f6fb; --card:#ffffff; --accent:#556ee6; --muted:#6b7280; }}
            body {{ font-family: 'Segoe UI', Roboto, Arial, sans-serif; background: linear-gradient(180deg,#eef2ff 0%,#f8fafc 100%); padding: 20px; color:#111827; }}
            .container {{ max-width:1100px; margin:20px auto; padding:20px; }}
            .topbar {{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:20px; }}
            .brand {{ display:flex; align-items:center; gap:10px; text-decoration:none; color:var(--accent); font-weight:700; }}
            .logo {{ width:44px; height:44px; background:var(--accent); border-radius:10px; display:inline-flex; align-items:center; justify-content:center; color:white; font-weight:700; }}
            .btn {{ padding:10px 14px; border-radius:8px; text-decoration:none; font-weight:600; display:inline-block; }}
            .btn-primary {{ background:var(--accent); color:white; box-shadow:0 6px 18px rgba(85,110,230,0.12); }}
            .section {{ margin-bottom:28px; }}
            table {{ width:100%; border-collapse:collapse; border-radius:8px; overflow:hidden; box-shadow:0 8px 24px rgba(15,23,42,0.04); }}
            th {{ text-align:left; padding:10px 12px; background:#ffffff; color:#374151; border-bottom:1px solid #eef2ff; }}
            td {{ padding:10px 12px; border-bottom:1px solid #f1f5f9; }}
            .muted {{ color:var(--muted); font-size:13px; }}
            @media (max-width:720px) {{ table, thead, tbody, th, td, tr {{ display:block; }} tr {{ margin-bottom:12px; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="topbar">
                <a class="brand" href="/api/maestro">
                    <span class="logo">M</span>
                    <span>API Maestro</span>
                </a>
                <div>
                    <a class="btn btn-primary" href="/api/maestro">Menú principal</a>
                </div>
            </div>
            <h1 style="margin:0 0 18px 0;">Maestro General</h1>
    """

    for collection, firebase_name in COLLECTIONS_MAP.items():
        html += f"<div class='section'><h2>{collection.capitalize()}</h2>"

        html += """
        <table>
            <tr>
                <th>Colección</th>
                <th>ID</th>
                <th>Campo 1</th>
                <th>Campo 2</th>
                <th>Acción</th>
            </tr>
        """

        docs = db.collection(firebase_name).stream()
        fields = MAESTRO_FIELDS[collection][1:3]

        for d in docs:
            data = d.to_dict()
            campo1 = data.get(fields[0], "")

            # Para 'facturas' mostramos el total en el Campo 2.
            if collection == "facturas":
                # Preferimos un campo 'total' si existe, si no intentamos calcularlo desde items/line_items
                total = data.get("total")
                if total is None:
                    total = 0.0
                    items = data.get("items") or data.get("line_items") or []
                    # Si items viene como dict (ej. {id: item}), tomar los valores
                    if isinstance(items, dict):
                        items = items.values()
                    for it in items:
                        if not isinstance(it, dict):
                            continue
                        # distintos nombres posibles para precio/cantidad
                        amount = it.get("amount") or it.get("total")
                        if amount is not None:
                            try:
                                total += float(amount)
                                continue
                            except Exception:
                                pass
                        price = it.get("price") or it.get("unit_price") or it.get("precio") or 0
                        qty = it.get("quantity") or it.get("qty") or 1
                        try:
                            total += float(price) * float(qty)
                        except Exception:
                            pass
                # Formatear con 2 decimales
                try:
                    campo2 = f"{float(total):.2f}"
                except Exception:
                    campo2 = str(total)
            else:
                campo2 = data.get(fields[1], "")

            html += f"""
            <tr>
                <td>{collection}</td>
                <td>{d.id}</td>
                <td>{campo1}</td>
                <td>{campo2}</td>
                <td><a href='/api/detalle/{collection}/{d.id}'>Ver detalle</a></td>
            </tr>
            """

        html += "</table></div>"

    html += "</body></html>"
    return HTMLResponse(html)

import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
