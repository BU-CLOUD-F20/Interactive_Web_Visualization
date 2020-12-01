from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def load_api():
    from run import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    # app = create_app()
    # affiliates_schema = load_item()
    # load_item()
    load_api()
    app.run(debug=True, port=8080, host="http://api-flask-ece-528-interactive-web-visualization.k-apps.osh.massopen.cloud")
