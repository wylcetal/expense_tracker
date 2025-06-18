import mysql.connector
from expense import Expense


def export_to_mysql(
    expenses_file_path,
    host="localhost",
    user="root",
    password="",
    database="expense_tracker",
):
    """
    Exporta los datos del archivo CSV a una base de datos MySQL

    Args:
        expenses_file_path: Ruta al archivo CSV de gastos
        host: Host de la base de datos MySQL
        user: Usuario de MySQL
        password: Contraseña de MySQL
        database: Nombre de la base de datos
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

        # 2. Conectar a MySQL
        conn = mysql.connector.connect(host=host, user=user, password=password)
        cursor = conn.cursor()

        # 3. Crear la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.execute(f"USE {database}")

        # 4. Crear la tabla si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            category VARCHAR(255) NOT NULL
        )
        """)

        # 5. Limpiar la tabla para actualizar con nuevos datos
        cursor.execute("TRUNCATE TABLE expenses")

        # 6. Insertar los datos
        for expense in expenses:
            cursor.execute(
                "INSERT INTO expenses (name, amount, category) VALUES (%s, %s, %s)",
                (expense.name, expense.amount, expense.category),
            )

        # 7. Confirmar los cambios
        conn.commit()

        print(f"✅ Datos exportados exitosamente a MySQL: '{database}.expenses'")

        # 8. Cerrar la conexión
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Error al exportar a MySQL: {str(e)}")
        return False
