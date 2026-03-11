"""
app.py - Servidor Flask que sirve los datos de grados y ciclos por isla desde SQLite.

Uso:
    python app.py

Endpoints:
    GET /api/islas                           -> Lista de islas
    GET /api/estudios?isla=<nombre>          -> Estudios agrupados por tipo para una isla
    GET /api/estudios?isla=<nombre>&cat=<id> -> Estudios filtrados por isla y categoria vocacional
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('test-vocacional.html')

DB_DIR = os.environ.get("DB_DIR", os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DB_DIR, "vocacional.db")


def get_db():
    """Abre una conexion a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/api/islas", methods=["GET"])
def get_islas():
    """Devuelve la lista de todas las islas."""
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM islas ORDER BY id")
        islas = [{"id": row["id"], "nombre": row["nombre"]} for row in cur.fetchall()]
        return jsonify(islas)
    finally:
        conn.close()


@app.route("/api/estudios", methods=["GET"])
def get_estudios():
    """
    Devuelve estudios filtrados por isla y opcionalmente por categoria vocacional.
    Los resultados se agrupan por tipo de estudio.

    Query params:
        isla (str, requerido): Nombre de la isla
        cat  (str, opcional):  ID de la categoria vocacional (ej: 'sanitario', 'tecnologico')
    """
    isla_nombre = request.args.get("isla")
    categoria = request.args.get("cat")

    if not isla_nombre:
        return jsonify({"error": "El parametro 'isla' es requerido"}), 400

    conn = get_db()
    try:
        cur = conn.cursor()

        # Verificar que la isla existe
        cur.execute("SELECT id FROM islas WHERE LOWER(nombre) = LOWER(?)", (isla_nombre,))
        isla_row = cur.fetchone()
        if not isla_row:
            return jsonify({"error": f"Isla '{isla_nombre}' no encontrada"}), 404

        isla_id = isla_row["id"]

        # Construir query
        if categoria:
            cur.execute("""
                SELECT e.nombre AS estudio, t.nombre AS tipo, e.categoria
                FROM estudios e
                JOIN tipos_estudio t ON e.tipo_id = t.id
                WHERE e.isla_id = ? AND LOWER(e.categoria) = LOWER(?)
                ORDER BY t.id, e.nombre
            """, (isla_id, categoria))
        else:
            cur.execute("""
                SELECT e.nombre AS estudio, t.nombre AS tipo, e.categoria
                FROM estudios e
                JOIN tipos_estudio t ON e.tipo_id = t.id
                WHERE e.isla_id = ?
                ORDER BY t.id, e.nombre
            """, (isla_id,))

        rows = cur.fetchall()

        # Agrupar por tipo de estudio
        grouped = {}
        for row in rows:
            tipo = row["tipo"]
            if tipo not in grouped:
                grouped[tipo] = []
            grouped[tipo].append({
                "nombre": row["estudio"],
                "categoria": row["categoria"]
            })

        return jsonify({
            "isla": isla_nombre,
            "categoria": categoria,
            "total": len(rows),
            "estudios_por_tipo": grouped
        })
    finally:
        conn.close()


@app.route("/api/estudios/recomendados", methods=["GET"])
def get_recomendados():
    """
    Devuelve estudios recomendados para una isla basandose en multiples categorias.
    Se usa en la pantalla de resultados para cruzar las top categorias del usuario
    con la oferta disponible en su isla.

    Query params:
        isla (str, requerido): Nombre de la isla
        cats (str, requerido): Categorias separadas por coma (ej: 'sanitario,tecnologico,economico')
    """
    isla_nombre = request.args.get("isla")
    cats_param = request.args.get("cats", "")

    if not isla_nombre:
        return jsonify({"error": "El parametro 'isla' es requerido"}), 400
    if not cats_param:
        return jsonify({"error": "El parametro 'cats' es requerido"}), 400

    categorias = [c.strip().lower() for c in cats_param.split(",") if c.strip()]

    conn = get_db()
    try:
        cur = conn.cursor()

        # Verificar isla
        cur.execute("SELECT id FROM islas WHERE LOWER(nombre) = LOWER(?)", (isla_nombre,))
        isla_row = cur.fetchone()
        if not isla_row:
            return jsonify({"error": f"Isla '{isla_nombre}' no encontrada"}), 404

        isla_id = isla_row["id"]

        # Buscar estudios que coincidan con cualquiera de las categorias
        placeholders = ",".join(["?" for _ in categorias])
        cur.execute(f"""
            SELECT e.nombre AS estudio, t.nombre AS tipo, e.categoria
            FROM estudios e
            JOIN tipos_estudio t ON e.tipo_id = t.id
            WHERE e.isla_id = ? AND LOWER(e.categoria) IN ({placeholders})
            ORDER BY
                CASE LOWER(e.categoria)
                    {" ".join([f"WHEN ? THEN {i}" for i, _ in enumerate(categorias)])}
                    ELSE {len(categorias)}
                END,
                t.id, e.nombre
        """, [isla_id] + categorias + categorias)

        rows = cur.fetchall()

        # Agrupar por categoria
        by_category = {}
        for row in rows:
            cat = row["categoria"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append({
                "nombre": row["estudio"],
                "tipo": row["tipo"]
            })

        return jsonify({
            "isla": isla_nombre,
            "categorias": categorias,
            "total": len(rows),
            "recomendados_por_categoria": by_category
        })
    finally:
        conn.close()


@app.route("/api/health", methods=["GET"])
def health():
    """Endpoint de salud para verificar que el servidor esta corriendo."""
    return jsonify({"status": "ok", "db_exists": os.path.exists(DB_PATH)})


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print(f"AVISO: No se encontro la base de datos en {DB_PATH}")
        print("Ejecuta primero: python init_db.py")
    else:
        print(f"Base de datos encontrada: {DB_PATH}")

    print("Servidor iniciando en http://localhost:5000")
    port=process.env.PORT || 4000
    app.run(host="0.0.0.0", port=port, debug=True)
