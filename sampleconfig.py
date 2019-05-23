# Change file name to config.py
class GlobalVariables:
    # Change as you see fit
    CHROMEDRIVER = 'path/to/chromedriver.exe'
    TIMEOUT = 10
    HEADLESS = False

class TwitterVariables:
    # Account Details
    USERNAME = "username"
    PASSWORD = "password"

    # CHANGE TO WHAT YOU WANT
    DO_NOT_MESSAGE = "data/twitter/do_not_message.txt"
    MESSAGED_CSV = "data/twitter/twitter_messaged.csv"
    REPLIED_CSV = "data/twitter/twitter_replied.csv"
    FOLLOWS_CSV = "data/twitter/twitter_followed.csv"
    REPLY_TEXT = "hello there this is a reply"
    DM_TEXT = "hello there this is a dm"

    # Constants
    LOGIN_URL = 'https://twitter.com/login'
    SEARCH_URL = 'https://twitter.com/search?q='
    DM_URL = 'https://twitter.com/messages/compose?recipient_id='

class InstagramVariables:
    # Account Details
    USERNAME = "username"
    PASSWORD = "password"

    # CHANGE TO WHAT YOU WANT
    REPLIED_TO = "data/instagram/instagram_replied.txt"
    FOLLOWS_CSV = "data/instagram/instagram_followed.csv"
    REPLY_TEXT = "hello there this is a reply"

    # Constants
    LOGIN_URL = 'https://instagram.com/accounts/login'
    SEARCH_URL = 'https://instagram.com/explore/tags/'

class MeetupVariables:
    # Account Details
    USERNAME = "username"
    PASSWORD = "password"

    # CHANGE TO WHAT YOU WANT
    MESSAGED_GROUPS = "data/meetup/meetup_messaged.txt"

    # Result of this will be, "Hi {admin name}, hello there this is a message"
    MESSAGE_TEXT = "hello there this is a message"

    # Constants
    LOGIN_URL = 'https://meetup.com/login'
    SEARCH_URL = 'https://www.meetup.com/find/?allMeetups=false&radius=Infinity&sort=recommended&eventFilter=mysugg&keywords='
