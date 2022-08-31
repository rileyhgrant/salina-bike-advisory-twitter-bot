import tweepy
# import requests
import os
from load_env import load_twitter_env
import weather_call

# load twitter credentials
consumer_key, consumer_secret, access_token, access_secret, bearer_token = load_twitter_env()

# advisory_tweet = "Hello world!"
advisory_tweet = weather_call.create_advisory()

# TODO: trying a guide with tweepy and 2.0
# # authenticate to twitter using Tweepy
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)

# # connect to twitter API
# api = tweepy.API(auth)


# # test auth
# try:
# 	api.verify_credentials()
# 	print("Authenticated to Twitter!")
# except:
# 	print("Error authenticating to twitter. Please re-configure credentials.")

# # send tweet
# try:
# 	api.update_status(advisory_tweet)
# 	print("Successful Tweet: ", advisory_tweet)
# except:
# 	print("Error posting.")


client = tweepy.Client(bearer_token=bearer_token,
											 consumer_key=consumer_key,
											 consumer_secret=consumer_secret,
											 access_token=access_token,
											 access_token_secret=access_secret,
											#  return_type = requests.Response,
											 wait_on_rate_limit=True)

response = client.create_tweet(text=advisory_tweet)


