# Reporte de Revisión de Código

**Fecha:** 2026-06-12 10:59
**Comparación:** `archivo` → `ejemplos\repo_prueba\cambios.diff`
**Total de hallazgos:** 6

## Resumen Ejecutivo

Este análisis de código identifica varias vulnerabilidades de seguridad críticas, incluyendo credenciales hardcodeadas y inyección SQL, así como el uso de un algoritmo criptográfico débil. También se detectaron errores potenciales por la falta de manejo de casos límite y problemas de rendimiento relacionados con la gestión de conexiones a bases de datos. Finalmente, se encontraron oportunidades de mejora en el estilo y mantenibilidad del código debido a la duplicación de lógica y nombres no descriptivos.

## Tabla de Hallazgos

| # | Categoría | Severidad | Título |
|---|-----------|-----------|--------|
| 1 | seguridad | 🔴 alta | Credenciales y claves sensibles hardcodeadas |
| 2 | seguridad | 🟡 media | Uso de algoritmo hash criptográfico débil (MD5) |
| 3 | error_potencial | 🟡 media | Falta de manejo de usuario no encontrado en verificación |
| 4 | seguridad | 🔴 alta | Vulnerabilidad de Inyección SQL |
| 5 | rendimiento | 🟡 media | Conexiones a la base de datos no cerradas explícitamente |
| 6 | estilo | 🟢 baja | Lógica duplicada, nombres no descriptivos y números mágicos |

## Detalle de Hallazgos

### 1. Credenciales y claves sensibles hardcodeadas

**Categoría:** seguridad  
**Severidad:** 🔴 alta  
**OWASP:** A04:2025 - Cryptographic Failures  
**Descripción:**  
Credenciales de base de datos (`DB_PASSWORD`), claves secretas (`SECRET_KEY`) y tokens de API (`API_TOKEN`) están codificados directamente en el código fuente. Esto representa un riesgo de seguridad crítico, ya que cualquier persona con acceso al código puede obtener estas credenciales, lo que podría llevar a un acceso no autorizado al sistema o a la exposición de datos sensibles. El comentario en el código hace referencia a A04:2025.

**Fragmento de código:**
```
DB_PASSWORD = "admin123"
SECRET_KEY = "clave-super-secreta-produccion"
API_TOKEN = "sk-prod-abc123xyz789"
```

**Recomendación:**  
Utilizar un sistema de gestión de secretos (ej. HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) o variables de entorno para almacenar y acceder de forma segura a las credenciales y claves sensibles.

---

### 2. Uso de algoritmo hash criptográfico débil (MD5)

**Categoría:** seguridad  
**Severidad:** 🟡 media  
**OWASP:** A04:2025 - Cryptographic Failures  
**Descripción:**  
La función `generar_token` utiliza MD5 para generar un hash. MD5 es un algoritmo criptográfico obsoleto y considerado inseguro debido a su susceptibilidad a colisiones de hash. Si este token se utiliza para autenticación o identificación crítica, un atacante podría explotar las debilidades de MD5 para generar tokens maliciosos o suplantar identidades.

**Fragmento de código:**
```
return hashlib.md5(usuario.encode()).hexdigest()
```

**Recomendación:**  
Reemplazar MD5 por un algoritmo de hashing criptográfico moderno y robusto, como SHA-256 o SHA-3.

---

### 3. Falta de manejo de usuario no encontrado en verificación

**Categoría:** error_potencial  
**Severidad:** 🟡 media  

**Descripción:**  
La función `verificar_usuario` intenta acceder directamente a `usuarios[usuario]` sin verificar si la clave `usuario` existe en el diccionario. Si se proporciona un usuario que no existe, esto provocará un `KeyError`, lo que resultará en un fallo inesperado de la aplicación en lugar de una verificación de credenciales fallida y controlada.

**Fragmento de código:**
```
def verificar_usuario(usuario, password):
    usuarios = {
        "admin": "admin123",
        "root": "root1234"
    }
    return usuarios[usuario] == password
```

**Recomendación:**  
Asegurar que el usuario existe en el diccionario antes de intentar acceder a su valor, por ejemplo, usando el método `dict.get()` con un valor por defecto o una comprobación `if usuario in usuarios:`.

---

### 4. Vulnerabilidad de Inyección SQL

**Categoría:** seguridad  
**Severidad:** 🔴 alta  
**OWASP:** A05:2025 - Injection  
**Descripción:**  
La consulta SQL en la función `buscar_usuario` se construye concatenando directamente la variable `nombre` dentro de la cadena de consulta (f-string). Esto expone la aplicación a ataques de Inyección SQL, donde un atacante podría manipular la entrada `nombre` para ejecutar comandos SQL arbitrarios en la base de datos, lo que podría llevar a la divulgación, modificación o eliminación no autorizada de datos.

**Fragmento de código:**
```
query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"
```

**Recomendación:**  
Utilizar consultas parametrizadas o marcadores de posición para pasar los valores a la consulta SQL. Esto es la forma segura de prevenir inyecciones SQL. Por ejemplo: `cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))`.

---

### 5. Conexiones a la base de datos no cerradas explícitamente

**Categoría:** rendimiento  
**Severidad:** 🟡 media  

**Descripción:**  
En ambas funciones `buscar_usuario` y `obtener_todos_los_registros`, se abre una conexión a la base de datos SQLite, pero no se cierra explícitamente después de completar la operación. Esto puede llevar a la acumulación de conexiones abiertas, agotamiento de recursos del sistema y, potencialmente, bloqueos de archivos de base de datos, especialmente en entornos de mayor concurrencia o en el caso de errores.

**Fragmento de código:**
```
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
```

**Recomendación:**  
Asegurarse de cerrar las conexiones a la base de datos después de cada operación. Se recomienda usar un bloque `with` para la gestión automática de la conexión, lo cual garantiza que la conexión se cierre incluso si ocurren errores. Ejemplo: `with sqlite3.connect("usuarios.db") as conn:`.

---

### 6. Lógica duplicada, nombres no descriptivos y números mágicos

**Categoría:** estilo  
**Severidad:** 🟢 baja  

**Descripción:**  
Las funciones `p` y `calc` tienen exactamente la misma lógica, lo que representa una duplicación de código. Esto dificulta el mantenimiento, la lectura y la actualización del software. Además, los nombres de las funciones (`p`, `calc`) y el parámetro (`l`) no son descriptivos. El número `1.16` es un 'número mágico' cuyo significado no es inmediatamente obvio, reduciendo la claridad del código. Similarmente, el parámetro `d` en la función `descuento` no es descriptivo.

**Fragmento de código:**
```
def p(l):
    r = []
    for i in l:
        if i > 0:
            r.append(i * 1.16)
    return r

def calc(l):
    r = []
    for i in l:
        if i > 0:
            r.append(i * 1.16)
    return r

def descuento(precio, d):
```

**Recomendación:**  
Consolidar la lógica duplicada en una única función con un nombre descriptivo (ej. `aplicar_impuesto` o `incrementar_valores_positivos`). Reemplazar los 'números mágicos' con constantes con nombres significativos. Renombrar los parámetros `l` y `d` a algo más claro como `lista_valores` y `porcentaje_descuento`.

---
