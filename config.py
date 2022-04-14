import tweepy
import logging
from credentials import *

logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Adjust the values below to tweak the bot to your liking

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Keyword(s) and/or hashtag(s) that you want to like / retweet
# Basic Formatting:
#   - Use %20OR%20 to separate keywords and hashtags
#       - i.e. dog%20OR%20cat
#   - Replace hashtag symbol # with %23 
#       - i.e. #twitter should be %23twitter
# More information about query formatting here: 
#   https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/guides/basic-stream-parameters
search_keywords = "当たる%20AND%20フォロー%20OR%20RT%20OR%20いいね%20OR%20リツイート" # TODO: better search keywords

# Time to wait between processing a request in seconds 
# Information about TwitterAPI limits here: https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits
delay = 100

# Specify what type of search results you want to get
# 'recent', 'popular', or 'mixed'
result_type = 'popular'

# Specify the number of tweets you want the bot to iterate through
number_of_tweets = 5
# OR change run_continuously to True if you want it to run continuously (or for deploying)
# if True, number_of_tweets will not be used
run_continuously = False

# Change booleans depending on if you want to only retweet, only like, or do both
retweet_tweets = True
like_tweets = True
follow_user = True


def create_api():
    auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)
    api = tweepy.API(auth)

    try:
        my_info = api.verify_credentials()
    except Exception as e:
        logger.error('Authentication Error', exc_info=True)
        raise e
    logger.info(f"Authentication OK. Connected to @{my_info.screen_name}")

    return api, my_info
