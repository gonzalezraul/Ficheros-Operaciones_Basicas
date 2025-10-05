# Ficheros: Operaciones Básicas

Proyecto del módulo de **Programación** del ciclo formativo de **Desarrollo de Aplicaciones Multiplataforma (DAM)**.

---

## 🧾 Descripción

Este proyecto simula un **sistema de gestión de reservas de vuelos** utilizando ficheros de texto para almacenar, procesar y clasificar la información.  
El objetivo principal es **practicar el manejo de ficheros en Python**, incluyendo la lectura, escritura, validación de datos y registro de errores.

El programa se divide en tres partes principales, cada una con un propósito distinto:

1. **Parte 1:** Creación, escritura y lectura de un fichero de reservas.  
2. **Parte 2:** Clasificación de reservas por destino.  
3. **Parte 3:** Manejo de errores y registro automático de líneas inválidas.

El código está completamente automatizado: basta con ejecutarlo para que realice todas las operaciones de forma secuencial.

---

## ⚙️ Funcionamiento general

Al ejecutar el programa (`python app.py`), se crean y procesan diferentes ficheros dentro de la carpeta `Reservas/`.  
El comportamiento varía según la parte que se ejecute:

- **Parte 1:** genera y procesa `reservas.txt`  
- **Parte 2:** genera y clasifica `reservas_maestro.txt`  
- **Parte 3:** genera `reservas_maestro_con_errores.txt` y registra errores en `registro_errores.log`

Cada parte puede ejecutarse de forma independiente mediante argumentos en consola.

---

## 📁 Estructura del proyecto

```
Ficheros-Operaciones_Basicas/
│
├── Reservas/                            # Carpeta donde se generan los ficheros de trabajo
│   ├── reservas.txt                     # Fichero de la Parte 1
│   ├── reservas_maestro.txt             # Fichero de la Parte 2
│   ├── reservas_maestro_con_errores.txt # Fichero con errores (Parte 3)
│   ├── registro_errores.log             # Registro de errores detectados
│   ├── reservas_madrid.txt              # Ejemplo de fichero clasificado por destino
│   └── ...                              # Otros ficheros generados
│
├── app.py                               # Archivo principal del programa
├── README.md                            # Este documento
└── .gitignore                           # Archivos ignorados por Git
```

---

## 🚀 Ejecución

### Requisitos

- **Python 3.13** o superior

### Instrucciones

1. Clona el repositorio:
   ```bash
   git clone https://github.com/gonzalezraul/Ficheros-Operaciones_Basicas.git
   cd Ficheros-Operaciones_Basicas
   ```

2. Ejecuta el programa completo:
   ```bash
   python app.py
   ```

3. También puedes ejecutar cada parte por separado:
   ```bash
   python app.py parte1
   python app.py parte2
   python app.py parte3
   ```

4. Para limpiar todos los ficheros generados:
   ```bash
   python app.py clean
   ```

---

## 🧩 Descripción por partes

### 🟢 Parte 1 — Creación y lectura de reservas

**Objetivo:**  
Simular la gestión básica de reservas de un vuelo.

**Tareas realizadas:**
1. Crear el archivo `reservas.txt` con datos de ejemplo.  
2. Escribir en él la información de varias reservas.  
3. Leer el archivo y mostrar por consola:
   - Asiento, nombre y clase de cada pasajero.  
   - Número total de reservas.  
   - Cuántos pasajeros viajan en clase *Business*.

**Archivos generados:**
- `reservas.txt` — fichero con todas las reservas.

---

### 🟡 Parte 2 — Clasificación de reservas por destino

**Objetivo:**  
Leer un fichero maestro y separar las reservas según su destino.

**Tareas realizadas:**
1. Crear `reservas_maestro.txt` con los datos de reserva (asiento, nombre, clase y destino).  
2. Leer el archivo y generar un nuevo fichero por cada destino, por ejemplo:
   - `reservas_madrid.txt`
   - `reservas_paris.txt`
   - `reservas_londres.txt`
3. Mostrar por consola:
   - Nombre de cada fichero creado.  
   - Número de reservas por destino.

**Archivos generados:**
- `reservas_maestro.txt`  
- Ficheros `reservas_<destino>.txt`

---

### 🔴 Parte 3 — Manejo de errores y registro de incidencias

**Objetivo:**  
Detectar y registrar líneas inválidas en el fichero maestro.

**Tareas realizadas:**
1. Crear `reservas_maestro_con_errores.txt` con líneas válidas e inválidas.  
2. Leer y validar cada línea:
   - Si tiene los 4 campos correctos (asiento, nombre, clase, destino), se procesa normalmente.  
   - Si está incompleta, vacía o mal formateada, se ignora y se registra el error.  
3. Registrar los errores en `registro_errores.log` con el formato:
   ```
   [Fecha y hora], [Línea con error], [Descripción del error]
   ```
4. Mostrar por consola:
   - Archivos de destino válidos y su número de reservas.  
   - Contenido completo del log de errores.

**Archivos generados:**
- `reservas_maestro_con_errores.txt`  
- `registro_errores.log`

---

## 🛠️ Tecnologías utilizadas

- **Lenguaje:** Python 3.13  
- **Librerías estándar:** `os`, `shutil`, `argparse`, `datetime`, `unicodedata`, `collections`

---

## ✅ Características destacadas

- Lectura y escritura en ficheros de texto.  
- Clasificación dinámica por destino.  
- Validación automática de formato.  
- Registro de errores con fecha y hora.  
- Automatización completa de todas las tareas.  
- Sistema de limpieza rápida de archivos generados (`python app.py clean`).

---

## 👤 Autor

**Raúl González // Itai Picornell // Isaac Cabrera**  
2º DAM — Desarrollo de Aplicaciones Multiplataforma  
Año académico: 2025–2026  

---

## 📄 Licencia

Proyecto realizado con fines educativos como parte de las prácticas del ciclo formativo.  
Todos los derechos reservados al autor.
