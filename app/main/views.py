from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('model_form.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


# Notar que uso el @main.route en lugar de @app.route... esto es por lo mismo que se usa @main.app_errorhandler
# Notar también que se usa .index en lugar de index. Esto es porque es referente a esta bluerpint
# Esto es equivalente a decir "main.index"
