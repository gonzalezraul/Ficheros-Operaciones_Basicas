# A CONTINUACIÓN TODOS LAS LIBRERIAS #

import os
import shutil
import datetime
import getpass
import csv


# CONSTANTES #

DOCUMENTS_DIR = 'Reservas'
RESERVATIONS_FILE = os.path.join(DOCUMENTS_DIR, 'reservas.txt')

# CREAR RESERVAS #

def registrar_log(mensaje):
    with open(RESERVATIONS_FILE, 'a') as f:
        f.write(f"[{datetime.datetime.now()}] {mensaje}\n")

