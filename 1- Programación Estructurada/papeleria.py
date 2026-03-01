# Carrito de compras papeleria
print("********************************************")
print("*                                          *")
print("*    BIENVENIDO A LA PAPELERIA ARCOIRIS    *")
print("*                                          *")
print("********************************************")

productos = {
    "Lapiz": { "cantidad": 10, "precio": 7 },
    "Pluma": {"cantidad": 10, "precio": 9},
    "Goma": {"cantidad": 10, "precio": 4},
    "Sacapuntas": {"cantidad": 10, "precio": 5},
    "Pegamento": {"cantidad": 10, "precio": 15},
    "Tijeras": {"cantidad": 10, "precio": 12},
    "Colores": {"cantidad": 10, "precio": 35},
    "Plumones": {"cantidad": 10, "precio": 42},
    "Cartulina": {"cantidad": 10, "precio": 8},
    "Cuaderno": {"cantidad": 10, "precio": 26}
}
print("")

# Mostrando productos
print("------------------PRODUCTOS------------------")
print("Producto:        Cantidad:      Precio:")
for key, value in productos.items():
    print(f"{key:20}{value['cantidad']}            ${value['precio']}")
print("---------------------------------------------")

# Carrito vacio
carrito = []

# Función añadir al carrito
def anadir_carrito():
    while True:
        product_comprar = input("\n¿Qué producto desea comprar? (Ingrese 's' para salir): ").strip().capitalize()
        # Verifica si el usuario quiere salir
        if product_comprar.lower() == "s":  
            break
        # Verifica si el producto existe en el inventario
        if product_comprar in productos:
            try:
                cant_comprar = int(input("Ingrese la cantidad de productos deseada: "))
                if cant_comprar < 1:
                    print("La cantidad debe ser al menos 1.")
                elif cant_comprar > 10:
                    print("Pida una cantidad más baja por favor (máximo 10).")
                # Verifica si hay suficiente inventario
                else:
                    stock_disponible = productos[product_comprar]["cantidad"]
                    if cant_comprar > stock_disponible:
                        print(f"No hay suficiente inventario. Solo quedan {stock_disponible} unidades.")
                    else:
                        # Añadir al carrito y reducir inventario
                        carrito.append({"producto": product_comprar, "cantidad": cant_comprar, "precio": productos[product_comprar]["precio"]})
                        productos[product_comprar]["cantidad"] -= cant_comprar
                        print(f"Se añadieron {cant_comprar} unidades de {product_comprar} al carrito.")
            except ValueError:
                print("Por favor, ingrese un número válido para la cantidad.")
        else:
            print("El producto ingresado no está disponible en la tienda.")

# Función para mostrar el carrito
def mostrar_carrito():
    if not carrito:  
        print("El carrito está vacío.")
    else:
        total = 0
        print("\n------------------------CARRITO------------------------")
        print("Producto------Cantidad---------Precio-----------Subtotal\n")
        for i in carrito:
            producto = i["producto"]
            cantidad = i["cantidad"]
            precio = i["precio"]
            subtotal = cantidad * precio
            total += subtotal
            print(f"{producto:15} {cantidad:<15} ${precio:<15} ${subtotal}")
        print("-----------------------------------------------------------")
        print(f"Total a pagar: ${total}\n")
        #Realización del pago
        pago = input("¿Desea pagar? (Ingrese 'si' o ingrese 'no' para regresar al menú): ")
        if pago == 'no':
            menu_opciones()
        elif pago == 'si':
            print("El pago se ha hecho con éxito")
            
# Función que muestra el menú de opciones por realizar
def menu_opciones():
    while True:  
        print("\n---------------MENÚ---------------")
        print("1. Añadir producto al carrito")
        print("2. Ver carrito y pagar")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            anadir_carrito()
        elif opcion == "2":
            mostrar_carrito()
            break
        else:
            print("Opción inválida. Por favor, inténtelo de nuevo.")

# Ejecutar el programa
menu_opciones()