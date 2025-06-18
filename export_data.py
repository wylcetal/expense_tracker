from export_gsheets import export_to_gsheets
from export_mysql import export_to_mysql
from export_supabase import export_to_supabase


def export_data(expenses_file_path, export_type="gsheets", **kwargs):
    """
    Función principal para exportar datos a diferentes destinos

    Args:
        expenses_file_path: Ruta al archivo CSV de gastos
        export_type: Tipo de exportación ('gsheets', 'mysql', 'supabase')
        **kwargs: Argumentos específicos para cada tipo de exportación

    Returns:
        bool: True si la exportación fue exitosa, False en caso contrario
    """
    if export_type.lower() == "gsheets":
        sheet_name = kwargs.get("sheet_name", "Expense Tracker")
        return export_to_gsheets(expenses_file_path, sheet_name)

    elif export_type.lower() == "mysql":
        host = kwargs.get("host", "localhost")
        user = kwargs.get("user", "root")
        password = kwargs.get("password", "")
        database = kwargs.get("database", "expense_tracker")
        return export_to_mysql(expenses_file_path, host, user, password, database)

    elif export_type.lower() == "supabase":
        table_name = kwargs.get("table_name", "expenses")
        return export_to_supabase(expenses_file_path, table_name)

    else:
        print(f"❌ Tipo de exportación no válido: {export_type}")
        print("Tipos válidos: 'gsheets', 'mysql', 'supabase'")
        return False
