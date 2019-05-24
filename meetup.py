import time
from bot_scripts.meetup import Meetup

"""
Settings are in config.py
"""

"""
    account.main(keywords)
    params:
    keywords:list - list of keywords both hashtags and phrases

    main() will search the keyword, find all groups, go to each group page, message the admin then
    go to next keyword
"""

account = Meetup()
keywords = ["#Osteoporosismonth", "#Healthybones",
            "#HealhyAging", "#Longevity", "#Fractures"]

account.main(keywords)
