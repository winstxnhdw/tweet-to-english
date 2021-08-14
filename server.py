from flask import Flask

from os import environ as env
from translate_tweet import translate_tweet

app = Flask(__name__)

@app.route('/')
def main():
    translate_tweet()
    return " "
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(env.get('PORT')), debug=False)