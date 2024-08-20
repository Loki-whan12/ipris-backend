from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

from routes.user_routes import user_bp
from routes.plant_routes import plant_bp
from routes.comment_routes import comment_bp

# Register Blueprints
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(plant_bp, url_prefix='/plants')
app.register_blueprint(comment_bp, url_prefix='/comments')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

