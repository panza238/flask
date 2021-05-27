from flask import Flask, request, make_response, render_template, redirect, session, url_for, flash
from markupsafe import escape
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_mail import Message
import os

basedir = os.path.abspath(os.path.dirname(__file__))  # Directorio base.
app = Flask(__name__)
bootstrap = Bootstrap(app)  # Ahora puedo usar bootstrap templates para hacer mi front más lindo con menos esfuerzo.
moment = Moment(app)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")  # Esto es para usar WTF Forms.
# Configuración para usar SQLite con SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Configuración de mail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)

# Esta va a ser la route básica. No hace nada más que display "Hello, World!"
@app.route("/")
def hello_world():
    """una route sin nada (landing page), se llama 'index page' """
    return "<h1>Hello, Pepelopy!</h1>"


# Esto agarra lo que se le ponga en la ruta. y te saluda
@app.route("/dynamic/<name>")
def hello(name):
    """ Esto es dynamic routing. No es estático. Cambia para cada <name>
    escape es una medida de seguridad para evitar la injection."""
    return f"Hello, {escape(name)}!"


@app.route("/user_agent")
def user_agent_fc():
    """Estoy accediendo a la información de la request que hizo mi browser.
    el servidor devuelve una response, con información de la request (qué browser está usando)."""
    user_agent = request.headers.get("User-Agent")
    return f"Your browser is: {user_agent}"


# Bad response example
@app.route("/bad_response")
def bad_response():
    """Por default, las funciones en Flask devuelven una response 200 (everythong ok)
    Esta función va a devolver un response 400 (como si algo hubiera salido mal)"""
    return "<h2>Bad Request!</h2>", 400


# make_response example
@app.route("/make_response")
def make_response_fc():
    """ejemplo de cómo se puede hacer una custom response con make_response"""
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie("answer", "42")
    return response


# Template rendering example
@app.route("/template")
def template_rendering_fc():
    """render desde un html file que está en /templates/"""
    return render_template("template_test.html")


# Dynamic emplate rendering example
@app.route("/dyn_templates/<string:temp_name>")
def dyn_template_rendering_fc(temp_name):
    """render dinámico. Se modifica un template a partir de parámetros de entrada.
    Uso la variable html_name para que quede explícito que eso es lo que le va a llegar al template de HTML
    De paso, también le metí otra feature de Flask. <string: foo> solo me deja meter strings en foo."""
    return render_template("template_dynamic.html", html_name=temp_name)


# Jinja & template extention example:
@app.route("/extended/<int:list_len>")
def extended(list_len):
    """usando el template que hay en base.html, construyo extended.html
    llamando a extended.html usé un poco de td... macros, base templates, jinja.
    notar que, al final, lo que se muestra es un html fijo, sin las variables!
    también uso python_list y html_list para que quede explícito."""
    python_list = list(range(list_len))
    return render_template("extended.html", html_list=python_list)


# Bootstrap expample:
@app.route("/bootstrap_extended/<string:name>")
def bootstrap_extended(name):
    """Muy parecido al extended. Pero ahora, el template que uso como base es el de Bootstrap"""
    return render_template("bootstrap_extended.html", html_name=name,
                           current_time=datetime.utcnow())


# Error handling example
@app.errorhandler(404)
def page_not_found(e):
    """La idea de esta función es dirigirte a una página custom cuando haya un error.
    Esto va a funcionar solo para el error 404. si quiero handelear otro error... tengo que hacer otra función.
    (o ver cómo lo resolvieron en CS50)"""
    return render_template("/404.html"), 404


# Form example (WTForms)
# Primero tengo que definir mi objeto form en una clase
class MyForm(FlaskForm):
    """Esta clase va a servir par instanciar formularios que tengan un campo para ingresar el nombre
    y un campo/botón de Submit"""
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# ahora uso una función, en la que le paso mi clase a render_template
@app.route("/forms", methods=["GET", "POST"])
def form_fc():
    my_form = MyForm()  # Creo mi form object que después va a ser rendereado por Jinja.
    name = None
    # Ahora vamos a hacer lo que en CS50 hacían con if request.method == "POST" con el form object que creamos.
    if my_form.validate_on_submit():  # Esto devuelve True solo si el form object fue submitted (vía POST request)
        name = my_form.name.data
        my_form.name.data=""  # Tengo que aprender a ponerle un placeholder.
        # Si el form fue submitted, ahora, va a mostrar el nombre que estaba en el form
    return render_template("/form.html", form=my_form, html_name=name)


# Ejemplo de la misma función de forms, pero con mejores prácticas de programación
@app.route("/forms2", methods=["GET", "POST"])
def form2_fc():
    """Va a hacer lo mismo que la función anterior. De hecho, va a renderear el mimso template.
    Pero, se va a encargar de que la última request NO sea una POST request.
    Se va a encargar de corregir el funcionamiento cuando uno recarga la página.
    También le agrego flashing messages para avisar del cambio."""
    my_form = MyForm()
    if my_form.validate_on_submit():
        flash("Looks like you've changed your name!")  # Esto va a mostrar un flash message!
        session["name"] = my_form.name.data
        return redirect(url_for("form2_fc"))
    # Notar que no hace falta que defina un nome = None. get va a devolver None si no hay name.
    # lo que pasa adentro del if es: 1) guarda el contenido del form en la sessión del usuario.
    # 2) Redirige al mismo URL: /forms2. Cuando se renderea, toma el nombre de la session, que persiste entre requests.
    # Ahora, con esto. No puedo hacer que se olvide mi nombre, a menos que explícitamente se lo diga en el código.
    return render_template("/form.html", form=my_form, html_name=session.get("name"))


# DATABASES!
# Vamos a trabajar con SQLite (porque es más fácil)
class Role(db.Model):
    """Este model va a ser el objeto que representa a la tabla 'roles'"""
    __tablename__ = 'roles'  # nombre de la tabla.
    id = db.Column(db.Integer, primary_key=True)  # Primera columna
    name = db.Column(db.String(64), unique=True)  # Segunda columna
    users = db.relationship('User', backref='role', lazy="dynamic")  # Acá estoy creando una relación...
    # NO me cierra tanto el 'role'... 'role' es una high-level representation de la one-to-many relationship.
    # En la flask shell la puedo tratar como una columna más de la tabla users.

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    """Objeto que referencia la tabla users"""
    __tablename__ = 'users'  # nombre de la tabla.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # Acá agrego la columna, y le digo que es una foreign key.

    def __repr__(self):
        return '<User %r>' % self.username


# ahora armo una función que interactúe con la db a través del ORM.
# Puedo pensar a los models como una definición de tablas. Con el objeto db, puedo interactuar con ellas.
@app.route("/model_form", methods=["GET", "POST"])
def model_form():
    form = MyForm()
    if form.validate_on_submit():
        flash("Looks like you've changed your name!")  # Esto va a mostrar un flash message!
        user = User.query.filter_by(username=form.name.data).first()  # Busca el nombre que acabo de ingresar en el form de la DB
        #result = db.engine.execute("SELECT * FROM users")  # OK... esto también funciona.

        if user is None:  # Si no lo encuentra en la DB, lo agrega
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            session['name'] = form.name.data
            return redirect(url_for('model_form'))
        else:  # Si lo encuentra en la DB, sólo cambia el session name.
            session['known'] = True
            session['name'] = form.name.data
            form.name.data = ''
            return redirect(url_for('model_form'))  # Este es el truco del redirect para que quede una GET request.
    return render_template('/model_form.html',
                           form=form, html_name=session.get('name'),
                           known=session.get('known', False))

# Para no tener que estar importando siempre:
@app.shell_context_processor
def make_shell_context():
    """Ahora se db, User y Role se importan automágicamente cuando incializo la flask shell."""
    return dict(db=db, User=User, Role=Role)


# MAIL
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

@app.route('/mail', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('model_form.html', form=form, name=session.get('name'),
                           known=session.get('known', False))

