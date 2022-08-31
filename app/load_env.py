import os
from dotenv import load_dotenv
load_dotenv()

def load_weather_env():
	"""
	TODO:
	"""
	weather_api_key = os.getenv('WEATHER_API_KEY')
	return weather_api_key

def load_twitter_env():
	"""
	TODO:
	"""
	consumer_key = os.getenv("TWITTER_API_KEY")
	consumer_secret = os.getenv("TWITTER_API_SECRET")
	access_token = os.getenv("TWITTER_ACCESS_TOKEN")
	access_secret = os.getenv("TWITTER_ACCESS_SECRET")
	bearer_token = os.getenv("TWITTER_API_BEARER_TOKEN")
	return consumer_key, consumer_secret, access_token, access_secret, bearer_token