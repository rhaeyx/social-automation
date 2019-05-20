import time
from bot_scripts.twitter import Twitter

"""
Settings are in config.py
"""

"""
    account.main(keywords, n)
    params:
    keywords:list - list of keywords both hashtags and phrases
    n:int - number of tweets to reply to for each keyword 

    main() will search each keyword and get n tweets from each keyword, then would like each n tweets and follow their
    authors, after all that is done it would then start messaging the authors that the bot just followed then done
"""

account = Twitter()
keywords = ["#Osteoporosismonth","#Healthybones", "#HealhyAging", "#Longevity", "#Fractures", "Osteoporosis", "Bone health", "Bone fractures", "Senior care", "Aging",
            "Primary Care", "Care providers", "Women’s health", "Sports medicine", "Physical therapy", "Rheumatology", "Health care", "Digital Health", "Health innovation", "Gerontology"]
account.main(keywords, 10)

