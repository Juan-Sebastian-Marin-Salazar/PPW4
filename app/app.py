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
        if not current_user.is_authenticated or current_user.usertype != 1:
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


@app.route("/perfil" , methods=['GET', 'POST'])
@login_required
def perfil():
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
    
    
    return (render_template("user/perfil.html"))


@app.route("/menu")
@login_required
def menu():
    return (render_template("user/menu.html"))

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

if __name__ == '__main__':
    
    app.run()