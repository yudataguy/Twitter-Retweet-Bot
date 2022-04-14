"""
A Twitter bot written in Python using Tweepy. 
It will like and/or retweet tweets that contain single or multiple keywords and hashtags.
"""

# Built-in/Generic Imports
import os
import re
import logging
from time import sleep

# Library Imports
import tweepy

# Own modules
from config import *

logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()

def initialize_api():
    api, my_info = create_api()
    return api, my_info
    
def get_user_account(tweet):
    twitter_usernames = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z0-9_]+)', tweet)
    
    if twitter_usernames:
        return twitter_usernames

def get_tweets(api):
    # Exclude retweets from search to avoid repeats
    
    tweets = api.search_tweets(q=search_keywords + " -filter:retweets",
                        count=100,
                        result_type=result_type,
                        lang="ja")
    print(len(tweets))
    return tweets
    
def process_tweets(api, tweets, my_info):
    for tweet in tweets:
        # tweet = api.get_status(tweet.id)
        logger.info(f"Processing tweet: {tweet.text}")
        
        # Ignore tweet if it is from myself or if it is a reply to a tweet
        if tweet.user.id != my_info.id or tweet.in_reply_to_status_id is not None:
            
            if retweet_tweets:
                if not tweet.retweeted:
                    try:
                        tweet.retweet()
                        logger.info("Retweeted now")
                    except Exception as e:
                        logger.error("Error on retweet", exc_info=True)
                        continue
                else:
                    logger.info("Has been retweeted previously")

            if like_tweets:    
                if not tweet.favorited:
                    try:
                        tweet.favorite()
                        logger.info("Favorited now")
                    except Exception as e:
                        logger.error("Error on favorite", exc_info=True)
                        continue
                else:
                    logger.info("Has been favorited previously")
            
            if follow_user:
                usernames = get_user_account(tweet.text)
                print("usernames: ", usernames)
                try:
                    for username in usernames:
                        user = api.get_user(screen_name=username)
                        if user.id != my_info.id:
                            api.create_friendship(screen_name = username)
                            logger.info(f"Followed user: {user.screen_name}")
                    # api.create_friendship(user_id = tweet.user.id)
                    # logger.info("Followed user")
                except Exception as e:
                    logger.error("Error on follow", exc_info=True)
                    continue

        # Delay in between processing tweets
        sleep(delay)


if __name__ == "__main__":
    api, my_info = initialize_api()
    tweets = get_tweets(api)
    process_tweets(api, tweets, my_info)
