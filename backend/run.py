from flask import Flask
from flask_cors import CORS
from app.routes.praw import praw_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})
app.register_blueprint(praw_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)