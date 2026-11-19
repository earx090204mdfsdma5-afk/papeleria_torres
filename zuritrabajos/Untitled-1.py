"""
=============================================================================
 SISTEMA DE CONTROL DE INVENTARIO
 Tecnologías: Python + SQLite + Tkinter
 Descripción: Aplicación CRUD para gestionar productos, compras, ventas
              e inventario de una pequeña empresa.
=============================================================================
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from contextlib import contextmanager

DB_NAME = "inventario.db"


# =============================================================================
# 1. CAPA DE BASE DE DATOS
# =============================================================================
def get_connection():
    """Devuelve una conexión SQLite con foreign keys activas y filas tipo dict."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def transaction():
    """Context manager para ejecutar operaciones dentro de una transacción."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def inicializar_bd():
    """Crea las tablas necesarias si no existen."""
    with transaction() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                categoria TEXT,
                precio_compra REAL NOT NULL DEFAULT 0 CHECK (precio_compra >= 0),
                precio_venta REAL NOT NULL DEFAULT 0 CHECK (precio_venta >= 0),
                stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
                stock_minimo INTEGER NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0),
                fecha_registro TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                precio_compra REAL NOT NULL CHECK (precio_compra >= 0),
                proveedor TEXT,
                fecha TEXT NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                precio_venta REAL NOT NULL CHECK (precio_venta >= 0),
                cliente TEXT,
                fecha TEXT NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS movimientos_inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK (tipo IN ('ENTRADA','SALIDA')),
                cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                referencia_id INTEGER,
                fecha TEXT NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
            )
        """)


# =============================================================================
# 2. MODELO / LÓGICA DE NEGOCIO
# =============================================================================
# ----------------------- PRODUCTOS -----------------------
def crear_producto(codigo, nombre, descripcion, categoria,
                   precio_compra, precio_venta, stock, stock_minimo):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with transaction() as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO productos
                (codigo, nombre, descripcion, categoria, precio_compra,
                 precio_venta, stock, stock_minimo, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (codigo, nombre, descripcion, categoria,
                  precio_compra, precio_venta, stock, stock_minimo, fecha))
            return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe un producto con ese código.")


def listar_productos():
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM productos ORDER BY id DESC").fetchall()
    finally:
        conn.close()


def buscar_productos(texto):
    conn = get_connection()
    try:
        patron = f"%{texto}%"
        return conn.execute("""
            SELECT * FROM productos
            WHERE nombre LIKE ? OR codigo LIKE ? OR categoria LIKE ?
            ORDER BY id DESC
        """, (patron, patron, patron)).fetchall()
    finally:
        conn.close()


def obtener_producto(pid):
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM productos WHERE id = ?", (pid,)).fetchone()
    finally:
        conn.close()


def actualizar_producto(pid, codigo, nombre, descripcion, categoria,
                        precio_compra, precio_venta, stock_minimo):
    with transaction() as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE productos
                SET codigo=?, nombre=?, descripcion=?, categoria=?,
                    precio_compra=?, precio_venta=?, stock_minimo=?
                WHERE id=?
            """, (codigo, nombre, descripcion, categoria,
                  precio_compra, precio_venta, stock_minimo, pid))
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe otro producto con ese código.")


def eliminar_producto(pid):
    with transaction() as conn:
        conn.execute("DELETE FROM productos WHERE id = ?", (pid,))


# ----------------------- COMPRAS -----------------------
def registrar_compra(producto_id, cantidad, precio_compra, proveedor=""):
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero.")
    if precio_compra < 0:
        raise ValueError("El precio no puede ser negativo.")

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with transaction() as conn:
        cur = conn.cursor()
        prod = cur.execute("SELECT id FROM productos WHERE id = ?",
                           (producto_id,)).fetchone()
        if not prod:
            raise ValueError("El producto no existe.")

        cur.execute("""
            INSERT INTO compras (producto_id, cantidad, precio_compra, proveedor, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (producto_id, cantidad, precio_compra, proveedor, fecha))
        compra_id = cur.lastrowid

        cur.execute("UPDATE productos SET stock = stock + ? WHERE id = ?",
                    (cantidad, producto_id))

        cur.execute("""
            INSERT INTO movimientos_inventario
            (producto_id, tipo, cantidad, referencia_id, fecha)
            VALUES (?, 'ENTRADA', ?, ?, ?)
        """, (producto_id, cantidad, compra_id, fecha))

        return compra_id


# ----------------------- VENTAS -----------------------
def registrar_venta(producto_id, cantidad, precio_venta, cliente=""):
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero.")
    if precio_venta < 0:
        raise ValueError("El precio no puede ser negativo.")

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with transaction() as conn:
        cur = conn.cursor()
        prod = cur.execute("SELECT stock, nombre FROM productos WHERE id = ?",
                           (producto_id,)).fetchone()
        if not prod:
            raise ValueError("El producto no existe.")
        if prod["stock"] < cantidad:
            raise ValueError(
                f"Stock insuficiente. Disponible: {prod['stock']}, "
                f"solicitado: {cantidad}."
            )

        cur.execute("""
            INSERT INTO ventas (producto_id, cantidad, precio_venta, cliente, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (producto_id, cantidad, precio_venta, cliente, fecha))
        venta_id = cur.lastrowid

        cur.execute("UPDATE productos SET stock = stock - ? WHERE id = ?",
                    (cantidad, producto_id))

        cur.execute("""
            INSERT INTO movimientos_inventario
            (producto_id, tipo, cantidad, referencia_id, fecha)
            VALUES (?, 'SALIDA', ?, ?, ?)
        """, (producto_id, cantidad, venta_id, fecha))

        return venta_id


# ----------------------- CONSULTAS -----------------------
def inventario_total():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT
                COUNT(*) AS total_productos,
                COALESCE(SUM(stock), 0) AS total_unidades,
                COALESCE(SUM(stock * precio_compra), 0) AS valor_compra,
                COALESCE(SUM(stock * precio_venta), 0) AS valor_venta
            FROM productos
        """).fetchone()
    finally:
        conn.close()


def productos_stock_bajo():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT * FROM productos
            WHERE stock > 0 AND stock <= stock_minimo
            ORDER BY stock ASC
        """).fetchall()
    finally:
        conn.close()


def productos_sin_stock():
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM productos WHERE stock = 0").fetchall()
    finally:
        conn.close()


def historial_movimientos(limite=300):
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT m.id, p.codigo, p.nombre, m.tipo, m.cantidad, m.fecha
            FROM movimientos_inventario m
            JOIN productos p ON p.id = m.producto_id
            ORDER BY m.id DESC
            LIMIT ?
        """, (limite,)).fetchall()
    finally:
        conn.close()


def historial_compras():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT c.id, p.codigo, p.nombre, c.cantidad, c.precio_compra,
                   c.proveedor, c.fecha
            FROM compras c
            JOIN productos p ON p.id = c.producto_id
            ORDER BY c.id DESC
        """).fetchall()
    finally:
        conn.close()


def historial_ventas():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT v.id, p.codigo, p.nombre, v.cantidad, v.precio_venta,
                   v.cliente, v.fecha
            FROM ventas v
            JOIN productos p ON p.id = v.producto_id
            ORDER BY v.id DESC
        """).fetchall()
    finally:
        conn.close()


# =============================================================================
# 3. VALIDACIONES
# =============================================================================
def _float(valor, campo):
    try:
        v = float(valor)
    except ValueError:
        raise ValueError(f"El campo '{campo}' debe ser un número.")
    if v < 0:
        raise ValueError(f"El campo '{campo}' no puede ser negativo.")
    return v


def _int(valor, campo, permitir_cero=True):
    try:
        v = int(valor)
    except ValueError:
        raise ValueError(f"El campo '{campo}' debe ser un número entero.")
    if v < 0 or (not permitir_cero and v == 0):
        raise ValueError(f"El campo '{campo}' no es válido.")
    return v


# =============================================================================
# 4. INTERFAZ GRÁFICA
# =============================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventario")
        self.geometry("1150x680")
        self.configure(bg="#f0f0f0")
        self.minsize(950, 600)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TNotebook.Tab", padding=[15, 8], font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=24, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_productos = ProductosFrame(self.notebook)
        self.frame_compras = ComprasFrame(self.notebook)
        self.frame_ventas = VentasFrame(self.notebook)
        self.frame_inventario = InventarioFrame(self.notebook)
        self.frame_historial = HistorialFrame(self.notebook)

        self.notebook.add(self.frame_productos, text="📦 Productos")
        self.notebook.add(self.frame_compras, text="🛒 Compras")
        self.notebook.add(self.frame_ventas, text="💰 Ventas")
        self.notebook.add(self.frame_inventario, text="📊 Inventario")
        self.notebook.add(self.frame_historial, text="🕓 Movimientos")

        # Refresca automáticamente al cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, _):
        try:
            idx = self.notebook.index(self.notebook.select())
            if idx == 1:
                self.frame_compras.refrescar()
            elif idx == 2:
                self.frame_ventas.refrescar()
            elif idx == 3:
                self.frame_inventario.actualizar()
            elif idx == 4:
                self.frame_historial.cargar()
        except Exception:
            pass


# ----------------------- MÓDULO PRODUCTOS -----------------------
class ProductosFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.producto_seleccionado = None
        self._construir()
        self.cargar()

    def _construir(self):
        form = ttk.LabelFrame(self, text="Datos del producto", padding=10)
        form.pack(fill="x")

        self.vars = {k: tk.StringVar() for k in
                     ["codigo", "nombre", "descripcion", "categoria",
                      "precio_compra", "precio_venta", "stock", "stock_minimo"]}

        campos = [
            ("Código/SKU *", "codigo", 0, 0),
            ("Nombre *", "nombre", 0, 2),
            ("Categoría", "categoria", 0, 4),
            ("Precio compra *", "precio_compra", 1, 0),
            ("Precio venta *", "precio_venta", 1, 2),
            ("Stock inicial", "stock", 1, 4),
            ("Stock mínimo", "stock_minimo", 2, 0),
            ("Descripción", "descripcion", 2, 2),
        ]
        for label, key, r, c in campos:
            ttk.Label(form, text=label).grid(row=r, column=c, sticky="w", padx=5, pady=3)
            ttk.Entry(form, textvariable=self.vars[key], width=22)\
                .grid(row=r, column=c + 1, padx=5, pady=3, sticky="w")

        botones = ttk.Frame(form)
        botones.grid(row=3, column=0, columnspan=6, pady=10, sticky="w")
        ttk.Button(botones, text="➕ Agregar", command=self.agregar).pack(side="left", padx=3)
        ttk.Button(botones, text="✏️ Actualizar", command=self.actualizar).pack(side="left", padx=3)
        ttk.Button(botones, text="🗑️ Eliminar", command=self.eliminar).pack(side="left", padx=3)
        ttk.Button(botones, text="🧹 Limpiar", command=self.limpiar).pack(side="left", padx=3)

        busq = ttk.Frame(self)
        busq.pack(fill="x", pady=8)
        ttk.Label(busq, text="Buscar:").pack(side="left")
        self.busqueda_var = tk.StringVar()
        ttk.Entry(busq, textvariable=self.busqueda_var, width=40).pack(side="left", padx=5)
        ttk.Button(busq, text="🔍 Buscar", command=self.buscar).pack(side="left", padx=3)
        ttk.Button(busq, text="Mostrar todos", command=self.cargar).pack(side="left", padx=3)

        cols = ("id", "codigo", "nombre", "categoria", "precio_compra",
                "precio_venta", "stock", "stock_minimo")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=14)
        for c in cols:
            self.tabla.heading(c, text=c.replace("_", " ").title())
            self.tabla.column(c, width=115, anchor="center")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def _leer_form(self):
        codigo = self.vars["codigo"].get().strip()
        nombre = self.vars["nombre"].get().strip()
        if not codigo or not nombre:
            raise ValueError("Código y Nombre son obligatorios.")
        descripcion = self.vars["descripcion"].get().strip()
        categoria = self.vars["categoria"].get().strip()
        pc = _float(self.vars["precio_compra"].get() or 0, "precio de compra")
        pv = _float(self.vars["precio_venta"].get() or 0, "precio de venta")
        stock = _int(self.vars["stock"].get() or 0, "stock")
        smin = _int(self.vars["stock_minimo"].get() or 0, "stock mínimo")
        return codigo, nombre, descripcion, categoria, pc, pv, stock, smin

    def agregar(self):
        try:
            datos = self._leer_form()
            crear_producto(*datos)
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            self.limpiar()
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        if not self.producto_seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla.")
            return
        try:
            codigo, nombre, descripcion, categoria, pc, pv, _stock, smin = self._leer_form()
            actualizar_producto(self.producto_seleccionado, codigo, nombre,
                                descripcion, categoria, pc, pv, smin)
            messagebox.showinfo("Éxito", "Producto actualizado.")
            self.limpiar()
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        if not self.producto_seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return
        if not messagebox.askyesno(
                "Confirmar",
                "¿Seguro que deseas eliminar este producto?\n"
                "Se eliminarán también sus compras, ventas y movimientos."):
            return
        try:
            eliminar_producto(self.producto_seleccionado)
            messagebox.showinfo("Éxito", "Producto eliminado.")
            self.limpiar()
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar(self):
        for v in self.vars.values():
            v.set("")
        self.producto_seleccionado = None
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)

    def cargar(self):
        self._llenar(listar_productos())

    def buscar(self):
        texto = self.busqueda_var.get().strip()
        if not texto:
            self.cargar()
            return
        self._llenar(buscar_productos(texto))

    def _llenar(self, filas):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for f in filas:
            self.tabla.insert("", "end", values=(
                f["id"], f["codigo"], f["nombre"], f["categoria"] or "",
                f["precio_compra"], f["precio_venta"], f["stock"], f["stock_minimo"]
            ))

    def seleccionar(self, _):
        sel = self.tabla.selection()
        if not sel:
            return
        vals = self.tabla.item(sel[0], "values")
        self.producto_seleccionado = int(vals[0])
        prod = obtener_producto(self.producto_seleccionado)
        if prod:
            self.vars["codigo"].set(prod["codigo"])
            self.vars["nombre"].set(prod["nombre"])
            self.vars["descripcion"].set(prod["descripcion"] or "")
            self.vars["categoria"].set(prod["categoria"] or "")
            self.vars["precio_compra"].set(str(prod["precio_compra"]))
            self.vars["precio_venta"].set(str(prod["precio_venta"]))
            self.vars["stock"].set(str(prod["stock"]))
            self.vars["stock_minimo"].set(str(prod["stock_minimo"]))


# ----------------------- MÓDULO COMPRAS -----------------------
class ComprasFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._construir()
        self.refrescar()

    def _construir(self):
        form = ttk.LabelFrame(self, text="Registrar compra (Entrada de mercancía)", padding=10)
        form.pack(fill="x")

        self.prod_var = tk.StringVar()
        self.cant_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.prov_var = tk.StringVar()

        ttk.Label(form, text="Producto *").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo = ttk.Combobox(form, textvariable=self.prod_var, width=50, state="readonly")
        self.combo.grid(row=0, column=1, padx=5, pady=5)
        self.combo.bind("<<ComboboxSelected>>", self._autocompletar_precio)

        ttk.Button(form, text="🔄 Actualizar lista",
                   command=self.refrescar).grid(row=0, column=2, padx=5)

        ttk.Label(form, text="Cantidad *").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.cant_var, width=20).grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(form, text="Precio compra *").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.precio_var, width=20).grid(row=2, column=1, sticky="w", padx=5)

        ttk.Label(form, text="Proveedor").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.prov_var, width=35).grid(row=3, column=1, sticky="w", padx=5)

        ttk.Button(form, text="📥 Registrar compra", command=self.registrar).grid(
            row=4, column=0, columnspan=2, pady=10)

        hist = ttk.LabelFrame(self, text="Historial de compras", padding=10)
        hist.pack(fill="both", expand=True, pady=10)

        cols = ("id", "codigo", "nombre", "cantidad", "precio_compra", "proveedor", "fecha")
        self.tabla = ttk.Treeview(hist, columns=cols, show="headings", height=12)
        for c in cols:
            self.tabla.heading(c, text=c.replace("_", " ").title())
            self.tabla.column(c, width=140, anchor="center")
        self.tabla.pack(fill="both", expand=True)

    def refrescar(self):
        """Recarga productos del combo y el historial."""
        self.cargar_productos()
        self.cargar_historial()

    def cargar_productos(self):
        self.productos = listar_productos()
        opciones = [
            f"{p['id']} - {p['codigo']} - {p['nombre']} (stock: {p['stock']})"
            for p in self.productos
        ]
        self.combo["values"] = opciones
        if self.prod_var.get() and self.prod_var.get() not in opciones:
            self.prod_var.set("")

    def _autocompletar_precio(self, _):
        try:
            pid = int(self.prod_var.get().split(" - ")[0])
            prod = obtener_producto(pid)
            if prod:
                self.precio_var.set(str(prod["precio_compra"]))
        except Exception:
            pass

    def registrar(self):
        try:
            if not self.prod_var.get():
                raise ValueError("Selecciona un producto.")
            pid = int(self.prod_var.get().split(" - ")[0])
            cantidad = _int(self.cant_var.get(), "cantidad", permitir_cero=False)
            precio = _float(self.precio_var.get(), "precio de compra")
            proveedor = self.prov_var.get().strip()

            registrar_compra(pid, cantidad, precio, proveedor)
            messagebox.showinfo("Éxito", "Compra registrada. Stock actualizado.")
            self.cant_var.set("")
            self.prov_var.set("")
            self.refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_historial(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for f in historial_compras():
            self.tabla.insert("", "end", values=(
                f["id"], f["codigo"], f["nombre"], f["cantidad"],
                f["precio_compra"], f["proveedor"] or "", f["fecha"]
            ))


# ----------------------- MÓDULO VENTAS -----------------------
class VentasFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._construir()
        self.refrescar()

    def _construir(self):
        form = ttk.LabelFrame(self, text="Registrar venta (Salida de mercancía)", padding=10)
        form.pack(fill="x")

        self.prod_var = tk.StringVar()
        self.cant_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.cli_var = tk.StringVar()

        ttk.Label(form, text="Producto *").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo = ttk.Combobox(form, textvariable=self.prod_var, width=50, state="readonly")
        self.combo.grid(row=0, column=1, padx=5, pady=5)
        self.combo.bind("<<ComboboxSelected>>", self._autocompletar_precio)

        ttk.Button(form, text="🔄 Actualizar lista",
                   command=self.refrescar).grid(row=0, column=2, padx=5)

        ttk.Label(form, text="Cantidad *").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.cant_var, width=20).grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(form, text="Precio venta *").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.precio_var, width=20).grid(row=2, column=1, sticky="w", padx=5)

        ttk.Label(form, text="Cliente").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.cli_var, width=35).grid(row=3, column=1, sticky="w", padx=5)

        ttk.Button(form, text="📤 Registrar venta", command=self.registrar).grid(
            row=4, column=0, columnspan=2, pady=10)

        hist = ttk.LabelFrame(self, text="Historial de ventas", padding=10)
        hist.pack(fill="both", expand=True, pady=10)

        cols = ("id", "codigo", "nombre", "cantidad", "precio_venta", "cliente", "fecha")
        self.tabla = ttk.Treeview(hist, columns=cols, show="headings", height=12)
        for c in cols:
            self.tabla.heading(c, text=c.replace("_", " ").title())
            self.tabla.column(c, width=140, anchor="center")
        self.tabla.pack(fill="both", expand=True)

    def refrescar(self):
        self.cargar_productos()
        self.cargar_historial()

    def cargar_productos(self):
        self.productos = listar_productos()
        opciones = [
            f"{p['id']} - {p['codigo']} - {p['nombre']} (stock: {p['stock']})"
            for p in self.productos
        ]
        self.combo["values"] = opciones
        if self.prod_var.get() and self.prod_var.get() not in opciones:
            self.prod_var.set("")

    def _autocompletar_precio(self, _):
        try:
            pid = int(self.prod_var.get().split(" - ")[0])
            prod = obtener_producto(pid)
            if prod:
                self.precio_var.set(str(prod["precio_venta"]))
        except Exception:
            pass

    def registrar(self):
        try:
            if not self.prod_var.get():
                raise ValueError("Selecciona un producto.")
            pid = int(self.prod_var.get().split(" - ")[0])
            cantidad = _int(self.cant_var.get(), "cantidad", permitir_cero=False)
            precio = _float(self.precio_var.get(), "precio de venta")
            cliente = self.cli_var.get().strip()

            registrar_venta(pid, cantidad, precio, cliente)
            messagebox.showinfo("Éxito", "Venta registrada. Stock actualizado.")
            self.cant_var.set("")
            self.cli_var.set("")
            self.refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_historial(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for f in historial_ventas():
            self.tabla.insert("", "end", values=(
                f["id"], f["codigo"], f["nombre"], f["cantidad"],
                f["precio_venta"], f["cliente"] or "", f["fecha"]
            ))


# ----------------------- MÓDULO INVENTARIO -----------------------
class InventarioFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._construir()
        self.actualizar()

    def _construir(self):
        top = ttk.Frame(self)
        top.pack(fill="x")
        ttk.Button(top, text="🔄 Actualizar", command=self.actualizar).pack(side="left")

        self.resumen = ttk.LabelFrame(self, text="Resumen del inventario", padding=10)
        self.resumen.pack(fill="x", pady=10)
        self.lbl_resumen = ttk.Label(self.resumen, text="", font=("Segoe UI", 11))
        self.lbl_resumen.pack(anchor="w")

        bajo = ttk.LabelFrame(self, text="⚠️ Productos con stock bajo", padding=10)
        bajo.pack(fill="both", expand=True, pady=5)
        cols = ("id", "codigo", "nombre", "stock", "stock_minimo")
        self.tabla_bajo = ttk.Treeview(bajo, columns=cols, show="headings", height=6)
        for c in cols:
            self.tabla_bajo.heading(c, text=c.title())
            self.tabla_bajo.column(c, width=140, anchor="center")
        self.tabla_bajo.pack(fill="both", expand=True)

        sin = ttk.LabelFrame(self, text="🚫 Productos sin existencias", padding=10)
        sin.pack(fill="both", expand=True, pady=5)
        cols2 = ("id", "codigo", "nombre", "categoria")
        self.tabla_sin = ttk.Treeview(sin, columns=cols2, show="headings", height=6)
        for c in cols2:
            self.tabla_sin.heading(c, text=c.title())
            self.tabla_sin.column(c, width=160, anchor="center")
        self.tabla_sin.pack(fill="both", expand=True)

    def actualizar(self):
        r = inventario_total()
        texto = (
            f"📦 Total de productos registrados: {r['total_productos']}\n"
            f"🔢 Total de unidades en stock: {r['total_unidades']}\n"
            f"💵 Valor del inventario (precio compra): ${r['valor_compra']:.2f}\n"
            f"💲 Valor potencial de venta: ${r['valor_venta']:.2f}"
        )
        self.lbl_resumen.config(text=texto)

        for i in self.tabla_bajo.get_children():
            self.tabla_bajo.delete(i)
        for f in productos_stock_bajo():
            self.tabla_bajo.insert("", "end", values=(
                f["id"], f["codigo"], f["nombre"], f["stock"], f["stock_minimo"]
            ))

        for i in self.tabla_sin.get_children():
            self.tabla_sin.delete(i)
        for f in productos_sin_stock():
            self.tabla_sin.insert("", "end", values=(
                f["id"], f["codigo"], f["nombre"], f["categoria"] or ""
            ))


# ----------------------- MÓDULO HISTORIAL -----------------------
class HistorialFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._construir()
        self.cargar()

    def _construir(self):
        top = ttk.Frame(self)
        top.pack(fill="x")
        ttk.Button(top, text="🔄 Actualizar", command=self.cargar).pack(side="left")

        hist = ttk.LabelFrame(self, text="Historial de movimientos de inventario", padding=10)
        hist.pack(fill="both", expand=True, pady=10)

        cols = ("id", "codigo", "nombre", "tipo", "cantidad", "fecha")
        self.tabla = ttk.Treeview(hist, columns=cols, show="headings", height=20)
        for c in cols:
            self.tabla.heading(c, text=c.replace("_", " ").title())
            self.tabla.column(c, width=170, anchor="center")
        self.tabla.pack(fill="both", expand=True)

    def cargar(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for f in historial_movimientos():
            self.tabla.insert("", "end", values=(
                f["id"], f["codigo"], f["nombre"], f["tipo"], f["cantidad"], f["fecha"]
            ))


# =============================================================================
# 5. PUNTO DE ENTRADA
# =============================================================================
def main():
    inicializar_bd()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()