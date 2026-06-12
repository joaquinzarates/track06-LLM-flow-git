# Reporte de Revisión de Código

**Fecha:** 2026-06-12 10:25
**Comparación:** `archivo` → `ejemplos\repo_prueba\cambios.diff`
**Total de hallazgos:** 9

## Resumen Ejecutivo

El análisis del código revela múltiples vulnerabilidades de seguridad, errores potenciales, y problemas de estilo y rendimiento, principalmente debido a credenciales hardcodeadas, inyección SQL, uso inseguro de criptografía y falta de buenas prácticas de programación.

## Tabla de Hallazgos

| # | Categoría | Severidad | Título |
|---|-----------|-----------|--------|
| 1 | seguridad | 🔴 alta | Credenciales y secretos hardcodeados |
| 2 | seguridad | 🔴 alta | Usuarios y contraseñas hardcodeados para autenticación |
| 3 | error_potencial | 🟡 media | Falta de manejo de usuario no encontrado en la verificación |
| 4 | seguridad | 🔴 alta | Uso de MD5 para generación de tokens |
| 5 | seguridad | 🔴 alta | Vulnerabilidad de inyección SQL en `buscar_usuario` |
| 6 | rendimiento | 🟡 media | Conexiones de base de datos SQLite no cerradas |
| 7 | estilo | 🟢 baja | Nombres de funciones y variables no descriptivos |
| 8 | estilo | 🟢 baja | Uso de 'números mágicos' |
| 9 | estilo | 🟢 baja | Lógica duplicada en funciones |

## Detalle de Hallazgos

### 1. Credenciales y secretos hardcodeados

**Categoría:** seguridad  
**Severidad:** 🔴 alta  
**OWASP:** A02:2025 - Security Misconfiguration  
**Descripción:**  
Las credenciales y claves secretas están hardcodeadas directamente en el código fuente. Esto representa un riesgo de seguridad crítico, ya que cualquier persona con acceso al código fuente obtendrá acceso a estos secretos, comprometiendo la seguridad del sistema en producción.

**Fragmento de código:**
```
DB_PASSWORD = "admin123"
SECRET_KEY = "clave-super-secreta-produccion"
API_TOKEN = "sk-prod-abc123xyz789"
```

**Recomendación:**  
Utiliza variables de entorno o un sistema de gestión de secretos seguro (como HashiCorp Vault, AWS Secrets Manager) para almacenar y acceder a las credenciales y claves secretas. Nunca las incluyas directamente en el código fuente.

---

### 2. Usuarios y contraseñas hardcodeados para autenticación

**Categoría:** seguridad  
**Severidad:** 🔴 alta  
**OWASP:** A07:2025 - Authentication Failures  
**Descripción:**  
La lógica de autenticación en la función `verificar_usuario` utiliza un diccionario de usuarios y contraseñas hardcodeado. Esto es extremadamente inseguro, ya que las credenciales están expuestas, son difíciles de mantener y no permiten una gestión de usuarios escalable o segura. Además, las contraseñas no están hasheadas.

**Fragmento de código:**
```
    usuarios = {
        "admin": "admin123",
        "root": "root1234"
    }
```

**Recomendación:**  
Implementa un sistema de gestión de usuarios adecuado, preferiblemente con una base de datos. Las contraseñas deben ser hasheadas de forma segura utilizando algoritmos robustos (ej. bcrypt, Argon2) y nunca almacenarse en texto plano.

---

### 3. Falta de manejo de usuario no encontrado en la verificación

**Categoría:** error_potencial  
**Severidad:** 🟡 media  

**Descripción:**  
La función `verificar_usuario` intenta acceder directamente a `usuarios[usuario]`. Si el `usuario` no se encuentra en el diccionario `usuarios`, se producirá un `KeyError`, lo que podría llevar a una falla inesperada de la aplicación o una excepción no manejada.

**Fragmento de código:**
```
    return usuarios[usuario] == password
```

**Recomendación:**  
Asegúrate de verificar la existencia del usuario en el diccionario antes de intentar acceder a él. Por ejemplo, `if usuario in usuarios: return usuarios[usuario] == password else: return False`.

---

### 4. Uso de MD5 para generación de tokens

**Categoría:** seguridad  
**Severidad:** 🔴 alta  
**OWASP:** A04:2025 - Cryptographic Failures  
**Descripción:**  
La función `generar_token` utiliza el algoritmo de hash MD5 para generar tokens. MD5 es un algoritmo criptográficamente roto, vulnerable a colisiones y no es adecuado para propósitos de seguridad como la generación de tokens que podrían ser utilizados para autenticación o autorización.

**Fragmento de código:**
```
    return hashlib.md5(usuario.encode()).hexdigest()
```

**Recomendación:**  
Utiliza un método criptográficamente seguro para generar tokens, como el módulo `secrets` de Python para tokens aleatorios seguros, o una biblioteca robusta para JSON Web Tokens (JWT) si se necesita información incrustada.

---

### 5. Vulnerabilidad de inyección SQL en `buscar_usuario`

**Categoría:** seguridad  
**Severidad:** 🔴 alta  
**OWASP:** A05:2025 - Injection  
**Descripción:**  
La función `buscar_usuario` construye la consulta SQL directamente usando f-strings e incrusta el parámetro `nombre` sin sanitización o el uso de consultas parametrizadas. Esto abre la puerta a ataques de inyección SQL, permitiendo a un atacante manipular la consulta de la base de datos o ejecutar comandos SQL arbitrarios.

**Fragmento de código:**
```
    query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"
```

**Recomendación:**  
Utiliza consultas parametrizadas para prevenir la inyección SQL. Modifica la ejecución de la consulta a: `cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))`.

---

### 6. Conexiones de base de datos SQLite no cerradas

**Categoría:** rendimiento  
**Severidad:** 🟡 media  

**Descripción:**  
En las funciones `buscar_usuario` y `obtener_todos_los_registros`, se abre una conexión a la base de datos (`sqlite3.connect("usuarios.db")`), pero esta conexión nunca se cierra explícitamente. Esto puede llevar a fugas de recursos, bloqueos de archivos y degradación del rendimiento de la aplicación con el tiempo.

**Fragmento de código:**
```
    conn = sqlite3.connect("usuarios.db")
```

**Recomendación:**  
Asegúrate de cerrar la conexión de la base de datos después de cada operación. La mejor práctica es usar un bloque `with` para asegurar que la conexión se cierre automáticamente: `with sqlite3.connect("usuarios.db") as conn:`.

---

### 7. Nombres de funciones y variables no descriptivos

**Categoría:** estilo  
**Severidad:** 🟢 baja  

**Descripción:**  
Las funciones `p` y `calc` tienen nombres muy genéricos y no descriptivos. De manera similar, las variables `l`, `r` e `i` dentro de estas funciones son de una sola letra, lo que dificulta la comprensión del propósito del código y reduce la mantenibilidad.

**Fragmento de código:**
```
def p(l):
def calc(l):
```

**Recomendación:**  
Utiliza nombres de funciones y variables que describan claramente su propósito y contenido (por ejemplo, `process_list_items`, `calculate_modified_values`, `input_list`, `result_list`, `item`).

---

### 8. Uso de 'números mágicos'

**Categoría:** estilo  
**Severidad:** 🟢 baja  

**Descripción:**  
El código utiliza valores numéricos (`1.16`, `0`, `100`) directamente incrustados en la lógica sin explicación o asignación a constantes con nombres significativos. Esto hace que el código sea menos legible, más difícil de entender su propósito y propenso a errores si estos valores cambian en el futuro.

**Fragmento de código:**
```
        if i > 0:
            r.append(i * 1.16)
    return precio - (precio * d / 100)
```

**Recomendación:**  
Define constantes con nombres descriptivos para estos valores (ej. `FACTOR_INCREMENTO = 1.16`, `UMBRAL_MINIMO = 0`, `DIVISOR_PORCENTAJE = 100`) al principio del módulo o dentro de la función si su ámbito es local.

---

### 9. Lógica duplicada en funciones

**Categoría:** estilo  
**Severidad:** 🟢 baja  

**Descripción:**  
Las funciones `p` y `calc` tienen una implementación idéntica. La duplicación de código dificulta el mantenimiento, ya que cualquier corrección de errores o cambio de funcionalidad debe aplicarse en múltiples lugares, aumentando la probabilidad de introducir inconsistencias.

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
```

**Recomendación:**  
Consolida la lógica duplicada en una única función con un nombre descriptivo. Las otras funciones pueden llamar a esta función común si se requiere la misma operación bajo diferentes nombres de punto de entrada.

---
