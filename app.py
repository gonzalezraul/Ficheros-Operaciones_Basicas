import os
import argparse
import shutil
import datetime
import unicodedata
from collections import defaultdict

# ============================================================
#  SISTEMA DE GESTIÓN DE RESERVAS
#  ------------------------------------------------------------
#  Este programa gestiona archivos de texto con reservas,
#  combinando, validando y generando archivos maestros.
#  También detecta y registra errores en los datos.
# ============================================================


# --- Constantes y rutas de trabajo ---
DOCUMENTS_DIR = 'Reservas'  # Carpeta donde se guardan los archivos de texto

# Archivos principales del sistema
RESERVATIONS_FILE = os.path.join(DOCUMENTS_DIR, 'reservas.txt')  # Archivo base de reservas individuales
MASTER_FILE = os.path.join(DOCUMENTS_DIR, 'reservas_maestro.txt')  # Archivo maestro consolidado
CORRUPT_MASTER_FILE = os.path.join(DOCUMENTS_DIR, 'reservas_maestro_con_errores.txt')  # Archivo con errores detectados
ERROR_LOG = os.path.join(DOCUMENTS_DIR, 'registro_errores.log')  # Registro de errores encontrados


# --- Funciones auxiliares (utilidades) ---

def ensure_dir(path: str):
    """Crea el directorio indicado si no existe."""
    os.makedirs(path, exist_ok=True)


def slugify(texto: str) -> str:
    """
    Convierte un texto en una versión 'segura' para usar en nombres de archivo.
    Ejemplo: 'París' -> 'paris', 'Nueva York' -> 'nueva_york'
    """
    norm = unicodedata.normalize('NFKD', texto)
    ascii_only = ''.join(c for c in norm if not unicodedata.combining(c))
    ascii_only = ascii_only.lower().replace(' ', '_')
    safe = ''.join(ch for ch in ascii_only if ch.isalnum() or ch in ['_', '-'])
    return safe


def parse_csv_line(line: str, expected_fields: int):
    """
    Valida y separa una línea CSV en campos.
    Devuelve una tupla con:
        - ok (bool): si la línea es válida
        - campos o motivo del error
        - línea original
    """
    raw = line.rstrip('\n')
    if not raw.strip():
        return False, "Línea vacía", raw

    parts = [p.strip() for p in raw.split(',')]
    if len(parts) != expected_fields:
        return False, f"Número de campos esperado {expected_fields}, recibido {len(parts)}", raw

    return True, parts, raw


def write_lines(path: str, lines):
    """Escribe una lista de líneas en un archivo de texto."""
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def log_error(message: str):
    """Registra un mensaje de error con marca temporal."""
    with open(ERROR_LOG, 'a', encoding='utf-8') as f:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {message}\n")


# --- Función principal para crear el archivo maestro ---

def process_reservations():
    """
    Lee el archivo de reservas (reservas.txt), valida los datos y crea:
        - reservas_maestro.txt con los registros válidos
        - reservas_maestro_con_errores.txt con registros con errores
        - registro_errores.log con los detalles de los errores encontrados
    """
    ensure_dir(DOCUMENTS_DIR)

    valid_lines = []   # Reservas válidas
    invalid_lines = [] # Reservas con errores

    if not os.path.exists(RESERVATIONS_FILE):
        print(f"❌ No se encontró el archivo de reservas: {RESERVATIONS_FILE}")
        return

    print("Procesando reservas...")

    with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, start=1):
            ok, data, raw = parse_csv_line(line, expected_fields=4)

            if not ok:
                # Guardar la línea problemática y registrar el error
                invalid_lines.append(raw)
                log_error(f"Línea {idx}: {data} -> {raw}")
                continue

            # Si la línea es válida, agregarla a las correctas
            valid_lines.append(','.join(data))

    # Guardar los resultados en sus archivos correspondientes
    write_lines(MASTER_FILE, valid_lines)
    write_lines(CORRUPT_MASTER_FILE, invalid_lines)

    print(f"✅ Archivo maestro generado: {MASTER_FILE}")
    print(f"⚠️  Archivo con errores: {CORRUPT_MASTER_FILE}")
    print(f"🪶 Registro de errores: {ERROR_LOG}")


# --- Función de respaldo (backup) ---

def backup_files():
    """
    Crea una copia de seguridad de todos los archivos del sistema de reservas
    en una carpeta con marca temporal.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(DOCUMENTS_DIR, f"backup_{timestamp}")
    ensure_dir(backup_dir)

    for file in [RESERVATIONS_FILE, MASTER_FILE, CORRUPT_MASTER_FILE, ERROR_LOG]:
        if os.path.exists(file):
            shutil.copy(file, backup_dir)

    print(f"📦 Copia de seguridad creada en: {backup_dir}")


# --- Interfaz de línea de comandos (CLI) ---

def main():
    """
    Permite ejecutar el programa desde la terminal con distintos comandos:
        - generar : crea los archivos maestro y de errores
        - backup  : crea una copia de seguridad de todos los archivos
    """
    parser = argparse.ArgumentParser(description="Sistema de gestión de reservas")
    parser.add_argument("accion", choices=["generar", "backup"], help="Acción a realizar")

    args = parser.parse_args()

    if args.accion == "generar":
        process_reservations()
    elif args.accion == "backup":
        backup_files()


# --- Punto de entrada del programa ---
if __name__ == "__main__":
    main()
