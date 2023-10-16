import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from config import config
from flask_mail import Mail, Message

# Models:
from models.ModelUser import ModelUser, update_token_in_database, generate_new_token

# Entities:
from models.entities.User import User

app = Flask(__name__)
mail = Mail(app)
db = MySQL(app)
login_manager_app = LoginManager(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] =  '@gmail.com' # Reemplaza esto con tu correo de Gmail
app.config['MAIL_PASSWORD'] =  '' # Reemplaza esto con tu contraseña de Gmail

mail = Mail(app)

def send_email(to, token):
    msg = Message('Tu token de acceso',
                  sender='@gmail.com',  # Reemplaza esto con tu correo de Gmail
                  recipients=[to])
    msg.body = f"Hola,\n\nEste es tu token de acceso: {token}\n\nSaludos."
    mail.send(msg)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password:
                new_token = generate_new_token()
                success = update_token_in_database(new_token, logged_user.id, db)
                if success:
                    send_email('@gmail.com', new_token)  # Reemplaza esto con la dirección de correo electrónico a la que deseas enviar el token
                    login_user(logged_user)
                    session['logged_in_user_id'] = logged_user.id
                    return redirect(url_for('token'))
                else:
                    flash("Hubo un problema al generar el nuevo token.")
            else:
                flash("Contraseña incorrecta.")
        else:
            flash("Usuario no encontrado.")
    return render_template('auth/login.html')

@app.route('/token', methods=['GET', 'POST'])
@login_required
def token():
    if 'logged_in_user_id' in session:
        if request.method == 'POST':
            user_token = request.form.get('token')
            user = ModelUser.get_by_id(db, int(session['logged_in_user_id']))

            if user and user.token == user_token:
                if datetime.datetime.now() - user.token_timestamp <= datetime.timedelta(minutes=2):
                    return render_template('home.html')
                else:
                    new_token = generate_new_token()
                    success = update_token_in_database(new_token, user.id, db)
                    if success:
                        flash("El token ha expirado. Se ha generado uno nuevo.")
                    else:
                        flash("Hubo un problema al generar el nuevo token.")
            else:
                flash("Token incorrecto. Inténtalo de nuevo.")
        return render_template('token.html')
    else:
        flash("Debes iniciar sesión primero.")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()