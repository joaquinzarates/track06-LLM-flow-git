import subprocess
import os

def obtener_diff_desde_git(ruta_repo, ref_base, ref_destino):
    if not os.path.isdir(ruta_repo):
        raise ValueError(f"La ruta especificada no existe: {ruta_repo}")

    resultado = subprocess.run(
    ["git", "diff", ref_base, ref_destino],
    cwd=ruta_repo,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace"
)

    if resultado.returncode != 0:
        raise RuntimeError(f"Error ejecutando git diff: {resultado.stderr}")

    if not resultado.stdout.strip():
        raise ValueError("El diff está vacío. Verifica las referencias.")

    return resultado.stdout

def obtener_diff_desde_archivo(ruta_archivo):
    if not os.path.isfile(ruta_archivo):
        raise ValueError(f"El archivo no existe: {ruta_archivo}")

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    if not contenido.strip():
        raise ValueError("El archivo de diff está vacío.")

    return contenido