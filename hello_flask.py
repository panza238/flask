from flask import Flask, request, make_response, render_template
from markupsafe import escape

app = Flask(__name__)


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
    notar que, al final, lo que se muestra es un html fijo, sin las variables!"""
    return render_template("extended.html", html_list=list(range(list_len)))
