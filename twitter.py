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
"""

account = Twitter()
keywords = ["#Osteoporosismonth","#Healthybones", "#HealhyAging", "#Longevity", "#Fractures", "Osteoporosis", "Bone health", "Bone fractures", "Senior care", "Aging",
            "Primary Care", "Care providers", "Women’s health", "Sports medicine", "Physical therapy", "Rheumatology", "Health care", "Digital Health", "Health innovation", "Gerontology"]
account.main(keywords, 10)

