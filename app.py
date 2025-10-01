import os
import argparse
import shutil
import datetime
import unicodedata
from collections import defaultdict

# --- Constantes y rutas ---
DOCUMENTS_DIR = 'Reservas'

RESERVATIONS_FILE = os.path.join(DOCUMENTS_DIR, 'reservas.txt')  # Parte 1
MASTER_FILE = os.path.join(DOCUMENTS_DIR, 'reservas_maestro.txt')  # Parte 2
CORRUPT_MASTER_FILE = os.path.join(DOCUMENTS_DIR, 'reservas_maestro_con_errores.txt')  # Parte 3
ERROR_LOG = os.path.join(DOCUMENTS_DIR, 'registro_errores.log')  # Parte 3


# --- Utilidades ---
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def slugify(texto: str) -> str:
    """
    Convierte 'París' -> 'paris', 'Nueva York' -> 'nueva_york'
    para generar nombres de archivo seguros.
    """
    norm = unicodedata.normalize('NFKD', texto)
    ascii_only = ''.join(c for c in norm if not unicodedata.combining(c))
    ascii_only = ascii_only.lower().replace(' ', '_')
    safe = ''.join(ch for ch in ascii_only if ch.isalnum() or ch in ['_', '-'])
    return safe


def parse_csv_line(line: str, expected_fields: int):
    """
    Devuelve (ok, campos|motivo_error, linea_limpia)
    """
    raw = line.rstrip('\n')
    if not raw.strip():
        return False, "Línea vacía", raw
    parts = [p.strip() for p in raw.split(',')]
    if len(parts) != expected_fields:
        return False, f"Número de campos esperado {expected_fields}, recibido {len(parts)}", raw
    return True, parts, raw


def write_lines(path: str, lines):
    with open(path, 'w', encoding='utf-8') as f:
        for ln in lines:
            f.write(ln + '\n')


def append_line(path: str, line: str):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


# ========== PARTE 1 ==========
def parte1_crear_y_escribir():
    """
    1) Crea 'reservas.txt'
    2) Escribe las reservas en formato: asiento, nombre, clase
    """
    ensure_dir(DOCUMENTS_DIR)
    reservas = [
        "12A, Juan Pérez, Economy",
        "14B, María López, Business",
        "21C, Carlos García, Economy",
    ]
    write_lines(RESERVATIONS_FILE, reservas)
    print(f"✔ Archivo creado: {RESERVATIONS_FILE} ({len(reservas)} líneas)")


def parte1_leer_y_procesar():
    """
    - Imprime cada reserva legible
    - Cuenta total
    - Cuenta cuántos van en Business
    """
    total = 0
    business = 0
    with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            ok, data, _ = parse_csv_line(line, expected_fields=3)
            if not ok:
                # En Parte 1 asumimos que el fichero está correcto
                continue
            asiento, nombre, clase = data
            print(f"Asiento: {asiento} | Pasajero: {nombre} | Clase: {clase}")
            total += 1
            if clase.strip().lower() == "business":
                business += 1
    print(f"\nTotal de reservas: {total}")
    print(f"Pasajeros en Business: {business}")


def run_parte1():
    parte1_crear_y_escribir()
    parte1_leer_y_procesar()


# ========== PARTE 2 ==========
def parte2_crear_maestro():
    """
    Crea 'reservas_maestro.txt' con asiento, nombre, clase, destino
    """
    ensure_dir(DOCUMENTS_DIR)
    reservas = [
        "12A, Juan Pérez, Economy, Madrid",
        "14B, María López, Business, París",
        "21C, Carlos García, Economy, Madrid",
        "05D, Ana Sánchez, Business, Londres",
        "19E, Luis Gómez, Economy, París",
        "08F, Sofía Vargas, Economy, Londres",
    ]
    write_lines(MASTER_FILE, reservas)
    print(f"✔ Archivo maestro creado: {MASTER_FILE} ({len(reservas)} líneas)")


def parte2_clasificar_por_destino():
    """
    Lee el maestro y genera: reservas_<destino>.txt
    Imprime nombre de archivo y nº de reservas por destino.
    """
    contadores = defaultdict(int)
    creados = set()

    with open(MASTER_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            ok, data, raw = parse_csv_line(line, expected_fields=4)
            if not ok:
                # La Parte 2 asume fichero correcto
                continue
            asiento, nombre, clase, destino = data
            dest_slug = slugify(destino)
            out_path = os.path.join(DOCUMENTS_DIR, f"reservas_{dest_slug}.txt")
            append_line(out_path, raw)
            contadores[out_path] += 1
            creados.add(out_path)

    print("\nArchivos por destino creados:")
    for path in sorted(creados):
        print(f"- {os.path.basename(path)}: {contadores[path]} reservas")


def run_parte2():
    parte2_crear_maestro()
    parte2_clasificar_por_destino()


# ========== PARTE 3 ==========
def parte3_crear_maestro_con_errores():
    """
    Crea 'reservas_maestro_con_errores.txt' con algunas líneas inválidas.
    """
    ensure_dir(DOCUMENTS_DIR)
    reservas = [
        "12A, Juan Pérez, Economy, Madrid",           # válida
        "14B, María López, Business",                 # falta destino
        "",                                           # línea vacía
        "21C Carlos García Economy Madrid",           # sin comas
        "05D, Ana Sánchez, Business, Londres",        # válida
        "[2025-09-20 23:54:00]",                      # formato totalmente incorrecto
        ", , , ",                                     # 4 campos vacíos
        "19E, Luis Gómez, Economy, París",            # válida
    ]
    write_lines(CORRUPT_MASTER_FILE, reservas)
    # Reiniciamos el log de errores
    write_lines(ERROR_LOG, [])
    print(f"✔ Archivo con errores creado: {CORRUPT_MASTER_FILE}")


def log_error(raw_line: str, descripcion: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    append_line(ERROR_LOG, f"{timestamp}, {raw_line}, {descripcion}")


def parte3_procesar_con_errores():
    """
    - Valida que cada línea tenga 4 campos (asiento, nombre, clase, destino).
    - Las válidas se clasifican por destino (igual que en Parte 2).
    - Las inválidas se registran en 'registro_errores.log'
      con [fecha y hora], [línea con error], [descripción].
    - Al final imprime resumen y muestra el contenido del log.
    """
    contadores = defaultdict(int)
    creados = set()

    with open(CORRUPT_MASTER_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            ok, data_or_msg, raw = parse_csv_line(line, expected_fields=4)
            if ok:
                asiento, nombre, clase, destino = data_or_msg
                dest_slug = slugify(destino)
                out_path = os.path.join(DOCUMENTS_DIR, f"reservas_{dest_slug}.txt")
                append_line(out_path, f"{asiento}, {nombre}, {clase}, {destino}")
                contadores[out_path] += 1
                creados.add(out_path)
            else:
                log_error(raw, data_or_msg)

    print("\nResumen de archivos por destino (válidos):")
    for path in sorted(creados):
        print(f"- {os.path.basename(path)}: {contadores[path]} reservas")

    print("\nContenido de registro_errores.log:")
    if os.path.exists(ERROR_LOG):
        with open(ERROR_LOG, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(content if content else "(sin errores)")
    else:
        print("(no existe el archivo de errores)")


def run_parte3():
    parte3_crear_maestro_con_errores()
    parte3_procesar_con_errores()


# ========== Comandos CLI ==========
def clean():
    if os.path.isdir(DOCUMENTS_DIR):
        shutil.rmtree(DOCUMENTS_DIR, ignore_errors=True)
        print("✔ Carpeta 'Reservas' eliminada.")
    else:
        print("Nada que limpiar.")


def main():
    parser = argparse.ArgumentParser(description="Gestión de reservas - Acceso a Datos")
    parser.add_argument('accion', nargs='?', default='all',
                    choices=['parte1','parte2','parte3','all','clean'],
                    help="Qué ejecutar (por defecto: all)")

    args = parser.parse_args()

    if args.accion == 'clean':
        clean()
    elif args.accion == 'parte1':
        run_parte1()
    elif args.accion == 'parte2':
        run_parte2()
    elif args.accion == 'parte3':
        run_parte3()
    elif args.accion == 'all':
        run_parte1()
        print("\n" + "="*60 + "\n")
        run_parte2()
        print("\n" + "="*60 + "\n")
        run_parte3()


if __name__ == "__main__":
    main()
