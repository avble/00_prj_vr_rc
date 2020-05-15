import os

from flask import Flask

from invitation import db
from invitation import peer
from invitation import auth


def create_app(test_config=None): 
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "invitation.sqlite"),
    )

    if test_config is not None:
        # load the test config if passed in
        app.config.update(test_config)
            
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.db_initialization(app)

    app.register_blueprint(peer.bp)
    app.register_blueprint(auth.bp)

    return app