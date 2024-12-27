from flask import Flask
from flask_cors import CORS
from controllers.usuario import Usuario

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(Usuario)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

