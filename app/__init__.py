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

    from .collection import bp as collection_bp
    app.register_blueprint(collection_bp)

    from .paperinfo import bp as paperinf_bp
    app.register_blueprint(paperinf_bp)

    from .browse import bp as browse_bp
    app.register_blueprint(browse_bp)

    from .citationcart import bp as citationcart_bp
    app.register_blueprint(citationcart_bp)

    from .citation import bp as citation_bp
    app.register_blueprint(citation_bp)

    return app
