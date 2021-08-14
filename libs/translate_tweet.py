import tweepy
import time as t

from libs.translator import translate_to_english

def oauth_login(consumer_key, consumer_secret, access_token, access_token_secret):
     
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth, wait_on_rate_limit=True)

def get_clean_text(full_text):

    user_handle = "@twt2eng"
    full_text_split = full_text.split(' ')
    index = full_text_split.index(user_handle) + 1

    return ' '.join(full_text_split[index:])

def reply_translated_tweet(api, mentions):

    try:
        for mention in mentions:
            translated = translate_to_english(mentions[mention]['text'])
            if translated is None:
                continue

            reply = "@{} {}".format(mentions[mention]['handle'], translated)
            api.update_status(reply, mention)

    except tweepy.error.TweepError:
        return

def extract_mentions(api):
    
    start_time = t.time()
    dir_path = 'data/last_seen_id.txt'
    mentions = api.mentions_timeline(tweet_mode='extended')
    mentions_dict = {}

    for mention in reversed(mentions):
        if start_time < mention.created_at.timestamp():
            continue

        clean_text = get_clean_text(mention.full_text)

        value = {
            'handle': mention.user.screen_name,
            'text': clean_text,
            'timestamp': mention.created_at.timestamp()
        }
        mentions_dict[mention.id] = value

    return mentions_dict

def translate_tweet():

    try:
        from api_keys.tweepy import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

    except ImportError:
        from os import environ as env
        CONSUMER_KEY = env['CONSUMER_KEY']
        CONSUMER_SECRET = env['CONSUMER_SECRET']
        ACCESS_TOKEN = env['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = env['ACCESS_TOKEN_SECRET']

    api = oauth_login(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    while True:
        mentions = extract_mentions(api)
        reply_translated_tweet(api, mentions)
        print("DEBUG")
        t.sleep(15)

if __name__ == "__main__":
    translate_tweet()