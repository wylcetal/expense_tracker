import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from expense import Expense


def export_to_gsheets(expenses_file_path, sheet_name="Expense Tracker"):
    """
    Exporta los datos del archivo CSV a Google Sheets

    Args:
        expenses_file_path: Ruta al archivo CSV de gastos
        sheet_name: Nombre de la hoja de cálculo en Google Sheets
    """
    try:
        # 1. Cargar los datos del CSV
        expenses = []
        with open(expenses_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip():  # Ignorar líneas vacías
                    name, amount, category = line.strip().split(",")
                    expense = Expense(
                        name=name, category=category, amount=float(amount)
                    )
                    expenses.append(expense)

        # 2. Convertir a DataFrame para facilitar la exportación
        data = {
            "Nombre": [expense.name for expense in expenses],
            "Monto": [expense.amount for expense in expenses],
            "Categoría": [expense.category for expense in expenses],
        }
        df = pd.DataFrame(data)

        # 3. Autenticar con Google Sheets
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", scope
        )
        client = gspread.authorize(credentials)

        # 4. Abrir o crear la hoja de cálculo
        try:
            spreadsheet = client.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(sheet_name)
            # Compartir con tu correo para que puedas acceder
            # spreadsheet.share('tu_email@gmail.com', perm_type='user', role='writer')

        # 5. Seleccionar la primera hoja o crearla si no existe
        try:
            worksheet = spreadsheet.worksheet("Gastos")
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title="Gastos", rows=100, cols=20)

        # 6. Limpiar la hoja y actualizar con nuevos datos
        worksheet.clear()

        # 7. Agregar encabezados y datos
        headers = ["Nombre", "Monto", "Categoría"]
        worksheet.append_row(headers)

        # Convertir el DataFrame a lista de listas para gspread
        values = df.values.tolist()
        for row in values:
            worksheet.append_row(row)

        print(f"✅ Datos exportados exitosamente a Google Sheets: '{sheet_name}'")
        print(f"📊 URL: {spreadsheet.url}")
        return spreadsheet.url

    except Exception as e:
        print(f"❌ Error al exportar a Google Sheets: {str(e)}")
        return None
