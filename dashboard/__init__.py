import os
import json
from flask import Flask
from flask.templating import render_template
from . queries import query_research_location

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        config_setup = {
            "type": os.environ.get('service_account'),
            "project_id": os.environ.get('project_id'),
            "private_key_id": os.environ.get('private_key_id'),
            "private_key": os.environ.get('private_key'),
            "client_email": os.environ.get('client_email'),
            "client_id": os.environ.get('client_id'),
            "auth_uri": os.environ.get('auth_uri'),
            "token_uri": os.environ.get('token_uri'),
            "auth_provider_x509_cert_url": os.environ.get('auth_provider_x509_cert_url'),
            "client_x509_cert_url": os.environ.get('client_x509_cert_url')
        }
        if not os.path.isfile('instance/digital-science-covid19-0ec7e3e208ed.json'):
            with open("instance/digital-science-covid19-0ec7e3e208ed.json", "w") as f:
                json.dump(config_setup, f)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        top_locations = query_research_location()
        print(top_locations)

        return render_template('location/location.html', top_locations=top_locations)

    from . import dashboard
    app.register_blueprint(dashboard.bp)

    return app