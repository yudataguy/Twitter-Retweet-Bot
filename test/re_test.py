import re


tweet_text = "私は吉岡さんは #ひらいて と言っていると回答！吉岡里帆さんは何と言っている？ @ayatakaJP をフォロー＆選択肢から回答をツイートで、100名様に #綾鷹 １ケース当たる！ https://t.co/puYMKSMWkr #茶葉ひらく香り立つ旨み"

def get_user_account(tweet):
    twitter_usernames = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z0-9_]+)', tweet)
    
    if twitter_usernames:
        return twitter_usernames

print(get_user_account(tweet_text))