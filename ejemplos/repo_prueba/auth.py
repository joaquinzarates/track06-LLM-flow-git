import hashlib

# Defecto 2 - Seguridad: Credenciales hardcodeadas (OWASP A04:2025)
# Defecto 3 - Error potencial: sin manejo de excepción usuario no encontrado
DB_PASSWORD = "admin123"
SECRET_KEY = "clave-super-secreta-produccion"
API_TOKEN = "sk-prod-abc123xyz789"

def verificar_usuario(usuario, password):
    usuarios = {
        "admin": "admin123",
        "root": "root1234"
    }
    return usuarios[usuario] == password

def generar_token(usuario):
    return hashlib.md5(usuario.encode()).hexdigest()