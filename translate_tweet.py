import tweepy
import time as t

from libs.translator import translate_to_english

def oauth_login(consumer_key, consumer_secret, access_token, access_token_secret):
     
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth, wait_on_rate_limit=True)

def retrieve_last_seen_id(dir_path):

    try:
        f_read = open(dir_path, 'r')
        last_id = int(f_read.read().strip())
        f_read.close()

    except ValueError:
        last_id = None

    return last_id  

def save_last_seen_id(last_id, dir_path):

    f_write = open(dir_path, 'w')
    f_write.write(str(last_id))
    f_write.close()

def reply_translated_tweet(api, mentions):

    try:
        for mention in mentions:
            translated = translate_to_english(mentions[mention]['text'])
            if translated is None:
                reply = "@{} Why do I need to translate English to English?".format(mentions[mention]['handle'])
                api.update_status(reply, mention)
                continue

            reply = "@{} {}", mention[mention]['handle'], translated
            api.update_status(reply, mention)

    except tweepy.error.TweepError:
        return

def extract_mentions(api):
    
    user_handle = "@twt2eng" + " "
    dir_path = 'data/last_seen_id.txt'

    last_id = retrieve_last_seen_id(dir_path)

    if last_id is None:
        mentions = api.mentions_timeline()

    else:
        mentions = api.mentions_timeline(last_id, tweet_mode='extended')

    mentions_dict = {}

    for mention in reversed(mentions):
        text = mention.text.replace(user_handle, '')
        value = {'handle': mention.user.screen_name, 'text': text}
        mentions_dict[mention.id] = value
        last_id = mention.id

    save_last_seen_id(last_id, dir_path)

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
        t.sleep(15)