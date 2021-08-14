FROM python:3.9.5-buster

WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./

CMD ["python", "translate_tweet.py"]