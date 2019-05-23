from urllib.parse import quote_plus
import time
import csv
import random
from datetime import datetime

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from config import TwitterVariables
from config import GlobalVariables

class Twitter:
    def __init__(self):
        self.globals = GlobalVariables.__dict__
        self.variables = TwitterVariables.__dict__
        self.timeout = self.globals['TIMEOUT']
        self.username = self.variables['USERNAME']
        self.password = self.variables['PASSWORD']
        self.reply = self.variables['REPLY_TEXT']
        if len(self.reply) > 263:
            print('Please keep the reply text less than 264 characters.')
            exit()

    def login_to_twitter(self):
        options = Options()
        options.headless = self.globals['HEADLESS']
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        self.chrome = webdriver.Chrome(self.globals['CHROMEDRIVER'], options=options)
        self.wait = WebDriverWait(self.chrome, self.timeout)
        
        # Open link to twitter
        self.chrome.get(self.variables['LOGIN_URL'])

        # Input login details
        print('[Twitter] Logging in as ' + self.username)
        username = self.chrome.find_element_by_class_name('js-username-field')
        username.send_keys(self.username)
        
        password = self.chrome.find_element_by_class_name('js-password-field')
        password.send_keys(self.password)

        submit = self.chrome.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button')
        submit.click()
            
    def search(self, tag, tab):
        print('[Twitter] Searching for ' + tag)
        if tab == 'top':
            query = self.variables['SEARCH_URL'] + quote_plus(tag)
        elif tab == 'latest':
            query = self.variables['SEARCH_URL'] + quote_plus(tag) + '&f=tweets'

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

    def already_replied_to_user(self, username):
        with open(self.variables['REPLIED_CSV'], 'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                line = line.split(',')
                if line[0] == username:
                    return True
            return False

    def already_replied_to_tweet(self):
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

    def already_messaged_user(self, user):
        with open(self.variables['MESSAGED_CSV'], 'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                line = line.split(',')
                if line[0] == user['username']:
                    return True
        
        with open(self.variables['DO_NOT_MESSAGE'], 'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                if line == user['username']:
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

    def submit(self):
        webdriver.ActionChains(self.chrome).send_keys(Keys.CONTROL, Keys.RETURN, Keys.CONTROL).perform()

    def extract_data(self, tweets):
        data = []
        for tweet in tweets:
            username = tweet.get_attribute('data-screen-name')
            tweet_id = tweet.get_attribute('data-tweet-id')
            user_id = tweet.get_attribute('data-user-id')
            data.append((username, tweet_id, user_id))
        return data

    def add_to_messaged_csv(self, username):
        with open(self.variables['MESSAGED_CSV'], 'a') as f:
            date = datetime.now().strftime('%m-%D-%y')
            time = datetime.now().strftime('%H:%M')
            f.write('\n' + ','.join([username, date, time]))

    def add_to_replied_csv(self, username, tweet):
        with open(self.variables['REPLIED_CSV'], 'a') as f:
            date = datetime.now().strftime('%m-%D-%y')
            time = datetime.now().strftime('%H:%M')
            f.write('\n' + ','.join([username, tweet, date, time]))

    def reply_to_tweets(self, tweets):
        print('[Twitter] Replying to tweets')
        tweets_data = self.extract_data(tweets)

        for tweet in tweets_data:
            username = tweet[0]
            tweet_id = tweet[1]
            user_id = tweet[2]
            print('[Twitter] Replying to ' + username + '\'s tweet' )
            tweet_link = f'https://twitter.com/{username}/status/{tweet_id}'
            self.chrome.get(tweet_link)
            time.sleep(10)

            tweet = self.chrome.find_element_by_class_name('js-actionable-tweet')

            if not self.is_followed(tweet):
                self.follow(username)
                self.add_to_follows_csv(username, user_id)

            if self.already_replied_to_tweet() or self.already_replied_to_user(username):
                continue

            tweet_id = tweet.get_attribute('data-tweet-id')
            tweet_box = self.chrome.find_element_by_id('tweet-box-reply-to-' + tweet_id)
            reply = '@' + username + ' ' + self.reply
            if len(reply) > 280:
                print('[Twitter] Too many characters in reply.')
                continue
            tweet_box.send_keys(reply)

            self.add_to_replied_csv(username, tweet_link)

            self.submit()

            for _ in range(random.randint(55,65)):
                time.sleep(1)


    def reply_to_keyword(self, keyword, n):
        self.search(keyword, 'top')
        print('[Twitter] Getting top tweets')
        top_tweets = self.get_tweets(n)

        time.sleep(5)
        self.search(keyword, 'latest')
        print('[Twitter] Getting latest tweets')
        latest_tweets = self.get_tweets(n)
        
        print('[Twitter] Replying to top tweets')
        self.reply_to_tweets(top_tweets)
        print('[Twitter] Replying to latest tweets')
        self.reply_to_tweets(latest_tweets)

    def add_to_follows_csv(self, username, user_id):
        with open(self.variables['FOLLOWS_CSV'], 'a') as f:
            print('[Twitter] Adding ' + username + ' to database.')

            link = 'https://twitter.com/' + username
            data = ','.join([username, user_id, link, 'true', 'false'])
            f.write('\n' + data)

    def get_follows_csv(self):
        with open(self.variables['FOLLOWS_CSV'], 'r') as f:
            reader = csv.DictReader(f)
            data = []
            for row in reader:
                data.append(dict(row))

        if not data:
            print('[Twitter] No data on csv file')

        return data
    
    def update_csv_row(self, new_data, index):
        new_data = list(new_data.values())
        print(new_data, index)

        with open(self.variables['FOLLOWS_CSV'], 'r') as old:
            csvreader = csv.reader(old)
            lines = list(csvreader)
            lines[index + 1] = new_data

        with open(self.variables['FOLLOWS_CSV'], 'w', newline='') as new:
            csvwriter = csv.writer(new)
            csvwriter.writerows(lines)

    def message(self, user, i):
        print('[Twitter] Messaging ' + user['username'])
        url = self.variables['DM_URL']
        dm_text = quote_plus(self.variables['DM_TEXT'])
        url += user['user_id'] + '&text=' + dm_text
        
        self.chrome.get(url)
        time.sleep(5)
        
        try:
            inp_box = self.chrome.find_element_by_class_name('DMComposer-editor')
            inp_box.send_keys(Keys.RETURN)
            user['messaged'] = 'true'
            self.update_csv_row(user, i)
            print('[Twitter] Message sent')

            self.add_to_messaged_csv(user['username'])
        except:
            user['messaged'] = 'cannot'
            self.update_csv_row(user, i)
            print('[Twitter] Cannot be messaged')

    def main(self, keywords, n):
        self.login_to_twitter()
        
        print('[Twitter] Starting the keyword search and reply operation')
        for keyword in keywords:
            self.reply_to_keyword(keyword, n)

        print('[Twitter] Starting the messaging operation')
        user_data = self.get_follows_csv()

        for i, user in enumerate(user_data):
            if user['messaged'] == 'false' or not self.already_messaged_user(user):
                self.message(user, i)
                print('[Twitter] Waiting for 60 secs')
                for i in range(random.randint(55, 65)):
                    time.sleep(1)

        print('[Twitter] Done')
