import sqlite3

# Defecto 1 - Seguridad: Inyección SQL (OWASP A05:2025)
# Defecto 4 - Rendimiento: conexión no cerrada, sin índice
def buscar_usuario(nombre):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"
    cursor.execute(query)
    return cursor.fetchall()

def obtener_todos_los_registros():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    return cursor.fetchall()