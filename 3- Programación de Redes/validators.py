# Valida los datos para crear un producto
def validate_product_data(data, existing_products):
    
    # Verificar campos obligatorios
    if not data.get('nombre'):
        return False, "El campo 'nombre' es obligatorio"
    if 'precio' not in data:
        return False, "El campo 'precio' es obligatorio"
    if 'stock' not in data:
        return False, "El campo 'stock' es obligatorio"
    
    # Verificar que no estén vacíos
    if not data['nombre'].strip():
        return False, "El nombre no puede estar vacío"
    
    # Verificar tipo y valor de precio
    try:
        precio = float(data['precio'])
        if precio <= 0:
            return False, "El precio debe ser mayor a 0"
    except (ValueError, TypeError):
        return False, "El precio debe ser un número válido"
    
    # Verificar tipo y valor de stock
    try:
        stock = int(data['stock'])
        if stock < 0:
            return False, "El stock no puede ser negativo"
    except (ValueError, TypeError):
        return False, "El stock debe ser un número entero"
    
    # Verificar nombre duplicado (case-insensitive)
    nombre_lower = data['nombre'].strip().lower()
    for producto in existing_products:
        if producto['nombre'].lower() == nombre_lower:
            return False, f"Ya existe un producto llamado '{data['nombre']}'"
    
    return True, None

# Valida los datos para actualizar un producto
def validate_product_update(data):
    if 'nombre' in data:
        if not data['nombre'].strip():
            return False, "El nombre no puede estar vacío"
    
    if 'precio' in data:
        try:
            precio = float(data['precio'])
            if precio <= 0:
                return False, "El precio debe ser mayor a 0"
        except (ValueError, TypeError):
            return False, "El precio debe ser un número válido"
    
    if 'stock' in data:
        try:
            stock = int(data['stock'])
            if stock < 0:
                return False, "El stock no puede ser negativo"
        except (ValueError, TypeError):
            return False, "El stock debe ser un número entero"
    
    return True, None

# Valida los datos para registrar un movimiento de stock
def validate_movimiento_data(data, existing_products):
    if 'producto_id' not in data:
        return False, "El campo 'producto_id' es obligatorio"
    if 'tipo' not in data:
        return False, "El campo 'tipo' es obligatorio"
    if 'cantidad' not in data:
        return False, "El campo 'cantidad' es obligatorio"
    
    # Verificar tipo de movimiento
    if data['tipo'] not in ['entrada', 'salida']:
        return False, "El tipo debe ser 'entrada' o 'salida'"
    
    # Verificar cantidad
    try:
        cantidad = int(data['cantidad'])
        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a 0"
    except (ValueError, TypeError):
        return False, "La cantidad debe ser un número entero"
    
    # Verificar que el producto existe
    producto_id = data['producto_id']
    producto_existe = any(p['id'] == producto_id for p in existing_products)
    if not producto_existe:
        return False, f"Producto con ID {producto_id} no encontrado"
    
    return True, None