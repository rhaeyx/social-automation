# Change file name to config.py

class TwitterVariables:
    # Account Details
    USERNAME = "username"
    PASSWORD = "password"

    # CHANGE TO WHAT YOU WANT
    CHROMEDRIVER = 'path/to/chromedriver.exe'
    FOLLOWS_CSV = "twitter_followed.csv"
    REPLY_TEXT = "hello there this is a reply"
    DM_TEXT = "hello there this is a dm"
    TIMEOUT = 10

    # Constants
    LOGIN_URL = 'https://twitter.com/login'
    SEARCH_URL = 'https://twitter.com/search?q='
    DM_URL = 'https://twitter.com/messages/compose?recipient_id='
