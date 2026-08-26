from flask import Flask, render_template, jsonify
from config import Config
from routes.api import api_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/learn")
    def learn():
        return render_template("learn.html")


    @app.errorhandler(413)
    def request_too_large(_error):
        return jsonify({
            "success": False,
            "error": "Request is too large. Please use a smaller input."
        }), 413

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
