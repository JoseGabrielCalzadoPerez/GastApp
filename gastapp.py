from database import DatabaseManager
from datetime import date

CATEGORIAS = ["Alimentación", "Transporte", "Salud", "Ocio", "Hogar", "Otros"]

class GastApp:
    def __init__(self):
        self.db = DatabaseManager()

    def registrar_gasto(self, monto, categoria, descripcion, fecha=None):
        if categoria not in CATEGORIAS:
            raise ValueError(f"Categoría inválida. Opciones: {CATEGORIAS}")
        if fecha is None:
            fecha = str(date.today())
        self.db.insertar_gasto(monto, categoria, descripcion, fecha)
        return True

    def obtener_resumen_mensual(self, mes, anio):
        return self.db.obtener_total_por_categoria(mes, anio)

    def obtener_gastos_del_mes(self, mes, anio):
        return self.db.obtener_gastos_mes(mes, anio)