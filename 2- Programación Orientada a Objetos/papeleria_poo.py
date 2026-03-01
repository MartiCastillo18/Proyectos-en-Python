import sqlite3
from datetime import datetime

class Producto:
    def __init__(self, id_prod, nombre, precio, stock):
        self.id = id_prod
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        
    def mostrar_info(self):
        print(f"{self.nombre:20} ${self.precio:10.2f}  Stock: {self.stock} \n")
        
    def actualizar_stock(self): 
        print()
        
    def a_dict(self):
        print()
        
class ItemCarrito:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = producto.precio * cantidad
        
    def calcular_subtotal(self):
        return round(self.subtotal, 2)
    
class Carrito:
    def __init__(self):
        self.items = []
        
    def agregar_item(self, producto, cantidad):
        for item in  self.items:
            if item.producto.nombre == producto.nombre:
                item.cantidad += cantidad
                item.subtotal = item.producto.precio * item.cantidad
                return
        self.items.append(ItemCarrito(producto, cantidad))
        
    def mostrar(self):
        if not self.items:
            print("El carrito está vacío")
            return
        
        else: 
            print("\n--- TU CARRITO DE COMPRAS ---")
            print(f"{'Producto':<20} {'Cant.':<10} {'Subtotal':<10}")
            
            for item in self.items:
                print(f"{item.producto.nombre:<20} {item.cantidad:<10} ${item.calcular_subtotal():<10.2f}")
                
            print(f"\nTOTAL A PAGAR: ${self.calcular_total():.2f}\n")
            
    def calcular_total(self):
        total = 0
        for item in self.items:
            total += item.calcular_subtotal()
        return round(total, 2)
    
    def vaciar(self):
        self.items = []
        
    def esta_vacio(self):
        return len(self.items) == 0
        
class SistemaPapeleria:
    def __init__(self):
        self.conn = sqlite3.connect("papeleria.db")
        self.cursor = self.conn.cursor()
        self.crear_tablas()
        self.carrito = Carrito()
         
    def crear_tablas(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS productos(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre TEXT UNIQUE NOT NULL,
                                precio REAL NOT NULL,
                                stock INTEGER NOT NULL
                                )
                                """)
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS ventas(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                cliente_nombre TEXT,
                                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                total REAL
                            )
                            """)
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS detalle_venta(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                venta_id INTEGER,
                                producto_id INTEGER,
                                cantidad INTEGER,
                                subtotal REAL,
                                FOREIGN KEY (venta_id) REFERENCES ventas(id),
                                FOREIGN KEY (producto_id) REFERENCES productos(id)
                            )
                            """)
        
        self.conn.commit()
    

    def menu_principal(self):
        while True:
            print("¿Qué tipo de usuario es?")
            print("1.- Cliente")
            print("2.- Administrador")
            print("3.- Salir")
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.menu_cliente()
            elif opcion == "2":
                self.menu_admin()
            elif opcion == "3":
                print("Saliendo...")
                self.conn.close()
                break
            else:
                print("Opción inválida. Ingrese una opción valida\n")
    
    def menu_cliente(self):
        print("\n********************************************")
        print("*                                          *")
        print("*    BIENVENIDO A LA PAPELERIA ARCOIRIS    *")
        print("*                                          *")
        print("********************************************\n")
        while True:
            print("\n1.- Ver productos")     
            print("2.- Agregar al carrito")
            print("3.- Ver Carrito")
            print("4.- Pagar")
            print("5.- Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.ver_inventario()
            elif opcion == "2":
                self.agregar_al_carrito()
            elif opcion == "3":
                self.carrito.mostrar()
            elif opcion == "4":
                self.pagar()
            elif opcion == "5":
                print("Volviendo...")
                break
            else:
                print("Opción inválida. Ingrese una opción valida\n")
            
    def menu_admin(self):
        print("\n----- MODO ADMINISTRADOR -----\n")
        while True:
            print("\n1.- Ver Inventario")
            print("2.- Agregar Producto")
            print("3.- Eliminar Producto")
            print("4.- Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.ver_inventario()
            elif opcion == "2":
                self.agregar_producto()
            elif opcion == "3":
                self.eliminar_producto()
            elif opcion == "4":
                print("Volviendo...")
                break
            else:
                print("Opción invalida. Ingresa una opción valida\n")
            
    # Función para agregar producto al inventario    
    def agregar_producto(self):
        print("\n--- AGREGAR NUEVO PRODUCTO ---\n")
        nombre = input("Nombre del producto: ").strip().capitalize()
        
        # Validación para precios
        try:
            precio = float(input("Precio: $"))
            if precio <= 0:
                print("El precio no puede ser negativo o igual a cero")
                return
        except ValueError:
            print("Error: Ingrese un número válido para el precio")
            return
        
        # Validación para stock
        try:
            stock = int(input("Cantidad que desea agregar: "))
            if stock <= 0:
                print("El stock no puede ser negativo o igual a 0")
                return
        except ValueError:
            print("Error: Ingrese un número entero para el stock")
            return
        
        # Insertar en la BD
        try:
            self.cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                (nombre, precio, stock)
            )
            self.conn.commit()
            print("Producto agregado exitosamente\n")
        except sqlite3.IntegrityError:
            print("Error: Ya existe un producto con ese nombre\n")
    
    # Función para eliminar producto del inventario        
    def eliminar_producto(self):
        print("\n--- ELIMINAR PRODUCTO ---")
        nombre = input("Ingrese el nombre del producto que desea eliminar: ").strip().capitalize()
        
        self.cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
        self.conn.commit()
        
        if self.cursor.rowcount == 0:
            print("No se encontro ningún producto con ese nombre")
        else:
            print("Producto eliminado correctamente\n")
            
            
        
    # Función para ver el inventario
    def ver_inventario(self):
        self.cursor.execute(
            "SELECT * FROM productos;"
        )
        filas = self.cursor.fetchall()
        if not filas:
            print("No hay productos registrados\n")
        else: 
            for fila in filas:
                prod = Producto(id_prod=fila[0], nombre=fila[1], precio=fila[2], stock=fila[3])
                prod.mostrar_info()
        
    def buscar_producto_por_nombre(self, nombre):
        self.cursor.execute(
            "SELECT id, nombre, precio, stock FROM productos WHERE nombre = ?",
            (nombre,)
        )
        fila = self.cursor.fetchone()
            
        if fila:
            return Producto(id_prod=fila[0], nombre=fila[1], 
                        precio=fila[2], stock=fila[3])
        return None
        
    def agregar_al_carrito(self):
        print("\n--- AGREGAR AL CARRITO ---")
        nombre = input("Nombre del producto: ").strip().capitalize()
            
        producto = self.buscar_producto_por_nombre(nombre)
        if not producto:
            print("Producto no encontrado en el inventario")
            return
            
        # Mostrar info y stock disponible
        print(f"{producto.nombre} - Precio: ${producto.precio:.2f}")
        print(f"   Stock disponible: {producto.stock}")
            
        # Pedir cantidad con validaciones
        try:
            cantidad = int(input("Cantidad a agregar: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor a 0")
                return
            if cantidad > producto.stock:
                print(f" No hay suficiente stock. Solo quedan {producto.stock} unidades\n")
                return
        except ValueError:
            print("Error: Ingresa un número válido\n")
            return
            
        # Agregar al carrito
        self.carrito.agregar_item(producto, cantidad)
    
    def pagar(self):
        # Verificar carrito no vacío
        if self.carrito.esta_vacio():
            print("El carrito está vacío. Agrega productos primero.")
            return
        
        # Pedir nombre del cliente
        print("\n--- PROCESAR PAGO ---")
        cliente = input("Nombre del cliente (opcional): ").strip()
        if not cliente:
            cliente = "Cliente anónimo"
        
        # Calcular totales
        subtotal = self.carrito.calcular_total()
        iva = subtotal * 0.16
        total = subtotal + iva
        
        # Guardar venta en tabla 'ventas'
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute(
            "INSERT INTO ventas (cliente_nombre, fecha, total) VALUES (?, ?, ?)",
            (cliente, fecha, total)
        )
        venta_id = self.cursor.lastrowid
        
        # Guardar detalles y actualizar stock
        for item in self.carrito.items:
            self.cursor.execute(
                "INSERT INTO detalle_venta (venta_id, producto_id, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                (venta_id, item.producto.id, item.cantidad, item.calcular_subtotal())
            )
            
            self.cursor.execute(
                "UPDATE productos SET stock = stock - ? WHERE id = ?",
                (item.cantidad, item.producto.id)
            )
        
        # Confirmar cambios
        self.conn.commit()
        
        # Mostrar ticket
        print("\n--- TICKET DE VENTA ---\n")
        print(f"Cliente: {cliente}")
        print(f"Fecha: {fecha}")
        print("-"*50)
        for item in self.carrito.items:
            print(f"{item.producto.nombre:20} x{item.cantidad:2}  ${item.calcular_subtotal():.2f}")
        print("-"*50)
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"IVA (16%): ${iva:.2f}")
        print(f"TOTAL: ${total:.2f}")
        print("="*50)
        print("¡Gracias por tu compra!\n")
        
        # Vaciar carrito
        self.carrito.vaciar()
            
        
    def ejecutar(self):
        self.menu_principal()

        
if __name__ == "__main__":
    app = SistemaPapeleria()
    app.ejecutar()