from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Notar que se usa @main.app_errorhandler para handlear el error!
# en el caso anterior se usó @app.errorhandler
# No entendí bien la explicación. Pero está en la página 91
