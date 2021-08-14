import os

from flask import Flask
from libs.translate_tweet import translate_tweet

class TranslateTweet(Flask):

  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):

    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        translate_tweet()
        
    super(TranslateTweet, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

if __name__ == "__main__":
    app = TranslateTweet(__name__)
    app.run(host='0.0.0.0', port=os.environ.get('PORT'), debug=True)