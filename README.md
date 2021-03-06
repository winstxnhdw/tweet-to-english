# tweet-to-english

A Twitter bot that detects the language of tweets and translates them into English using [IBM Watson's Translator API](https://cloud.ibm.com/catalog/services/language-translator). Made this bot as an excuse to test [Heroku Dynos](https://www.heroku.com/dynos).

> **Note**: This bot uses polling. Please use [webhooks](https://en.wikipedia.org/wiki/Webhook) instead.

## Requirements

Run the following to install Docker on either Arch Linux or Ubuntu. If you are on another platform, you will have to install Docker manually [here](https://docs.docker.com/get-docker/).

```bash
sh requirements.sh
```

## API Keys

Create a `api_keys/tweepy.py` file with the following contents.

```python
CONSUMER_KEY='<your consumer key>'
CONSUMER_SECRET='<your consumer secret>'
ACCESS_TOKEN='<your access token>'
ACCESS_TOKEN_SECRET='<your access token secret>'
```

Create a `api_keys/ibm.py` file with the following contents.

```python
KEY='<your API key>'
URL='<your API URL>'
```

## Usage

```bash
sh launch.sh
```
