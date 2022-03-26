from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .paperlist import bp as paperlist_bp
    app.register_blueprint(paperlist_bp)

    from .searchbycategory import bp as searchbycategory_bp
    app.register_blueprint(searchbycategory_bp)

    from .basicsearch import bp as basicsearch_bp
    app.register_blueprint(basicsearch_bp)

    from .paperinfo import bp as paperinfo_bp
    app.register_blueprint(paperinfo_bp)

    return app
