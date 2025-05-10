from flask import Flask
from flask import request, redirect, url_for, render_template, flash, abort
from flask_mysqldb import MySQL
from config import DevelopmentConfig
from models.ModelUsers import ModelUsers
from models.entities.users import User
from flask_login import LoginManager, login_user, logout_user,login_required,current_user
from functools import wraps



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

@app.route("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Solo manejar lógica de login
    if request.method == "POST":
        user = User(0, request.form['email'], request.form['password'], None, 0)
        logged_user = ModelUsers.login(db, user)
        if logged_user is not None:
            login_user(logged_user)
            if logged_user.usertype == 0:
                return redirect(url_for("index"))
            elif logged_user.usertype == 1:
                return redirect(url_for("index"))
            else:
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
    if request.method == 'POST':
        try:
            # Validar campos obligatorios
            if not all([request.form.get('email'), request.form.get('fullname'), request.form.get('password')]):
                flash("Todos los campos son obligatorios")
                return redirect(url_for('perfil'))
            print(f"{current_user.id},{current_user.email}, {current_user.fullname}, {current_user.password}, {current_user.usertype}")
            # Actualizar usuario
            current_user.email = request.form['email']
            current_user.fullname = request.form['fullname']
            current_user.password = request.form['password']
            
            # Guardar cambios en la base de datos
            ModelUsers.update(db, current_user)
            
            flash("Perfil actualizado exitosamente")
            return redirect('logout')
            
        except Exception as e:
            flash(f"Error al actualizar el perfil: {str(e)}")

    user = ModelUsers.get_by_id(db, id)
    if user is None:
        flash("Usuario no encontrado")
        return redirect(url_for('index'))
    
    # Si el usuario es el mismo que está logueado, permitir editar
    if current_user.id == id or current_user.usertype == 2:
        # Renderizar plantilla con datos del usuario
        return render_template("user/perfil.html", user=user, editable=True)
    
    if current_user.id != user.id:
        flash("No tienes permiso para editar este perfil")
        return redirect(url_for('index'))

    # Renderizar plantilla con datos del usuario
    return render_template("user/perfil.html", user=user)


@app.route("/admin")
@login_required
@admin_required
def admin():
    return (render_template("admin.html"))

@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)

@app.route('/logout')
@login_required
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

    # Transformar a lista de diccionarios si lo necesitas
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




if __name__ == '__main__':
    
    app.run()