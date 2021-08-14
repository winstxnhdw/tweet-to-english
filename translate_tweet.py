import tweepy
import time as t

from libs.translator import translate_to_english

class TweetToEnglish():

    def __init__(self):

        self.api = None
        self.last_id = None
        
        self.bot_handle = "twt2eng"
        self.max_tweets = 10
        self.mode = 'extended'

    def get_clean_text(self, full_text):

        full_text_split = full_text.split(' ')
        index = full_text_split.index('@' + self.bot_handle) + 1

        return ' '.join(full_text_split[index:])

    def reply_translated_tweet(self, mentions):

        try:
            for mention in mentions:
                tweet = mentions[mention]
                translated = translate_to_english(tweet['text'])
                print("Translated reply ({}): {}".format(mention, translated))
                if translated is None:
                    continue

                reply = "@{} {}".format(tweet['handle'], translated)
                self.api.update_status(reply, mention)
                print("Replied to {}.".format(mention))

        except tweepy.error.TweepError:
            print("No tweets were translated.")
            return

    def extract_mentions(self, start_time):

        print("\nExtracting timeline mentions..")

        if self.last_id is None:
            mentions = self.api.mentions_timeline(count=self.max_tweets, tweet_mode=self.mode)

        else:
            mentions = self.api.mentions_timeline(since_id=self.last_id, count=self.max_tweets, tweet_mode=self.mode)
        mentions_dict = {}

        for mention in mentions:
            if mention.created_at.timestamp() < start_time or mention.user.screen_name == self.bot_handle:
                continue

            clean_text = self.get_clean_text(mention.full_text)

            value = {
                'handle': mention.user.screen_name,
                'text': clean_text,
                'timestamp': mention.created_at.timestamp()
            }

            mentions_dict[mention.id] = value
            self.last_id = mention.id

        return mentions_dict

def oauth_login(consumer_key, consumer_secret, access_token, access_token_secret):
     
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

def translate_tweet():
    
    try:
        from api_keys.tweepy import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

    except ImportError:
        from os import environ as env
        CONSUMER_KEY = env['CONSUMER_KEY']
        CONSUMER_SECRET = env['CONSUMER_SECRET']
        ACCESS_TOKEN = env['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = env['ACCESS_TOKEN_SECRET']

    bot = TweetToEnglish()
    bot.api = oauth_login(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    start_time = t.time()

    while True:
        mentions = bot.extract_mentions(start_time)
        bot.reply_translated_tweet(mentions)
        print("Cycle complete.")
        t.sleep(30)

if __name__ == "__main__":
    print("\nInitialising Twitter bot..")
    translate_tweet()
