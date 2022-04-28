# tweet-to-english

A Twitter bot that detects the language of tweets and translates them into English using [IBM Watson's Translator API](https://cloud.ibm.com/catalog/services/language-translator). Made this bot as an excuse to test [Heroku Dynos](https://www.heroku.com/dynos).

> This bot uses polling. Please use [webhooks](https://en.wikipedia.org/wiki/Webhook) instead.

## Installation

### Requirements

Once you have installed [Docker](https://docs.docker.com/get-docker/) and [Python](https://www.python.org/downloads/), run the following block.

```bash
pip install -r requirements.txt
```

### API Keys

Create a `api_keys/tweepy.py` file with the following contents.

```python
CONSUMER_KEY= '<your consumer key>'
CONSUMER_SECRET= '<your consumer secret>'
ACCESS_TOKEN= '<your access token>'
ACCESS_TOKEN_SECRET= '<your access token secret>'
```

Create a `api_keys/ibm.py` file with the following contents.

```python
KEY= '<your API key>'
URL= '<your API URL>'
```

## Usage

```bash
sh launch.sh
```
