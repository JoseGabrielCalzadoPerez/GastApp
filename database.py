import sqlite3

class DatabaseManager:
    def __init__(self, db_name="gastapp.db"):
        self.db_name = db_name
        self.conn = None
        self.crear_tablas()

    def conectar(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def crear_tablas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monto REAL NOT NULL,
                categoria TEXT NOT NULL,
                descripcion TEXT,
                fecha TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presupuestos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT NOT NULL,
                monto_limite REAL NOT NULL,
                mes INTEGER NOT NULL,
                anio INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def insertar_gasto(self, monto, categoria, descripcion, fecha):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gastos (monto, categoria, descripcion, fecha)
            VALUES (?, ?, ?, ?)
        ''', (monto, categoria, descripcion, fecha))
        conn.commit()
        conn.close()

    def obtener_gastos_mes(self, mes, anio):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM gastos
            WHERE strftime('%m', fecha) = ? AND strftime('%Y', fecha) = ?
        ''', (str(mes).zfill(2), str(anio)))
        gastos = cursor.fetchall()
        conn.close()
        return gastos

    def obtener_total_por_categoria(self, mes, anio):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT categoria, SUM(monto) FROM gastos
            WHERE strftime('%m', fecha) = ? AND strftime('%Y', fecha) = ?
            GROUP BY categoria
        ''', (str(mes).zfill(2), str(anio)))
        resultado = cursor.fetchall()
        conn.close()
        return resultado