import logging

from flask import Flask
from flask_cors import CORS
from waitress import serve

from backend.routes.fetch_article.routes import fetch_article_bp
from backend.routes.parse_result import parse_result_bp
from backend.routes.summary.routes import summary_bp
from backend.utils.utils import generate_internal_error_response

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/',
)
CORS(app)

app.register_blueprint(
    parse_result_bp,
    url_prefix='/',
    static_folder='static',
    template_folder='templates'
)
app.register_blueprint(
    fetch_article_bp,
    url_prefix='/',
    static_folder='static',
    template_folder='templates'
)
app.register_blueprint(
    summary_bp,
    url_prefix='/',
    static_folder='static',
    template_folder='templates'
)


@app.errorhandler(Exception)
def handle_exception(error):
    print(error)
    return generate_internal_error_response(error)


if __name__ == '__main__':
    logger = logging.getLogger('waitress.queue')
    logger.setLevel(logging.ERROR)
    serve(app, listen='0.0.0.0:5000', threads=1)
