from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.secret_key = 'your_secret_key_here'

    # Import the routes here to avoid circular imports
    from app.routes import main
    app.register_blueprint(main)

    return app
