<a id="readme-top"></a>

[![Python][python-shield]][python-url]
[![Gemini][gemini-shield]][gemini-url]
[![OWASP][owasp-shield]][owasp-url]
[![Git][git-shield]][git-url]
[![dotenv][dotenv-shield]][dotenv-url]

<div align="center">
  <h3 align="center">Revisor de Código Automatizado con LLM</h3>
  <p align="center">
    Proyecto del Track 06: AI Software Engineer. Herramienta CLI en Python
    que automatiza la revisión de código integrando un LLM al flujo de Git,
    generando reportes Markdown con hallazgos clasificados por seguridad
    (OWASP Top 10 2025), errores potenciales, rendimiento y estilo.
    <br />
  </p>
</div>

---

## Tabla de contenidos

<details>
  <summary>Ver contenidos</summary>
  <ol>
    <li><a href="#sobre-el-proyecto">Sobre el proyecto</a></li>
    <li><a href="#tecnologías">Tecnologías</a></li>
    <li><a href="#requisitos-previos">Requisitos previos</a></li>
    <li><a href="#instalación">Instalación</a></li>
    <li><a href="#uso">Uso</a></li>
    <li><a href="#estructura-del-proyecto">Estructura del proyecto</a></li>
    <li><a href="#plataforma-de-ia-elegida-y-justificación">Plataforma de IA elegida y justificación</a></li>
    <li><a href="#contacto">Contacto</a></li>
  </ol>
</details>

---

## Sobre el proyecto

Herramienta de línea de comandos que automatiza la revisión de código
dentro del flujo de trabajo con Git. Obtiene el diff entre dos ramas o
commits, lo envía a Gemini 2.5 Flash mediante un prompt estructurado y
genera un reporte Markdown con hallazgos clasificados por categoría y
severidad.

**Características:**

- Obtención del diff mediante `git diff` vía `subprocess` o desde
  un archivo `.diff` pregenerado
- Prompt de sistema estructurado con salida JSON validada
- Reporte Markdown con resumen ejecutivo, tabla por severidad y detalle
  de cada hallazgo con fragmento de código y recomendación
- Clasificación por categorías: seguridad (OWASP Top 10 2025), errores
  potenciales, rendimiento y estilo
- Manejo de errores de API: reintentos con backoff exponencial ante
  respuestas 429 y formato inesperado
- Variables sensibles gestionadas con `python-dotenv`, nunca en el código
- Repositorio de prueba con 5 defectos intencionales verificados con
  el LLM y con SonarQube (extensión VS Code)

<p align="right">(<a href="#readme-top">Regresar al inicio</a>)</p>

---

## Tecnologías

- Python 3.14
- google-generativeai 0.8.6 (Gemini 2.5 Flash)
- python-dotenv
- argparse
- subprocess
- OWASP Top 10 2025

<p align="right">(<a href="#readme-top">Regresar al inicio</a>)</p>

---

## Requisitos previos

- Python 3.10 o superior
- Git instalado y disponible en el PATH
- API key de Gemini (capa gratuita — sin tarjeta de crédito)

Verifica tu versión de Python:

```sh
python --version
```

<p align="right">(<a href="#readme-top">Regresar al inicio</a>)</p>

---

## Instalación

1. Clona el repositorio:

```sh
git clone https://github.com/joaquinzarates/track06-LLM-flow-git.git
```

2. Entra a la carpeta:

```sh
cd track06-LLM-flow-git
```

3. Instala las dependencias:

```sh
pip install -r requirements.txt
```

4. Copia el archivo de variables de entorno:

```sh
cp .env.example .env
```

5. Edita `.env` y agrega tu API key:

```sh
GEMINI_API_KEY=tu_api_key_aqui
```

Obtén tu API key gratuita en [Google AI Studio](https://aistudio.google.com)
sin necesidad de tarjeta de crédito.

<p align="right">(<a href="#readme-top">Regresar al inicio</a>)</p>

---

## Uso

### Modo archivo .diff (recomendado para capa gratuita)

Genera el diff manualmente y pásalo como entrada:

```sh
git diff rama-base rama-destino > cambios.diff
python src/main.py --archivo cambios.diff --salida reporte.md
```

### Modo repositorio local

Apunta directamente a un repositorio local con dos referencias Git:

```sh
python src/main.py --repo ruta/al/repo --base main --destino feature/rama --salida reporte.md
```

### Ejemplo con el repositorio de prueba

```sh
cd ejemplos/repo_prueba
git init
git add .
git diff --cached | Out-File -FilePath cambios.diff -Encoding utf8
cd ../..
python src/main.py --archivo ejemplos/repo_prueba/cambios.diff --salida ejemplos/reporte_ejemplo.md
```

Ver el reporte generado: [`ejemplos/reporte_ejemplo.md`](ejemplos/reporte_ejemplo.md)

<p align="right">(<a href="#readme-top">Regresar al inicio</a>)</p>

---

## Estructura del proyecto

```
track06-LLM-flow-git/
├── src/
│   ├── main.py             # Entry point, interfaz CLI con argparse
│   ├── git_diff.py         # Obtención del diff (subprocess y archivo)
│   ├── revisor.py          # Integración con Gemini 2.5 Flash
│   ├── reporte.py          # Generación del reporte Markdown
│   └── config.py           # Carga de variables de entorno
├── prompts/
│   └── system_revisor.txt  # Prompt de sistema del revisor
├── ejemplos/
│   ├── repo_prueba/        # Archivos con 5 defectos intencionales
│   └── reporte_ejemplo.md  # Reporte generado de ejemplo
├── .env.example
├── requirements.txt
└── README.md
```

<p align="right">(<a href="#readme-top">Regresar al inicio</a>)</p>

---

## **Plataforma elegida: Google Gemini 2.5 Flash**

### justificación

Se eligió Gemini 2.5 Flash por las siguientes razones:

- **Capa gratuita con acceso desde código:** Gemini
  ofrece acceso sin costo vía API key desde Google AI Studio, sin requerir tarjeta de crédito.
- **Ventana de contexto de 1,048,576 tokens:** La más amplia entre las opciones gratuitas, lo que permite analizar diffs grandes sin fragmentación excesiva en la mayoría de casos reales.
- **Límite de salida de 65,536 tokens:** Suficiente para reportes  detallados con múltiples hallazgos. El proyecto usa 8,192 tokens como límite para la respuesta (equivalente a un octavo del límite de tokens de salida).
- **Salida estructurada JSON:** El modelo responde de forma consistente a un esquema definido en el prompt de sistema, facilitando la validación y el parseo antes de generar el reporte.
- **OWASP Top 10 2025:** Se utilizó la versión más reciente del estándar, presentada el año pasado, mostrando cambios en el ranking o bien el orden de aparción de las vulnerabilidades.

**Limitaciones encontradas en la capa gratuita:**

- Los datos enviados en la capa gratuita pueden usarse para mejorar los productos de Google. El nivel de pago desactiva esto. Considerar para ódigo propietario o sensible.
- Proyectos nuevos inician con un límite reducido de solicitudes diarias (20 RPD), lo que se evidenció durante las pruebas con diffs grandes. Se recomienda el modo `--archivo` para optimizar el uso de la cuota.
- Contexto de caché no disponible en capa gratuita.
- El Playground de AI Studio requiere plan de pago; el acceso gratuito es exclusivamente vía API key insertada en el código.

**Verificación adicional:**

Los 5 defectos intencionales del repositorio de prueba fueron detectados
tanto por el LLM como por SonarQube (extensión de VS Code), validando
que los hallazgos de seguridad son reales y no falsos positivos.

**Fuentes:**

- Límites de tokens: https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash?hl=es-419
- Precios y condiciones: https://ai.google.dev/gemini-api/docs/pricing?hl=es-419#standard_8
- OWASP Top 10 2025: https://owasp.org/Top10/2025/

<p align="right">(<a href="#readme-top">Regresar al inicio</a>)</p>

---

## Contacto

Joaquin Zárate - <joaquin.zarate@ids.com.mx>

Link del proyecto:
[Revisor de Código Automatizado con LLM](https://github.com/joaquinzarates/track06-LLM-flow-git)

<p align="right">(<a href="#readme-top">Regresar al inicio</a>)</p>

---

<!-- MARKDOWN LINKS & BADGES -->
[python-shield]: https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org
[gemini-shield]: https://img.shields.io/badge/Gemini_2.5_Flash-Free_Tier-4285F4?style=for-the-badge&logo=google&logoColor=white
[gemini-url]: https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash
[owasp-shield]: https://img.shields.io/badge/OWASP_Top_10-2025-000000?style=for-the-badge&logo=owasp&logoColor=white
[owasp-url]: https://owasp.org/Top10/2025/
[git-shield]: https://img.shields.io/badge/Git-Flow-F05032?style=for-the-badge&logo=git&logoColor=white
[git-url]: https://git-scm.com
[dotenv-shield]: https://img.shields.io/badge/dotenv-Config-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black
[dotenv-url]: https://github.com/theskumar/python-dotenv
