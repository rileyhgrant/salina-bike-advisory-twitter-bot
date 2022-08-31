import tweepy
import weather_call
from load_env import load_twitter_env
from datetime import date

# load twitter keys and secrets from .env
(
    consumer_key,
    consumer_secret,
    access_token,
    access_secret,
    bearer_token,
) = load_twitter_env()


print(f"creating Tweet ...")
advisory_tweet = weather_call.create_advisory()

# check if it's a weekend, if so don't make a post
today = date.today()
day_of_week = today.strftime("%A")
weekend = ["Saturday", "Sunday"]
if weekend.count(day_of_week) is not 0:
    print(f"today is {day_of_week}, a weekend. Not Tweeting today.")
    exit()


print(f"posting to Twitter ...")
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_secret,
)

response = client.create_tweet(text=advisory_tweet)
print("create_tweet completed")
print(f"response is: {response}")
