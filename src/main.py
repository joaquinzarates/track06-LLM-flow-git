import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from config import validar_configuracion
from git_diff import obtener_diff_desde_git, obtener_diff_desde_archivo
from revisor import revisar_diff
from reporte import generar_reporte

def main():
    parser = argparse.ArgumentParser(
        description="Revisor de código automatizado con LLM"
    )
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--repo", help="Ruta al repositorio local")
    grupo.add_argument("--archivo", help="Ruta a un archivo .diff")

    parser.add_argument("--base", help="Rama o commit base (requerido con --repo)")
    parser.add_argument("--destino", help="Rama o commit destino (requerido con --repo)")
    parser.add_argument("--salida", default="reporte.md", help="Nombre del archivo de salida")

    args = parser.parse_args()

    try:
        validar_configuracion()

        if args.archivo:
            diff = obtener_diff_desde_archivo(args.archivo)
            base, destino = "archivo", args.archivo
        else:
            if not args.base or not args.destino:
                parser.error("--base y --destino son requeridos cuando se usa --repo")
            diff = obtener_diff_desde_git(args.repo, args.base, args.destino)
            base, destino = args.base, args.destino

        print("Analizando diff con Gemini...")
        resultado = revisar_diff(diff)

        generar_reporte(resultado, base, destino, args.salida)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()