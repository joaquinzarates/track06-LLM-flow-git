from datetime import datetime

ICONOS = {"alta": "🔴", "media": "🟡", "baja": "🟢"}

def generar_reporte(resultado, ref_base, ref_destino, archivo_salida="reporte.md"):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    hallazgos = resultado.get("hallazgos", [])
    resumen = resultado.get("resumen", "Sin resumen disponible.")

    lineas = [
        f"# Reporte de Revisión de Código",
        f"",
        f"**Fecha:** {fecha}",
        f"**Comparación:** `{ref_base}` → `{ref_destino}`",
        f"**Total de hallazgos:** {len(hallazgos)}",
        f"",
        f"## Resumen Ejecutivo",
        f"",
        f"{resumen}",
        f"",
        f"## Tabla de Hallazgos",
        f"",
        f"| # | Categoría | Severidad | Título |",
        f"|---|-----------|-----------|--------|",
    ]

    for i, h in enumerate(hallazgos, 1):
        icono = ICONOS.get(h.get("severidad", "baja"), "")
        lineas.append(
            f"| {i} | {h.get('categoria')} | "
            f"{icono} {h.get('severidad')} | {h.get('titulo')} |"
        )

    lineas += ["", "## Detalle de Hallazgos", ""]

    for i, h in enumerate(hallazgos, 1):
        owasp = f"**OWASP:** {h['owasp']}  " if h.get("owasp") else ""
        lineas += [
            f"### {i}. {h.get('titulo')}",
            f"",
            f"**Categoría:** {h.get('categoria')}  ",
            f"**Severidad:** {ICONOS.get(h.get('severidad','baja'))} "
            f"{h.get('severidad')}  ",
            f"{owasp}",
            f"**Descripción:**  ",
            f"{h.get('descripcion')}",
            f"",
            f"**Fragmento de código:**",
            f"```",
            f"{h.get('fragmento_codigo')}",
            f"```",
            f"",
            f"**Recomendación:**  ",
            f"{h.get('recomendacion')}",
            f"",
            f"---",
            f"",
        ]

    contenido = "\n".join(lineas)
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"Reporte generado: {archivo_salida}")
    return archivo_salida