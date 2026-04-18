import sqlite3
import config

# FUNCIONES DE CONEXIÓN
def get_db_connection():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    # Tabla de movimientos de stock
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            tipo TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            motivo TEXT,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)
    
    conn.commit()
    conn.close()

# Carga los productos iniciales si la tabla está vacía
def seed_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar si ya hay productos
    cursor.execute("SELECT COUNT(*) FROM productos")
    count = cursor.fetchone()[0]
    
    if count == 0:
        for producto in config.PRODUCTOS_INICIALES:
            cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                (producto["nombre"], producto["precio"], producto["stock"])
            )
        conn.commit()
        print("Productos iniciales cargados correctamente")
    else:
        print(f"ℹBase de datos ya contiene {count} productos")
    
    conn.close()

# FUNCIONES DE PRODUCTOS (CRUD)

#  Retorna TODOS los productos de la base de datos
def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return productos

# Retorna UN producto por su ID
def get_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# Crea un nuevo producto
def create_product(nombre, precio, stock):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            (nombre, precio, stock)
        )
        conn.commit()
        product_id = cursor.lastrowid
        return get_product_by_id(product_id)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

# Actualiza un producto existente (solo campos no None)
def update_product(product_id, nombre=None, precio=None, stock=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar si existe
    producto = get_product_by_id(product_id)
    if not producto:
        conn.close()
        return None
    
    # Construir UPDATE dinámico
    updates = []
    values = []
    
    if nombre is not None:
        updates.append("nombre = ?")
        values.append(nombre)
    if precio is not None:
        updates.append("precio = ?")
        values.append(precio)
    if stock is not None:
        updates.append("stock = ?")
        values.append(stock)
    
    if updates:
        values.append(product_id)
        query = f"UPDATE productos SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
    
    producto_actualizado = get_product_by_id(product_id)
    conn.close()
    return producto_actualizado

# Elimina un producto por ID
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))
    conn.commit()
    eliminado = cursor.rowcount > 0
    conn.close()
    return eliminado

# FUNCIONES DE MOVIMIENTOS

# Registra un movimiento de stock (entrada o salida)
def create_movimiento(producto_id, tipo, cantidad, motivo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO movimientos (producto_id, tipo, cantidad, motivo) VALUES (?, ?, ?, ?)",
        (producto_id, tipo, cantidad, motivo)
    )
    conn.commit()
    movimiento_id = cursor.lastrowid
    conn.close()
    return movimiento_id

# Retorna todos los movimientos registrados
def get_all_movimientos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, p.nombre as producto_nombre 
        FROM movimientos m
        JOIN productos p ON m.producto_id = p.id
        ORDER BY m.fecha DESC
    """)
    movimientos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return movimientos

init_db()
seed_data()