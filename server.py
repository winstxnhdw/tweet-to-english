import os

from flask import Flask
from libs.translate_tweet import translate_tweet

class TranslateTweet(Flask):

  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
      
    super(TranslateTweet, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)
    translate_tweet()

if __name__ == "__main__":
    app = TranslateTweet(__name__)
    app.run(host='0.0.0.0', port=os.environ.get('PORT'), debug=False)