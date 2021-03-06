import tweepy
import time as t

from libs.translator import translate_to_english

class TweetToEnglish():

    def __init__(self, auth):

        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.last_id = None
        
        self.bot_handle = 'twt2eng'
        self.max_tweets = 10
        self.mode = 'extended'

    def sanitise_text(self, full_text):

        full_text_split = full_text.split(' ')
        index = full_text_split.index(f'@{self.bot_handle}') + 1

        return ' '.join(full_text_split[index:])

    def reply_translated_tweet(self, mentions):

        for mention in mentions:
            tweet = mentions[mention]

            translated = translate_to_english(tweet['text'])
            print(f"Translated reply ({mention}): {translated}")

            if not translated:
                continue

            reply = f"@{tweet['handle']} {translated}"
            self.api.update_status(reply, mention)
            print(f"Replied to {mention}.")

    def extract_mentions(self, start_time):

        print("\nExtracting timeline mentions..")

        if not self.last_id:
            mentions = self.api.mentions_timeline(count=self.max_tweets, tweet_mode=self.mode)

        else:
            mentions = self.api.mentions_timeline(since_id=self.last_id, count=self.max_tweets, tweet_mode=self.mode)
            
        mentions_dict = {}

        for mention in mentions:
            if mention.created_at.timestamp() < start_time or mention.user.screen_name == self.bot_handle:
                continue

            clean_text = self.sanitise_text(mention.full_text)

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
    return auth

def translate_tweet():
    
    print("\nInitialising Twitter bot..")
    
    try:
        from api_keys.tweepy import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

    except ImportError:
        from os import environ as env
        CONSUMER_KEY = env['CONSUMER_KEY']
        CONSUMER_SECRET = env['CONSUMER_SECRET']
        ACCESS_TOKEN = env['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = env['ACCESS_TOKEN_SECRET']

    auth = oauth_login(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    bot = TweetToEnglish(auth)
    
    start_time = t.time()

    while True:
        mentions = bot.extract_mentions(start_time)

        try:
            bot.reply_translated_tweet(mentions)
        
        except tweepy.error.TweepError:
            print("No tweets were translated.")

        print("Cycle complete.")
        t.sleep(30)

if __name__ == "__main__":
    translate_tweet()
