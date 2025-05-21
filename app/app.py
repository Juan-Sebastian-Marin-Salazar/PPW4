from flask import Flask
from flask import request, redirect, url_for, render_template, flash, abort
from flask_mysqldb import MySQL
from app.config import DevelopmentConfig
from app.models.ModelUsers import ModelUsers
from app.models.entities.users import User
from app.models.modelOrders import ModelOrders
from flask_login import LoginManager, login_user, logout_user,login_required,current_user
from functools import wraps
from app.models.modelOrders import ModelOrders



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = MySQL(app)
login_manager_app = LoginManager(app)

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.usertype != 2:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view

def worker_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not (current_user.usertype == 1 or current_user.usertype == 2) :
            abort(403)
        return func(*args, **kwargs)
    return decorated_view

@app.route("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(0, request.form['email'], request.form['password'], None, 0)
        logged_user = ModelUsers.login(db, user)
        if logged_user is not None:
            login_user(logged_user)
            return redirect(url_for("index"))
        flash("Acceso rechazado...")
    return render_template("auth/login.html")



@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Validar campos obligatorios
            if not all([request.form.get('email'), request.form.get('password'), request.form.get('fullname')]):
                flash("Todos los campos son obligatorios")
                return redirect(url_for('register'))
            
            existe = ModelUsers.get_by_email(db, request.form.get('email'))
            if existe:
                flash("El correo ya está registrado")
                return redirect(url_for('login'))
                
            # Crear nuevo usuario
            new_user = User(
                id=None,  # El ID será autoincremental
                email=request.form['email'],
                password=request.form['password'],  # Se hasheará en ModelUsers
                fullname=request.form['fullname'],
                usertype=0  # 0 para usuario normal
            )
            
            # Registrar el usuario
            registered = ModelUsers.register(db, new_user)
            if registered:
                flash("¡Registro exitoso! Por favor inicia sesión")
                return redirect(url_for('login'))
            else:
                flash("Error al registrar el usuario")
                
        except Exception as e:
            flash(f"Error en el registro: {str(e)}")

    
    return render_template("auth/register.html")
    


@app.route("/index")
@login_required
def index():
    return (render_template("user/index.html"))


@app.route("/perfil/<int:id>" , methods=['GET', 'POST'])
@login_required
def perfil(id):
    
    user = ModelUsers.get_by_id(db, id)
    if user is None:
        flash("Usuario no encontrado")
        return redirect(url_for('index'))
    
    # Si el usuario es el mismo que está logueado, permitir editar
    if current_user.id == id or current_user.usertype == 2:
        # Renderizar plantilla con datos del usuario
        return render_template("user/perfil.html", user=user)
    
    else:
        flash("No tienes permiso para editar este perfil")
        return redirect(url_for('index'))

@app.route("/perfil/edit_perfil/<int:id>" , methods=['GET', 'POST'])
@login_required
def edit_perfil(id):
    if request.method == 'POST':
        try:
            # Validar campos obligatorios
            if not all([request.form.get('email'), request.form.get('fullname'), request.form.get('password')]):
                flash("Todos los campos son obligatorios")
                return redirect(url_for('perfil'))
            # Actualizar usuario
            current_user.email = request.form['email']
            current_user.fullname = request.form['fullname']
            current_user.password = request.form['password']
            
            print(f"{current_user.id},{current_user.email}, {current_user.fullname}, {current_user.password}, {current_user.usertype}")
            # Guardar cambios en la base de datos
            ModelUsers.update(db, current_user)
            
            return redirect(url_for('logout'))
            
        except Exception as e:
            flash(f"Error al actualizar el perfil: {str(e)}")
            return redirect(url_for('perfil', id=current_user.id))
    
    user = ModelUsers.get_by_id(db, id)
    if user is None:
        flash("Usuario no encontrado")
        return redirect(url_for('index'))
    
    # Si el usuario es el mismo que está logueado, permitir editar
    if current_user.id == id or current_user.usertype == 2:
        # Renderizar plantilla con datos del usuario
        return render_template("user/edit_perfil.html", user=user)
    else:
        flash("No tienes permiso para editar este perfil")
        return redirect(url_for('index'))


@login_required
@app.route('/delete_user')
def delete_user():
    ModelUsers.delete(db, current_user)
    return redirect(url_for('logout'))


@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


#dishes
@app.route('/menu')
@login_required
def menu():
    cursor = db.connection.cursor()
    cursor.execute('''
        SELECT d.id, d.name, d.descr, d.price, d.image, c.name AS category 
        FROM dishes d
        JOIN categories c ON d.category_id = c.id
    ''')
    dishes = cursor.fetchall()
    cursor.close()

    # Transformar a lista de diccionarios
    dish_list = []
    for dish in dishes:
        dish_list.append({
            'id': dish[0],
            'name': dish[1],
            'desc': dish[2],
            'price': dish[3],
            'image': dish[4],
            'category': dish[5]
        })

    return render_template('user/menu.html', dishes=dish_list)


@app.route('/admin/crear_platillo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_platillo():
    cursor = db.connection.cursor()
    
    # Obtener categorías para el formulario
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']
        image = request.form['image']
        category_id = request.form['category_id']

        cursor.execute('''
            INSERT INTO dishes (name, descr, price, image, category_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, desc, price, image, category_id))
        db.connection.commit()
        cursor.close()
        return redirect(url_for('menu'))
    
    cursor.close()
    return render_template('admin/create_dish.html', categories=categories)


@app.route('/admin/edit_dish/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_dish(id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    
    cursor.execute("SELECT * FROM dishes WHERE id = %s", (id,))
    dish = cursor.fetchone()

    if not dish:
        abort(404)

    if request.method == 'POST':
        name = request.form['name']
        descr = request.form['desc']
        price = request.form['price']
        image = request.form['image']
        category_id = request.form['category_id']

        cursor.execute('''
            UPDATE dishes
            SET name=%s, descr=%s, price=%s, image=%s, category_id=%s
            WHERE id=%s
        ''', (name, descr, price, image, category_id, id))
        db.connection.commit()
        cursor.close()
        return redirect(url_for('menu'))

    cursor.close()
    return render_template('admin/edit_dish.html', dish=dish, categories=categories)



@app.route('/admin/delete_dish/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_dish(id):
    if request.method == 'POST':
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM dishes WHERE id = %s", (id,))
        db.connection.commit()
        cursor.close()
        return redirect(url_for('menu'))


@app.route('/add_cart/<int:dish_id>', methods=['POST'])
@login_required
def add_cart(dish_id):
    cantidad = int(request.form['cantidad'])

    cursor = db.connection.cursor()

    # Verifica si el usuario ya tiene un carrito activo (active = 1)
    cursor.execute("""
        SELECT id FROM carts 
        WHERE user_id = %s AND active = 1
    """, (current_user.id,))
    carrito = cursor.fetchone()

    # Si no tiene, crea uno
    if not carrito:
        cursor.execute("""
            INSERT INTO carts (user_id, created_at, active) 
            VALUES (%s, CURRENT_TIMESTAMP, 1)
        """, (current_user.id,))
        db.connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        carrito_id = cursor.fetchone()[0]
    else:
        carrito_id = carrito[0]

    # Verifica si el platillo ya está en el carrito
    cursor.execute("""
        SELECT id FROM cart_items 
        WHERE cart_id = %s AND dish_id = %s
    """, (carrito_id, dish_id))
    item_existente = cursor.fetchone()

    if item_existente:
        # Si ya existe, actualiza la cantidad
        cursor.execute("""
            UPDATE cart_items 
            SET quantity = quantity + %s 
            WHERE id = %s
        """, (cantidad, item_existente[0]))
    else:
        # Si no existe, agrega nuevo item
        cursor.execute("""
            INSERT INTO cart_items (cart_id, dish_id, quantity)
            VALUES (%s, %s, %s)
        """, (carrito_id, dish_id, cantidad))
    
    db.connection.commit()
    cursor.close()
    return redirect(url_for('menu'))



@app.route('/ver_carrito')
@login_required
def ver_carrito():
    cursor = db.connection.cursor()
    
    # Obtener el carrito activo del usuario
    cursor.execute("""
        SELECT id FROM carts 
        WHERE user_id = %s AND active = 1
    """, (current_user.id,))
    carrito = cursor.fetchone()
    
    items_carrito = []
    total = 0.0
    
    if carrito:
        carrito_id = carrito[0]
        # Obtener los items del carrito con detalles del platillo
        cursor.execute("""
            SELECT ci.id, ci.dish_id, d.name, d.descr, d.price, ci.quantity, 
                   (d.price * ci.quantity) as subtotal
            FROM cart_items ci
            JOIN dishes d ON ci.dish_id = d.id
            WHERE ci.cart_id = %s
        """, (carrito_id,))
        items_carrito = cursor.fetchall()
        
        # Calcular el total
        cursor.execute("""
            SELECT SUM(d.price * ci.quantity) as total
            FROM cart_items ci
            JOIN dishes d ON ci.dish_id = d.id
            WHERE ci.cart_id = %s
        """, (carrito_id,))
        total_result = cursor.fetchone()
        total = total_result[0] if total_result[0] else 0.0
    
    cursor.close()
    return render_template('user/carrito.html', items=items_carrito, total=total)


@app.route('/eliminar_del_carrito/<int:item_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(item_id):
    cursor = db.connection.cursor()
    
    # Verificar que el item pertenece al usuario actual
    cursor.execute("""
        DELETE ci FROM cart_items ci
        JOIN carts c ON ci.cart_id = c.id
        WHERE ci.id = %s AND c.user_id = %s
    """, (item_id, current_user.id))
    
    db.connection.commit()
    cursor.close()
    flash("Item eliminado del carrito")
    return redirect(url_for('ver_carrito'))

@app.route('/actualizar_cantidad/<int:item_id>', methods=['POST'])
@login_required
def actualizar_cantidad(item_id):
    nueva_cantidad = int(request.form['cantidad'])
    
    if nueva_cantidad < 1:
        flash("La cantidad debe ser al menos 1", "error")
        return redirect(url_for('ver_carrito'))
    
    cursor = db.connection.cursor()
    
    # Verificar que el item pertenece al usuario actual
    cursor.execute("""
        UPDATE cart_items ci
        JOIN carts c ON ci.cart_id = c.id
        SET ci.quantity = %s
        WHERE ci.id = %s AND c.user_id = %s
    """, (nueva_cantidad, item_id, current_user.id))
    
    db.connection.commit()
    cursor.close()
    flash("Cantidad actualizada")
    return redirect(url_for('ver_carrito'))

@app.route('/checkout')
@login_required
def checkout():
    cursor = db.connection.cursor()
    
    try:
        # 1. Obtener el carrito activo del usuario
        cursor.execute("""
            SELECT id FROM carts 
            WHERE user_id = %s AND active = 1
            LIMIT 1
        """, (current_user.id,))
        carrito = cursor.fetchone()
        
        if not carrito:
            flash("No tienes un carrito activo", "warning")
            return redirect(url_for('ver_carrito'))
            
        carrito_id = carrito[0]
        
        # 2. Calcular el total del carrito (CORREGIDO: usando dishes)
        cursor.execute("""
            SELECT SUM(d.price * ci.quantity) 
            FROM cart_items ci
            JOIN dishes d ON ci.dish_id = d.id
            WHERE ci.cart_id = %s
        """, (carrito_id,))
        total = cursor.fetchone()[0] or 0.00
        
        # 3. Crear el pedido en la tabla orders
        cursor.execute("""
            INSERT INTO orders (owner_id, cost, delivered)
            VALUES (%s, %s, %s)
        """, (current_user.id, total, False))
        db.connection.commit()
        
        cursor.execute("""
            UPDATE carts 
            SET active = 0 
            WHERE id = %s
        """, (carrito_id,))
        
        db.connection.commit()
        flash("Pedido realizado con éxito!", "success")
    
    except Exception as e:
        db.connection.rollback()
        flash(f"Error al procesar el pedido: {str(e)}", "error")
        return redirect(url_for('ver_carrito'))
    
    finally:
        cursor.close()
    
    return redirect(url_for('menu'))

@app.route('/ubicaciones')
@login_required
def ubicaciones():
    return render_template('user/ubicaciones.html')

@app.route("/pedidos", methods=['GET', 'POST'])
@login_required
@worker_required
def pedidos():
    if request.method == 'POST':
        # Asegúrate de recibir el order_id del formulario
        order_id = request.form.get('order_id')
        if order_id:
            ModelOrders.set_ordered_as_delivered(db, order_id)
            return redirect(url_for('pedidos'))
        
    raw_orders = ModelOrders.get_not_delivered_orders(db)
    orders = []
    for raw_order in raw_orders:
        current_order = {}
        current_order['order_id'] = raw_order[0]  # Cambiado a nombre consistente
        current_order['numero_de_orden'] = raw_order[0]  # Alias para la plantilla
        current_order['ordenado_por'] = ModelUsers.get_by_id(db, raw_order[1])
        current_order['fecha_de_orden'] = raw_order[2]
        current_order['monto_total'] = raw_order[3]
        orders.append(current_order)
    return render_template('worker/pedidos.html', orders=orders)



@app.route("/nosotros")
@login_required
def nosotros():
    return render_template('user/nosotros.html')

@app.route("/contacto")
@login_required
def contacto():
    return render_template('user/contacto.html')



if __name__ == '__main__':
    
    app.run()