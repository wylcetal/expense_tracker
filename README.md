# Expense Tracking App

Una aplicación de seguimiento de gastos con capacidad para exportar datos a Google Sheets, MySQL y Supabase.

## Índice

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
  - [Configuración del Entorno Virtual](#configuración-del-entorno-virtual)
  - [Instalación de Dependencias](#instalación-de-dependencias)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
- [Configuración de Servicios de Exportación](#configuración-de-servicios-de-exportación)
  - [Google Sheets](#google-sheets)
  - [MySQL](#mysql)
  - [Supabase](#supabase)
    - [Solución al Error de Row Level Security](#solución-al-error-de-row-level-security)
- [Ejecución de Scripts de Exportación](#ejecución-de-scripts-de-exportación)

## Descripción del Proyecto

Esta aplicación permite registrar gastos diarios, categorizarlos y visualizar resúmenes. Además, ofrece la funcionalidad de exportar los datos a:

- Google Sheets
- Base de datos MySQL
- Supabase (base de datos PostgreSQL en la nube)

## Requisitos

- Python 3.11 o superior
- Gestor de paquetes `uv` (recomendado)
- Acceso a internet para la exportación a servicios en la nube

## Instalación

### Configuración del Entorno Virtual

1. Instala `uv` si aún no lo tienes:

```bash
pip install uv
```

2. Clona el repositorio:

```bash
git clone <url-del-repositorio>
cd Expense_Tracking_App
```

3. Crea un entorno virtual con `uv`:

```bash
uv venv
```

4. Activa el entorno virtual:

En Windows:
```bash
.venv\Scripts\activate
```

En macOS/Linux:
```bash
source .venv/bin/activate
```

### Instalación de Dependencias

Instala todas las dependencias necesarias usando `uv`:

```bash
uv pip install -r requirements.txt
```

O instala las dependencias individualmente:

```bash
uv pip install gspread oauth2client pandas mysql-connector-python requests supabase python-dotenv
```

## Estructura del Proyecto

```
Expense_Tracking_App/
│
├── diagramas/             # Diagramas del proyecto
│   ├── App requirements.png
│   └── Expense_tracking_APP.png
├── expense_tracker.py     # Aplicación principal
├── expense.py             # Clase Expense
├── expenses.csv           # Archivo de datos
├── export_gsheets.py      # Exportación a Google Sheets
├── export_mysql.py        # Exportación a MySQL
├── export_supabase.py     # Exportación a Supabase
├── export_data.py         # Integración de exportaciones
├── main.py                # Punto de entrada alternativo
├── credentials.json       # Credenciales de Google Sheets (debes crearlo)
├── .env                   # Variables de entorno para credenciales (debes crearlo)
├── pyproject.toml         # Configuración del proyecto
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

## Uso

Para ejecutar la aplicación principal:

```bash
python expense_tracker.py
```

La aplicación muestra un menú con las siguientes opciones:

1. **Agregar Gasto**: Permite registrar un nuevo gasto con nombre, monto y categoría.
2. **Resumir Gastos**: Muestra un resumen de gastos por categoría, total gastado y presupuesto restante.
3. **Exportar Datos**: Abre el submenú de exportación.
4. **Salir**: Cierra la aplicación.

## Configuración de Servicios de Exportación

### Google Sheets

1. **Crear un proyecto en Google Cloud Console**:
   - Ve a [Google Cloud Console](https://console.cloud.google.com/)
   - Crea un nuevo proyecto
   - Ve a "APIs y servicios" > "Biblioteca"
   - Busca y habilita las siguientes APIs:
     - Google Sheets API
     - Google Drive API

2. **Crear credenciales**:
   - Ve a "APIs y servicios" > "Credenciales"
   - Haz clic en "Crear credenciales" > "Cuenta de servicio"
   - Completa los campos requeridos y haz clic en "Crear"
   - Asigna el rol "Editor" a la cuenta de servicio
   - Haz clic en "Continuar" y luego en "Listo"

3. **Descargar archivo de credenciales**:
   - En la lista de cuentas de servicio, haz clic en la cuenta recién creada
   - Ve a la pestaña "Claves"
   - Haz clic en "Agregar clave" > "Crear nueva clave"
   - Selecciona "JSON" y haz clic en "Crear"
   - Se descargará un archivo JSON. Renómbralo a `credentials.json` y colócalo en la carpeta raíz del proyecto

4. **Compartir hoja de cálculo**:
   - Si ya tienes una hoja de cálculo en Google Sheets que quieres usar, compártela con la dirección de correo electrónico de la cuenta de servicio (se encuentra en el archivo `credentials.json` como `client_email`)
   - Si no tienes una hoja, la aplicación creará una automáticamente

### MySQL

1. **Instalar MySQL Server**:
   - Descarga e instala [MySQL Server](https://dev.mysql.com/downloads/mysql/)
   - Durante la instalación, configura un usuario root y contraseña
   - Instala el conector de MySQL para Python: pip install mysql-connector-python

2. **Crear base de datos**:
   - Abre MySQL Command Line Client o MySQL Workbench
   - Ejecuta:
     ```sql
     CREATE DATABASE expense_tracker;
     USE expense_tracker;
     CREATE TABLE expenses (
         id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(255) NOT NULL,
         amount DECIMAL(10, 2) NOT NULL,
         category VARCHAR(255) NOT NULL
     );
     ```

3. **Configurar usuario** (opcional, para mayor seguridad):
   ```sql
   CREATE USER 'expense_user'@'localhost' IDENTIFIED BY 'tu_contraseña';
   GRANT ALL PRIVILEGES ON expense_tracker.* TO 'expense_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Supabase

1. **Crear cuenta y proyecto**:
   - Regístrate en [Supabase](https://supabase.com/)
   - Crea un nuevo proyecto
   - Anota la URL del proyecto y la clave API (en Configuración > API)
   - Instala la librería supabase: pip install supabase

2. **Crear tabla**:
   - En el panel de Supabase, ve a "Table editor"
   - Crea una nueva tabla llamada `expenses` con las siguientes columnas:
     - `id`: tipo uuid, primary key
     - `name`: tipo text
     - `amount`: tipo numeric
     - `category`: tipo text
3. **Puedes habilitar RLS (Row Level Security) con el siguiente comando SQL**:
   ```sql
   alter table site_pages enable row level security;
   ```

3. **Configurar variables de entorno**:
   - Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```
   SUPABASE_URL=tu_url_de_supabase
   SUPABASE_SERVICE_KEY=tu_clave_de_servicio_de_supabase
   ```

## Ejecución de Scripts de Exportación

### Exportación a Google Sheets

1. Ejecuta la aplicación: `python expense_tracker.py`
2. Selecciona la opción "3" (Exportar Datos)
3. Selecciona la opción "1" (Export to Google Sheets)
4. Ingresa el nombre de la hoja de cálculo (o presiona Enter para usar el nombre predeterminado)
5. La aplicación exportará los datos y mostrará la URL de la hoja de cálculo

### Exportación a MySQL

1. Ejecuta la aplicación: `python expense_tracker.py`
2. Selecciona la opción "3" (Exportar Datos)
3. Selecciona la opción "2" (Export to MySQL)
4. Ingresa los detalles de conexión:
   - Host (predeterminado: localhost)
   - Usuario (predeterminado: root)
   - Contraseña
   - Nombre de la base de datos (predeterminado: expense_tracker)
5. La aplicación exportará los datos a la tabla `expenses`

### Exportación a Supabase

1. Ejecuta la aplicación: `python expense_tracker.py`
2. Selecciona la opción "3" (Exportar Datos)
3. Selecciona la opción "3" (Export to Supabase)
4. Ingresa el nombre de la tabla (predeterminado: expenses)
5. La aplicación exportará los datos a Supabase

## Dependencias

El proyecto utiliza las siguientes dependencias principales:

- **gspread (≥6.2.1)**: Cliente para API de Google Sheets
- **oauth2client (≥4.1.3)**: Autenticación con servicios de Google
- **pandas (≥2.3.0)**: Manipulación y análisis de datos
- **mysql-connector-python (≥9.3.0)**: Conexión con bases de datos MySQL
- **python-dotenv (≥1.1.0)**: Gestión de variables de entorno
- **requests (≥2.32.4)**: Realización de solicitudes HTTP
- **supabase (≥2.15.3)**: Cliente para API de Supabase

---

Con esta configuración, podrás gestionar tus gastos y exportar los datos a diferentes plataformas según tus necesidades.
