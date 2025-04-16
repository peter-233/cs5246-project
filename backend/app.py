from flask import Flask
from flask_cors import CORS

from backend.routes.parse_result import parse_result_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(
    parse_result_bp,
    url_prefix='/',
    static_folder='static',
    template_folder='templates'
)

if __name__ == '__main__':
    app.run()
