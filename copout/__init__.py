import os

from flask import Flask
from dotenv import load_dotenv

def create_app(test_config=None):
    load_dotenv('.env')
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'copout.sqlite'),
        SECRET_GEO=app.config.get('SECRET_GEO'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import report
    app.register_blueprint(report.bp)
    app.add_url_rule('/', endpoint='index')

    return app


