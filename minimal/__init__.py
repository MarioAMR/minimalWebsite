import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"
from .jinjafilters import *
from .errorhandlers import *
os.environ["SESSION_SECRET"]="MySessionSecret" 
def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SESSION_SECRET'],
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from . import bl_home
    app.register_blueprint(bl_home.bp)

    from . import bl_modals
    app.register_blueprint(bl_modals.bp)

    from . import bl_niceurls
    app.register_blueprint(bl_niceurls.bp)

    #Add other blueprints if needed

    from . import auth
    app.register_blueprint(auth.auth)

    login_manager = LoginManager()
    login_manager.login_message = "Please login to access your portal"
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Note

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    with app.app_context():
        db.create_all()

    #ADDS HANDLER FOR ERRORs
    app.register_error_handler(500, error_500)
    app.register_error_handler(404, error_404)

    #JINJA FILTERS
    app.jinja_env.filters['slugify'] = slugify
    app.jinja_env.filters['displayError'] = displayError 
    app.jinja_env.filters['displayMessage'] = displayMessage

    return app
