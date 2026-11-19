from flask import Flask, request, redirect, url_for, flash, session, render_template_string
from flask_mysqldb import MySQL
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura' 
app.config['SESSION_TYPE'] = 'filesystem'

# --- Configuración de la base de datos ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tiendita'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)

# ==============================================================================
# DISEÑO HTML (Incrustado para que no necesites carpetas)
# ==============================================================================
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Papelería Torres</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --color-1: #C9B6A8; --color-2: #E8DCCF; --color-3: #B89A86; --color-4: #F4EFE9; --color-5: #A78470; }
        body { background-color: var(--color-4); font-family: 'Poppins', sans-serif; color: var(--color-5); }
        .navbar-custom { background-color: var(--color-5); color: white; padding: 15px 20px; border-radius: 0 0 15px 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar-custom h1 { font-size: 1.8rem; font-weight: 600; margin: 0; }
        .card-custom { background-color: white; border: none; border-radius: 15px; box-shadow: 0 4px 10px rgba(167, 132, 112, 0.15); margin-bottom: 20px; }
        .card-header-custom { background-color: var(--color-2); color: var(--color-5); font-weight: 600; border-radius: 15px 15px 0 0 !important; padding: 15px 20px; border-bottom: 2px solid var(--color-1); }
        .table-custom { background-color: white; border-radius: 0 0 15px 15px; overflow: hidden; }
        .table-custom thead { background-color: var(--color-3); color: white; }
        .table-custom tbody tr:hover { background-color: var(--color-4); }
        .btn-custom-primary { background-color: var(--color-5); color: white; border: none; border-radius: 8px; font-weight: 600; }
        .btn-custom-primary:hover { background-color: var(--color-3); color: white; }
        .btn-custom-secondary { background-color: var(--color-1); color: var(--color-5); border: none; border-radius: 8px; font-weight: 600; }
        .btn-custom-secondary:hover { background-color: var(--color-2); color: var(--color-5); }
        .btn-custom-danger { background-color: #c97a7a; color: white; border: none; border-radius: 8px; }
        .form-control { border: 1px solid var(--color-1); border-radius: 8px; }
        .form-control:focus { border-color: var(--color-5); box-shadow: 0 0 0 0.25rem rgba(167, 132, 112, 0.25); }
        .alert { border-radius: 10px; border: none; }
    </style>
</head>
<body>
    <div class="navbar-custom d-flex justify-content-between align-items-center">
        <h1>Papelería Torres</h1>
        <div>
            <span class="me-3">Bienvenido, <strong>{{ session['username'] }}</strong></span>
            <a href="#" class="btn btn-sm btn-custom-secondary" data-bs-toggle="modal" data-bs-target="#ventaModal">Ir a Ventas</a>
            <a href="{{ url_for('logout') }}" class="btn btn-sm btn-custom-danger">Cerrar Sesión</a>
        </div>
    </div>

    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% if error_msg %}<div class="alert alert-danger">{{ error_msg }}</div>{% endif %}

        <div class="card card-custom p-3 mb-4">
            <form action="{{ url_for('search') }}" method="GET" class="d-flex align-items-center">
                <input type="text" name="id_compra" class="form-control me-2" placeholder="Buscar por ID o Nombre..." value="{{ search_query or '' }}">
                <button type="submit" class="btn btn-custom-primary me-2">Buscar</button>
                <a href="{{ url_for('index') }}" class="btn btn-custom-secondary">Ver Todo</a>
            </form>
        </div>

        <div class="card card-custom">
            <div class="card-header card-header-custom">
                {% if compra_a_editar %}Editar Producto{% else %}Registrar Nuevo Producto{% endif %}
            </div>
            <div class="card-body">
                <form action="{% if compra_a_editar %}{{ url_for('update', compra_id=compra_a_editar.id_compra) }}{% else %}{{ url_for('add') }}{% endif %}" method="POST">
                    <div class="row g-3">
                        <div class="col-md-3">
                            <input type="text" name="id_compra" class="form-control" placeholder="ID (ej: P051)" value="{{ compra_a_editar.id_compra if compra_a_editar else '' }}" required {% if compra_a_editar %}readonly{% endif %}>
                        </div>
                        <div class="col-md-5">
                            <input type="text" name="nombre" class="form-control" placeholder="Nombre del Producto" value="{{ compra_a_editar.nombre if compra_a_editar else '' }}" required>
                        </div>
                        <div class="col-md-4">
                            <input type="number" step="0.01" name="unitario" class="form-control" placeholder="Costo Unitario ($)" value="{{ compra_a_editar.unitario if compra_a_editar else '' }}" required>
                        </div>
                        <div class="col-md-3"><input type="text" name="marca" class="form-control" placeholder="Marca" value="{{ compra_a_editar.marca if compra_a_editar else '' }}"></div>
                        <div class="col-md-3"><input type="text" name="modelo" class="form-control" placeholder="Modelo / SKU" value="{{ compra_a_editar.modelo if compra_a_editar else '' }}"></div>
                        <div class="col-md-3"><input type="text" name="presentacion" class="form-control" placeholder="Presentación (ej: Pieza)" value="{{ compra_a_editar.presentacion if compra_a_editar else '' }}"></div>
                        <div class="col-md-3"><input type="number" name="stock" class="form-control" placeholder="Stock Inicial" value="{{ compra_a_editar.stock if compra_a_editar else '' }}" required></div>
                        <div class="col-md-12"><input type="text" name="proveedor" class="form-control" placeholder="Proveedor" value="{{ compra_a_editar.proveedor if compra_a_editar else '' }}"></div>
                    </div>
                    <div class="mt-4 text-center">
                        <button type="submit" class="btn btn-custom-primary px-5">{% if compra_a_editar %}Actualizar{% else %}Añadir Producto{% endif %}</button>
                        {% if compra_a_editar %}<a href="{{ url_for('index') }}" class="btn btn-custom-secondary px-4 ms-2">Cancelar</a>{% endif %}
                    </div>
                </form>
            </div>
        </div>

        <div class="card card-custom mt-4">
            <div class="card-header card-header-custom d-flex justify-content-between align-items-center">
                <span>Historial de Inventario</span>
                <span class="badge bg-light text-dark">{{ compras|length }} productos</span>
            </div>
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-custom table-hover mb-0">
                        <thead>
                            <tr><th>ID</th><th>Nombre</th><th>Marca</th><th>Modelo</th><th>Presentación</th><th>Proveedor</th><th>Costo</th><th>Stock</th><th>Acciones</th></tr>
                        </thead>
                        <tbody>
                            {% for compra in compras %}
                            <tr>
                                <td><strong>{{ compra.id_compra }}</strong></td>
                                <td>{{ compra.nombre }}</td>
                                <td>{{ compra.marca }}</td>
                                <td>{{ compra.modelo }}</td>
                                <td>{{ compra.presentacion }}</td>
                                <td>{{ compra.proveedor }}</td>
                                <td>${{ "%.2f"|format(compra.unitario) }}</td>
                                <td>
                                    {% if compra.stock <= 10 %}<span class="badge bg-danger">{{ compra.stock }}</span>
                                    {% else %}<span class="badge bg-success">{{ compra.stock }}</span>{% endif %}
                                </td>
                                <td>
                                    <a href="{{ url_for('edit', compra_id=compra.id_compra) }}" class="btn btn-sm btn-custom-secondary">Editar</a>
                                    <form action="{{ url_for('delete', compra_id=compra.id_compra) }}" method="POST" class="d-inline" onsubmit="return confirm('¿Eliminar producto?');">
                                        <button type="submit" class="btn btn-sm btn-custom-danger">Eliminar</button>
                                    </form>
                                </td>
                            </tr>
                            {% else %}
                            <tr><td colspan="9" class="text-center py-4 text-muted">No hay productos.</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="card card-custom mt-4 mb-5">
            <div class="card-header card-header-custom">Ventas Recientes</div>
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-custom table-hover mb-0">
                        <thead><tr><th>ID Venta</th><th>Cliente (DNI)</th><th>Producto (Ref)</th><th>Cantidad</th><th>Monto Total</th><th>Fecha</th></tr></thead>
                        <tbody>
                            {% for venta in ventas %}
                            <tr>
                                <td>{{ venta.id_venta }}</td><td>{{ venta.cliente_dni }}</td><td>{{ venta.producto_ref }}</td>
                                <td>{{ venta.cantidad }}</td><td>${{ "%.2f"|format(venta.monto) }}</td>
                                <td>{{ venta.fecha.strftime('%Y-%m-%d %H:%M') if venta.fecha else '' }}</td>
                            </tr>
                            {% else %}
                            <tr><td colspan="6" class="text-center py-4 text-muted">No hay ventas registradas.</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal para Registrar Venta -->
    <div class="modal fade" id="ventaModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header" style="background-color: var(--color-5); color: white;">
                    <h5 class="modal-title">Registrar Nueva Venta</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form action="{{ url_for('add_sale') }}" method="POST">
                    <div class="modal-body">
                        <div class="mb-3"><label class="form-label">DNI del Cliente</label><input type="text" name="cliente_dni" class="form-control" required></div>
                        <div class="mb-3"><label class="form-label">ID o Nombre del Producto</label><input type="text" name="producto_ref" class="form-control" placeholder="Ej: P001" required></div>
                        <div class="mb-3"><label class="form-label">Cantidad</label><input type="number" name="cantidad" class="form-control" value="1" min="1" required></div>
                        <div class="mb-3"><label class="form-label">Monto Total ($)</label><input type="number" step="0.01" name="monto" class="form-control" required></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-custom-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-custom-primary">Registrar Venta</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

HTML_LOGIN = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Login - Papelería Torres</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #F4EFE9; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }
        .login-card { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 350px; }
        h2 { color: #A78470; text-align: center; margin-bottom: 30px; font-weight: bold; }
        .form-control { border: 1px solid #C9B6A8; margin-bottom: 15px; }
        .btn-custom { background: #A78470; color: white; width: 100%; border: none; padding: 10px; border-radius: 5px; font-weight: bold; }
        .btn-custom:hover { background: #B89A86; color: white; }
    </style>
</head>
<body>
    <div class="login-card">
        <h2>Papelería Torres</h2>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-danger p-2 text-center" style="font-size: 14px;">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST">
            <input type="text" name="username" class="form-control" placeholder="Usuario (admin)" required>
            <input type="password" name="password" class="form-control" placeholder="Contraseña (password)" required>
            <button type="submit" class="btn-custom mt-3">Ingresar</button>
        </form>
    </div>
</body>
</html>
"""

# ==============================================================================
# LÓGICA DE LA APLICACIÓN
# ==============================================================================

def convert_unitario_to_float(compras):
    if isinstance(compras, dict): compras_list = [compras]
    elif isinstance(compras, list): compras_list = compras
    else: return compras

    for compra in compras_list:
        if 'unitario' in compra:
            try: compra['unitario'] = float(compra['unitario'])
            except: compra['unitario'] = 0.0
        if 'monto' in compra:
            try: compra['monto'] = float(compra['monto'])
            except: compra['monto'] = 0.0
        if 'stock' in compra:
            try: compra['stock'] = int(compra['stock'])
            except: compra['stock'] = 0
    return compras_list[0] if isinstance(compras, dict) and compras_list else compras_list

def get_compra(id_compra):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM compras WHERE id_compra = %s", (id_compra,))
    compra = cursor.fetchone()
    cursor.close()
    return convert_unitario_to_float(compra) if compra else None

def get_ventas_list():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM ventas ORDER BY id_venta DESC")
        ventas = cursor.fetchall()
        cursor.close()
        return convert_unitario_to_float(ventas)
    except: return []

def inicializar_base_de_datos():
    with app.app_context():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id_compra VARCHAR(50) PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                marca VARCHAR(255),
                modelo VARCHAR(255),
                presentacion VARCHAR(255),
                proveedor VARCHAR(255),
                unitario DECIMAL(10,2) NOT NULL,
                stock INT NOT NULL DEFAULT 0
            )""")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id_venta INT AUTO_INCREMENT PRIMARY KEY,
                cliente_dni VARCHAR(255) NOT NULL,
                producto_ref VARCHAR(255) NOT NULL,
                cantidad INT NOT NULL DEFAULT 1,
                monto DECIMAL(10,2) NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            mysql.connection.commit()

            cursor.execute("SELECT COUNT(*) as total FROM compras")
            if cursor.fetchone()['total'] == 0:
                productos = [
                    ('P001', 'Cuaderno Profesional', 'Scribe', 'Raya 100 Hojas', 'Pieza', 'Distribuidora Escolar', 25.50, 50),
                    ('P002', 'Cuaderno Profesional', 'Scribe', 'Cuadro 100 Hojas', 'Pieza', 'Distribuidora Escolar', 25.50, 40),
                    ('P003', 'Bolígrafo Tinta Negra', 'Bic', 'Cristal', 'Pieza', 'Bic Mexico', 6.00, 100),
                    ('P004', 'Bolígrafo Tinta Azul', 'Bic', 'Cristal', 'Pieza', 'Bic Mexico', 6.00, 120),
                    ('P005', 'Bolígrafo Tinta Roja', 'Bic', 'Cristal', 'Pieza', 'Bic Mexico', 6.00, 80),
                    ('P006', 'Lápiz del No. 2', 'Dixon', 'Amarillo', 'Pieza', 'Lápices Unidos', 4.50, 150),
                    ('P007', 'Goma de Borrar', 'Pelikan', 'Blanca', 'Pieza', 'Pelikan', 5.00, 80),
                    ('P008', 'Sacapuntas Metálico', 'Maped', 'Doble Orificio', 'Pieza', 'Maped', 12.00, 40),
                    ('P009', 'Regla de 30 cm', 'Maped', 'Plástico', 'Pieza', 'Maped', 10.00, 35),
                    ('P010', 'Tijeras Escolares', 'Maped', 'Punta Roma', 'Pieza', 'Maped', 28.00, 30),
                    ('P011', 'Pegamento en Barra', 'Pritt', '21g', 'Pieza', 'Henkel', 18.00, 50),
                    ('P012', 'Pegamento Líquido', 'Resistol', '240ml', 'Pieza', 'Henkel', 35.00, 25),
                    ('P013', 'Marcatextos Amarillo', 'Sharpie', 'Fluorescente', 'Pieza', 'Sanford', 22.00, 60),
                    ('P014', 'Marcatextos Verde', 'Sharpie', 'Fluorescente', 'Pieza', 'Sanford', 22.00, 45),
                    ('P015', 'Marcatextos Rosa', 'Sharpie', 'Fluorescente', 'Pieza', 'Sanford', 22.00, 45),
                    ('P016', 'Caja de Colores', 'Norma', '12 Lápices', 'Caja', 'Norma', 45.00, 30),
                    ('P017', 'Caja de Colores', 'Norma', '24 Lápices', 'Caja', 'Norma', 85.00, 20),
                    ('P018', 'Plumón para Pizarrón', 'Pilot', 'Negro', 'Pieza', 'Pilot', 28.00, 40),
                    ('P019', 'Plumón para Pizarrón', 'Pilot', 'Azul', 'Pieza', 'Pilot', 28.00, 40),
                    ('P020', 'Corrector Líquido', 'Bic', '15ml', 'Pieza', 'Bic Mexico', 20.00, 50),
                    ('P021', 'Cinta Adhesiva', 'Scotch', 'Transparente', 'Pieza', '3M', 15.00, 70),
                    ('P022', 'Cinta Adhesiva', 'Scotch', 'Masking', 'Pieza', '3M', 22.00, 40),
                    ('P023', 'Post-it', '3M', 'Amarillo 3x3', 'Bloc', '3M', 35.00, 35),
                    ('P024', 'Clips Mariposa', 'ACCO', 'Caja 12 pzas', 'Caja', 'ACCO', 12.00, 60),
                    ('P025', 'Grapadora', 'Swingline', 'Escritorio', 'Pieza', 'Swingline', 85.00, 15),
                    ('P026', 'Caja de Grapas', 'Swingline', 'Estándar', 'Caja', 'Swingline', 15.00, 100),
                    ('P027', 'Perforadora', 'Maped', '2 Orificios', 'Pieza', 'Maped', 95.00, 12),
                    ('P028', 'Carpeta de Argollas', 'Leitz', '1 Pulgada', 'Pieza', 'Leitz', 65.00, 25),
                    ('P029', 'Carpeta de Argollas', 'Leitz', '2 Pulgadas', 'Pieza', 'Leitz', 85.00, 20),
                    ('P030', 'Fólder Tamaño Carta', 'Smead', 'Color Beige', 'Pieza', 'Smead', 12.00, 60),
                    ('P031', 'Fólder Tamaño Oficio', 'Smead', 'Color Beige', 'Pieza', 'Smead', 15.00, 50),
                    ('P032', 'Sobre Tamaño Carta', 'Office Depot', 'Blanco', 'Paquete 10', 'Office Depot', 25.00, 40),
                    ('P033', 'Block de Hojas Blancas', 'Scribe', 'Carta 100 Hojas', 'Bloc', 'Distribuidora Escolar', 30.00, 30),
                    ('P034', 'Libreta de Taquigrafía', 'Scribe', 'Espiral', 'Pieza', 'Distribuidora Escolar', 18.00, 45),
                    ('P035', 'Agenda 2024', 'Norma', 'Diaria', 'Pieza', 'Norma', 120.00, 10),
                    ('P036', 'Calculadora Básica', 'Casio', '8 Dígitos', 'Pieza', 'Casio', 150.00, 15),
                    ('P037', 'Calculadora Científica', 'Casio', 'fx-82MS', 'Pieza', 'Casio', 320.00, 8),
                    ('P038', 'Juego Geométrico', 'Maped', '4 Piezas', 'Juego', 'Maped', 40.00, 20),
                    ('P039', 'Transportador', 'Maped', '180 Grados', 'Pieza', 'Maped', 12.00, 30),
                    ('P040', 'Compás de Precisión', 'Maped', 'Metálico', 'Pieza', 'Maped', 55.00, 15),
                    ('P041', 'Mochila Escolar', 'Totto', 'Azul', 'Pieza', 'Totto', 450.00, 5),
                    ('P042', 'Mochila Escolar', 'Totto', 'Café', 'Pieza', 'Totto', 480.00, 5),
                    ('P043', 'Estuche Escolar', 'Totto', 'Doble Cierre', 'Pieza', 'Totto', 150.00, 10),
                    ('P044', 'Lonchera', 'Totto', 'Térmica', 'Pieza', 'Totto', 180.00, 8),
                    ('P045', 'Papel Bond', 'Scribe', 'Carta 500 Hojas', 'Paquete', 'Distribuidora Escolar', 120.00, 20),
                    ('P046', 'Papel Fotográfico', 'HP', 'Carta 50 Hojas', 'Paquete', 'HP', 180.00, 15),
                    ('P047', 'Tinta para Impresora', 'HP', 'Negra 664', 'Pieza', 'HP', 220.00, 12),
                    ('P048', 'Tinta para Impresora', 'HP', 'Color 664', 'Pieza', 'HP', 250.00, 10),
                    ('P049', 'Masking Tape', 'Tuk', '1 Pulgada', 'Pieza', 'Tuk', 18.00, 40),
                    ('P050', 'Gises de Colores', 'Crayola', 'Caja 12 pzas', 'Caja', 'Crayola', 25.00, 25)
                ]
                query = "INSERT INTO compras (id_compra, nombre, marca, modelo, presentacion, proveedor, unitario, stock) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(query, productos)
                mysql.connection.commit()
                print("✅ Base de datos inicializada con los 50 productos de Papelería Torres.")
            cursor.close()
        except Exception as e:
            print(f"⚠️ Error al inicializar BD (Verifica que la BD 'tiendita' exista): {e}")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Por favor, inicia sesión.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ----------------- Rutas -----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'password':
            session['logged_in'] = True
            session['username'] = 'admin'
            flash('¡Bienvenido a Papelería Torres!', 'success')
            return redirect(url_for('index'))
        flash('Credenciales inválidas.', 'error')
    return render_template_string(HTML_LOGIN)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM compras ORDER BY id_compra ASC")
        compras = convert_unitario_to_float(cursor.fetchall())
        cursor.close()
        return render_template_string(HTML_LAYOUT, compras=compras, ventas=get_ventas_list(), search_query=None, compra_a_editar=None)
    except Exception as e:
        return render_template_string(HTML_LAYOUT, error_msg=str(e), compras=[], ventas=[], search_query=None, compra_a_editar=None)

@app.route('/add', methods=['POST'])
@login_required
def add():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO compras VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       (request.form['id_compra'], request.form['nombre'], request.form['marca'], request.form['modelo'], 
                        request.form['presentacion'], request.form['proveedor'], float(request.form['unitario']), int(request.form.get('stock', 0))))
        mysql.connection.commit(); cursor.close()
        flash('Producto añadido.', 'success')
    except Exception as e: flash(f'Error: {e}', 'error')
    return redirect(url_for('index'))

@app.route('/edit/<string:compra_id>')
@login_required
def edit(compra_id):
    compra_a_editar = get_compra(compra_id)
    if not compra_a_editar:
        flash('No encontrado.', 'error')
        return redirect(url_for('index'))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM compras ORDER BY id_compra ASC")
    compras = convert_unitario_to_float(cursor.fetchall())
    cursor.close()
    return render_template_string(HTML_LAYOUT, compras=compras, ventas=get_ventas_list(), search_query=None, compra_a_editar=compra_a_editar)

@app.route('/update/<string:compra_id>', methods=['POST'])
@login_required
def update(compra_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE compras SET id_compra=%s, nombre=%s, marca=%s, modelo=%s, presentacion=%s, proveedor=%s, unitario=%s, stock=%s WHERE id_compra=%s",
                       (request.form['id_compra'], request.form['nombre'], request.form['marca'], request.form['modelo'], 
                        request.form['presentacion'], request.form['proveedor'], float(request.form['unitario']), int(request.form['stock']), compra_id))
        mysql.connection.commit(); cursor.close()
        flash('Actualizado.', 'success')
    except Exception as e: flash(f'Error: {e}', 'error')
    return redirect(url_for('index'))

@app.route('/delete/<string:compra_id>', methods=['POST'])
@login_required
def delete(compra_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM compras WHERE id_compra = %s", (compra_id,))
        mysql.connection.commit(); cursor.close()
        flash('Eliminado.', 'danger')
    except Exception as e: flash(f'Error: {e}', 'error')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
@login_required
def search():
    q = request.args.get('id_compra')
    if not q: return redirect(url_for('index'))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM compras WHERE id_compra = %s OR nombre LIKE %s", (q, f"%{q}%"))
    results = convert_unitario_to_float(cursor.fetchall())
    cursor.close()
    return render_template_string(HTML_LAYOUT, compras=results, ventas=get_ventas_list(), search_query=q, compra_a_editar=None)

@app.route('/add_sale', methods=['POST'])
@login_required
def add_sale():
    try:
        ref = request.form['producto_ref']
        cant = int(request.form['cantidad'])
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_compra, stock FROM compras WHERE id_compra = %s OR nombre = %s", (ref, ref))
        prod = cursor.fetchone()
        
        if prod:
            if int(prod['stock']) < cant:
                flash(f'Stock insuficiente. Solo hay {prod["stock"]}.', 'error')
                return redirect(url_for('index'))
            cursor.execute("UPDATE compras SET stock = stock - %s WHERE id_compra = %s", (cant, prod['id_compra']))
            
        cursor.execute("INSERT INTO ventas (cliente_dni, producto_ref, cantidad, monto) VALUES (%s, %s, %s, %s)",
                       (request.form['cliente_dni'], ref, cant, float(request.form['monto'])))
        mysql.connection.commit(); cursor.close()
        flash('Venta registrada.', 'success')
    except Exception as e: 
        mysql.connection.rollback()
        flash(f'Error al vender: {e}', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    inicializar_base_de_datos()
    app.run(host='0.0.0.0', port=5000, debug=True)