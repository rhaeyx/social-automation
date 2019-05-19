from urllib.parse import quote_plus
import time

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from config import TwitterVariables

class Twitter:
    def __init__(self):
        self.variables = TwitterVariables.__dict__
        self.timeout = self.variables['TIMEOUT']
        self.username = self.variables['USERNAME']
        self.password = self.variables['PASSWORD']
        self.reply = self.variables['REPLY_TEXT']
        if len(self.reply) > 264:
            print('Please keep the reply text less than 264 characters.')
            exit()

    def login_to_twitter(self):
        # Selenium
        options = Options()
        options.headless = False
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        self.chrome = webdriver.Chrome('../chromedriver.exe', options=options)
        self.wait = WebDriverWait(self.chrome, self.timeout)
        
        # Open link to twitter
        self.chrome.get('https://twitter.com/login')

        # Input login details
        username = self.chrome.find_element_by_class_name('js-username-field')
        username.send_keys(self.username)
        
        password = self.chrome.find_element_by_class_name('js-password-field')
        password.send_keys(self.password)

        submit = self.chrome.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button')
        submit.click()
            
    def search(self, tag):
        query = self.variables['SEARCH_URL'] + quote_plus(tag)
        self.chrome.get(query)

    def get_tweets(self, n):
        while self.tweets_loaded() < n:
            html = self.chrome.find_element_by_tag_name('html')
            # To scroll to the bottom of the page and load more tweets
            html.send_keys(Keys.END)
            time.sleep(1)
        # If number of tweets is >= to n, get the tweets
        tweets = self.chrome.find_elements_by_class_name('js-stream-tweet')
        return tweets[:n]        

    def tweets_loaded(self):
        tweets = self.chrome.find_elements_by_class_name('js-stream-tweet')
        return len(tweets)

    def already_replied(self):
        try:
            replies = self.chrome.find_element_by_class_name('descendant')
        except:
            return False

        for reply in replies:
            reply_username = reply.get_attribute('data-screen-name')
            if reply_username.lower() == self.username.lower():
                return True
        return False

    def reply_to_tweets(self, tweets):
        if len(self.reply) > 263:
            print('Please keep the reply text less than 263 characters.')
            exit()

        for tweet in tweets:
            username = tweet.get_attribute('data-screen-name')
            print(f"Replying to {username}'s tweet...'")
            
            reply_btn = tweet.find_element_by_class_name('js-actionReply')
            reply_btn.click()

            self.wait.until(EC.visibility_of_element_located((By.ID, 'tweet-box-global')))

            if self.already_replied():
                # Go to next tweet
                html = self.chrome.find_element_by_tag_name('html')
                html.send_keys(Keys.ESCAPE)
                time.sleep(3)
                continue

            tweet_box = self.chrome.find_element_by_id('tweet-box-global')
            reply = '@' + username + ' ' + self.reply
            if len(reply) > 280:
                print('Cannot reply to')
            tweet_box.send_keys(reply)

            submit = self.chrome.find_element_by_class_name('js-tweet-btn')
            submit.click()
            time.sleep(3)

    def reply_to_keyword(self, keyword, n):
        print("Logging in...")
        self.login_to_twitter()
        print(f"Logged in as {self.username}")

        print(f"Searching for {keyword}...")
        self.search(keyword)
        print(f"Search found {n} tweets...")
        
        tweets = self.get_tweets(n)
        print("Replying to tweets...")
        self.reply_to_tweets(tweets)


