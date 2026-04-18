from flask import Flask, jsonify, request
import storage
import validators
import config

app = Flask(__name__)


# ENDPOINTS DE PRODUCTOS
@app.route('/')
def home():
    # Endpoint raíz - Estado de la API.
    return jsonify({
        "mensaje": "API de Papelería Arcoíris - Funcionando",
        "endpoints": {
            "productos": "/api/productos",
            "movimientos": "/api/movimientos"
        }
    }), 200

# Listar todos los productos
@app.route('/api/productos', methods=['GET'])
def listar_productos():
    productos = storage.get_all_products()
    return jsonify(productos), 200

# Obtener un producto por ID
@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = storage.get_product_by_id(id)
    if not producto:
        return jsonify({"error": f"Producto con ID {id} no encontrado"}), 404
    return jsonify(producto), 200

# Crear un nuevo producto
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos en el request"}), 400
    
    # Validar datos
    existing_products = storage.get_all_products()
    es_valido, error = validators.validate_product_data(data, existing_products)
    if not es_valido:
        return jsonify({"error": error}), 400
    
    # Crear producto
    nuevo = storage.create_product(
        nombre=data['nombre'].strip(),
        precio=float(data['precio']),
        stock=int(data['stock'])
    )
    
    if not nuevo:
        return jsonify({"error": "Error al crear el producto (posible nombre duplicado)"}), 400
    
    return jsonify({
        "mensaje": "Producto creado exitosamente",
        "producto": nuevo
    }), 201

# Actualizar un producto completo (todos los campos)
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto_completo(id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos en el request"}), 400
    
    # Validar que todos los campos estén presentes
    if not all(key in data for key in ['nombre', 'precio', 'stock']):
        return jsonify({"error": "PUT requiere todos los campos: nombre, precio, stock"}), 400
    
    es_valido, error = validators.validate_product_update(data)
    if not es_valido:
        return jsonify({"error": error}), 400
    
    producto_existente = storage.get_product_by_id(id)
    if not producto_existente:
        return jsonify({"error": f"Producto con ID {id} no encontrado"}), 404
    
    actualizado = storage.update_product(
        product_id=id,
        nombre=data['nombre'].strip(),
        precio=float(data['precio']),
        stock=int(data['stock'])
    )
    
    return jsonify({
        "mensaje": "Producto actualizado exitosamente",
        "producto": actualizado
    }), 200
# Actualizar parcialmente un producto (solo campos enviados)
@app.route('/api/productos/<int:id>', methods=['PATCH'])
def actualizar_producto_parcial(id):

    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos en el request"}), 400
    
    es_valido, error = validators.validate_product_update(data)
    if not es_valido:
        return jsonify({"error": error}), 400
    
    producto_existente = storage.get_product_by_id(id)
    if not producto_existente:
        return jsonify({"error": f"Producto con ID {id} no encontrado"}), 404
    
    actualizado = storage.update_product(
        product_id=id,
        nombre=data.get('nombre', '').strip() if data.get('nombre') else None,
        precio=float(data['precio']) if data.get('precio') else None,
        stock=int(data['stock']) if data.get('stock') else None
    )
    
    return jsonify({
        "mensaje": "Producto actualizado exitosamente",
        "producto": actualizado
    }), 200

# Eliminar algún producto
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = storage.get_product_by_id(id)
    
    if not producto:
        return jsonify({"error": f"Producto con ID {id} no encontrado"}), 404
    
    storage.delete_product(id)
    return jsonify({
        "mensaje": f"Producto '{producto['nombre']}' eliminado exitosamente"
    }), 200


# ENDPOINTS DE MOVIMIENTOS

# Listar todos los movimientos de stock
@app.route('/api/movimientos', methods=['GET'])
def listar_movimientos():
    movimientos = storage.get_all_movimientos()
    return jsonify(movimientos), 200

# Registrar un movimiento de stock (entrada o salida)
@app.route('/api/movimientos', methods=['POST'])
def registrar_movimiento():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos en el request"}), 400
    
    # Validar datos
    existing_products = storage.get_all_products()
    es_valido, error = validators.validate_movimiento_data(data, existing_products)
    if not es_valido:
        return jsonify({"error": error}), 400
    
    producto_id = data['producto_id']
    tipo = data['tipo']
    cantidad = int(data['cantidad'])
    motivo = data.get('motivo', 'Sin especificar')
    
    # Actualizar stock según el tipo de movimiento
    producto = storage.get_product_by_id(producto_id)
    nuevo_stock = producto['stock']
    
    if tipo == 'entrada':
        nuevo_stock += cantidad
    else:  # salida
        if cantidad > producto['stock']:
            return jsonify({
                "error": f"Stock insuficiente. Solo hay {producto['stock']} unidades"
            }), 400
        nuevo_stock -= cantidad
    
    # Actualizar el stock del producto
    storage.update_product(product_id=producto_id, stock=nuevo_stock)
    
    # Registrar el movimiento
    storage.create_movimiento(
        producto_id=producto_id,
        tipo=tipo,
        cantidad=cantidad,
        motivo=motivo
    )
    
    return jsonify({
        "mensaje": f"Movimiento de {tipo} registrado exitosamente",
        "producto_id": producto_id,
        "cantidad": cantidad,
        "nuevo_stock": nuevo_stock
    }), 201

# EJECUCIÓN
if __name__ == '__main__':
    print(f"Iniciando {config.APP_NAME}...")
    app.run(debug=config.DEBUG, port=config.PORT)