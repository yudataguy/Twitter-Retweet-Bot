"""
A Twitter bot written in Python using Tweepy and deployed on AWS EC2. 
It will like and/or retweet tweets that contain single or multiple keywords and hashtags.
"""

# Built-in/Generic Imports
import os
import logging
import time

# Library Imports
import tweepy

# Own modules
from config import *

__author__ = 'Annie Wu'
__version__ = '1.0.0'
__maintainer__ = 'Annie Wu'
__email__ = 'anniewu2303@gmail.com'
__status__ = 'Dev'


logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()

api = create_api()
self = api.me()

if run_continuously:
    tweets = tweepy.Cursor(api.search,
                       q=search_keywords + "-filter:retweets",
                       result_type=result_type,
                       monitor_rate_limit=True, 
                       wait_on_rate_limit=True,
                       lang="en").items()
else:
    tweets = tweepy.Cursor(api.search,
                       q=search_keywords + "-filter:retweets",
                       result_type=result_type,
                       monitor_rate_limit=True, 
                       wait_on_rate_limit=True,
                       lang="en").items(number_of_tweets)


for tweet in tweets:
    tweet = api.get_status(tweet.id)
    logger.info(f"Processing tweet: {tweet.text}")

    # Ignore tweets if author is myself
    if tweet.user.id != self.id:

        if retweet_tweets:
            if not tweet.retweeted:
                try:
                    tweet.retweet()
                    logger.info("Retweeted now")
                except Exception as e:
                    logger.error("Error in retweet", exc_info=True)
                    raise e
            else:
                logger.info("Has been retweeted previously")

        if like_tweets:    
            if not tweet.favorited:
                try:
                    tweet.favorite()
                    logger.info("Favorited now")
                except Exception as e:
                    logger.error("Error in favorite", exc_info=True)
                    raise e
            else:
                logger.info("Has been favorited previously")

    time.sleep(delay)