from flask import Flask

from os import environ as env

if __name__ == "__main__":
    app = Flask(__name__)
    app.run(host='0.0.0.0', port=int(env.get('PORT')), debug=False)