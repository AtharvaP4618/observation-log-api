from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    from . import models
    from .routes import main
    app.register_blueprint(main)

    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({
            "error": {
                "code": 400,
                "message": error.description
            }
        }), 400
    
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "error": {
                "code": 404,
                "message": error.description
            }
        }), 404


    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({
            "error": {
                "code": 500,
                "message": "Internal server error"
            }
        }), 500
    
    return app