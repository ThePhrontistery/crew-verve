from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from crewverve.middleware import authenticate_handler
from crewverve.views import crewverve_bp
from crewverve.models import init_app
from admin.views import admin_bp

app = Flask(__name__)

# The SECRET_KEY is used to encrypt session data in (persistent) cookies.
# >>> import secrets; secrets.token_hex(32)
app.config['SECRET_KEY'] = '642918690903c342d812d16cd33a4de4c8692483462550c9ddcd4303621cc1b2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crewverve.db'
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True
db = init_app(app)
app.register_blueprint(crewverve_bp)
app.register_blueprint(admin_bp)

app.app_context().push()
db.create_all()


@app.before_request
def before_request():
    return authenticate_handler(None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        if username == 'john' and password == 'hola':
        
            session['CURRENT_USER'] = username
            return redirect(url_for('crewverve.index'))
        else:
            error = 'Invalid username or password'
               

    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET'])
def logout():

    # Note: Flask session. NOT SqlAlchemy...
    del session['CURRENT_USER']
    return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('crewverve.index'))


@app.route('/page-not-found')
def page_not_found():
    return render_template('error.html', error_message="Page not found", error_description="This isn't the page you are looking for....")


if __name__ == '__main__':
    app.run(debug=True)
