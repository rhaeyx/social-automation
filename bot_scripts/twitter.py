from urllib.parse import quote_plus
import time
import csv

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
        if len(self.reply) > 263:
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
        print('[Twitter] Logging in as ' + self.username)
        username = self.chrome.find_element_by_class_name('js-username-field')
        username.send_keys(self.username)
        
        password = self.chrome.find_element_by_class_name('js-password-field')
        password.send_keys(self.password)

        submit = self.chrome.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button')
        submit.click()
            
    def search(self, tag):
        print('[Twitter] Searching for ' + tag)
        query = self.variables['SEARCH_URL'] + quote_plus(tag)
        self.chrome.get(query)

    def get_tweets(self, n):
        print('[Twitter] Getting ' + str(n) + ' tweets')
        while self.loaded_tweets() < n:
            html = self.chrome.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            time.sleep(1)
        tweets = self.chrome.find_elements_by_class_name('js-stream-tweet')
        print('[Twitter] Found ' + str(n) + ' tweets')
        return tweets[:n]        

    def loaded_tweets(self):
        tweets = self.chrome.find_elements_by_class_name('js-stream-tweet')
        return len(tweets)

    def already_replied(self):
        try:
            replies = self.chrome.find_elements_by_class_name('descendant')
        except:
            return False

        for reply in replies:
            reply_username = reply.get_attribute('data-screen-name')
            if reply_username.lower() == self.username.lower():
                print('[Twitter] Already replied, proceeding to next tweet')
                return True
        return False

    def is_followed(self, tweet):
        followed = tweet.get_attribute('data-you-follow')
        if followed == 'false':
            return False
        return True

    def follow(self, username):
            print('[Twitter] Following ' + username)
            follow_btn = self.chrome.find_element_by_css_selector('div.content.clearfix > div > div.follow-bar > div > span > button.EdgeButton.EdgeButton--secondary.EdgeButton--medium.button-text.follow-text')
            follow_btn.click()


    def save_to_csv(self, username):
        with open(self.variables['FOLLOWS_CSV'], 'a') as f:
            print('[Twitter] Adding ' + username + ' to database.')
            link = 'https://twitter.com/' + username
            data = ', '.join([username, link, 'true'])
            f.write(data + '\n')

    def submit(self):
        webdriver.ActionChains(self.chrome).send_keys(Keys.CONTROL, Keys.RETURN, Keys.CONTROL).perform()


    def reply_to_tweets(self, tweets):
        print('[Twitter] Replying to tweets')
        tweets_data = []

        for tweet in tweets:
            username = tweet.get_attribute('data-screen-name')
            tweet_id = tweet.get_attribute('data-tweet-id')
            tweets_data.append((username, tweet_id))

        for tweet in tweets_data:
            username = tweet[0]
            tweet_id = tweet[1]
            print('[Twitter] Replying to ' + username + '\'s tweet' )
            self.chrome.get(f'https://twitter.com/{username}/status/{tweet_id}')
            time.sleep(3)

            tweet = self.chrome.find_element_by_class_name('js-actionable-tweet')

            if not self.is_followed(tweet):
                self.follow(username)
                self.save_to_csv(username)

            if self.already_replied():
                continue

            tweet_id = tweet.get_attribute('data-tweet-id')
            tweet_box = self.chrome.find_element_by_id('tweet-box-reply-to-' + tweet_id)
            reply = '@' + username + ' ' + self.reply
            if len(reply) > 280:
                print('Too many characters in reply.')
                continue
            tweet_box.send_keys(reply)

            self.submit()

            time.sleep(3)

    def reply_to_keyword(self, keyword, n):
        self.login_to_twitter()
        self.search(keyword)
        tweets = self.get_tweets(n)
        self.reply_to_tweets(tweets)


