# Change file name to config.py

class GlobalVariables:
    CHROMEDRIVER = 'chromedriver'
    TIMEOUT = 10

class TwitterVariables:
    # Account Details
    USERNAME = "username"
    PASSWORD = "password"

    # CHANGE TO WHAT YOU WANT
    FOLLOWS_CSV = "twitter_followed.csv"
    REPLY_TEXT = "hello there this is a reply"
    DM_TEXT = "hello there this is a dm"

    # Constants
    LOGIN_URL = 'https://twitter.com/login'
    SEARCH_URL = 'https://twitter.com/search?q='
    DM_URL = 'https://twitter.com/messages/compose?recipient_id='
