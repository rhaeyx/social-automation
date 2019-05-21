import time
from bot_scripts.instagram import Instagram

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

account = Instagram()
keywords = ["#Osteoporosismonth", "#Healthybones", "#HealhyAging", "#Longevity", "#Fractures"]

account.main(keywords, 2)
