from expense import Expense
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


def export_to_supabase(expenses_file_path, table_name="expenses"):
    """
    Exporta los datos del archivo CSV a Supabase

    Args:
        expenses_file_path: Ruta al archivo CSV de gastos
        table_name: Nombre de la tabla en Supabase
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

        # 2. Preparar los datos para Supabase
        data = []
        for expense in expenses:
            data.append(
                {
                    "name": expense.name,
                    "amount": expense.amount,
                    "category": expense.category,
                }
            )
        response = supabase.table(table_name).insert(data).execute()
        print(f"✅ Datos exportados exitosamente a Supabase: tabla '{table_name}'")
        return response

    except Exception as e:
        print(f"❌ Error al exportar a Supabase: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "status_code": getattr(e, "status_code", None),
            "data": None,
        }
