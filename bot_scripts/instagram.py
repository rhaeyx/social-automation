from urllib.parse import quote_plus
import time
import csv
import random

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from config import InstagramVariables
from config import GlobalVariables

class Instagram:
    
    def __init__(self):
        self.variables = InstagramVariables.__dict__
        self.globals = GlobalVariables.__dict__
        self.timeout = self.globals['TIMEOUT']
        self.username = self.variables['USERNAME']
        self.password = self.variables['PASSWORD']
        self.reply = self.variables['REPLY_TEXT']

    def login_to_instagram(self):
        options = Options()
        options.headless = self.globals['HEADLESS']
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        self.chrome = webdriver.Chrome(self.globals['CHROMEDRIVER'], options=options)
        self.wait = WebDriverWait(self.chrome, self.timeout)

        self.chrome.get(self.variables['LOGIN_URL'])

        print('[Instagram] Logging in as ' + self.username)
        username = self.chrome.find_element_by_name('username')
        username.send_keys(self.username)

        password = self.chrome.find_element_by_name('password')
        password.send_keys(self.password)

        # Submit
        password.send_keys(Keys.RETURN)
    
    def search(self, tag):
        print('[Instagram] Searching for ' + tag)
        if tag.startswith('#'):
            tag = tag[1:]
        else:
            print('[Instagram] Search function can only search for hashtags')
        link = self.variables['SEARCH_URL'] + tag
        self.chrome.get(link)

    def get_posts(self, n):
        print('[Instagram] Getting ' + str(n) + ' posts')
        while self.loaded_posts() < n:
           html = self.chrome.find_element_by_tag_name('html')
           html.send_keys(Keys.END)
           time.sleep(1)
        posts = []
        visible_posts = self.chrome.find_elements_by_tag_name('a')
        for post in visible_posts:
            link = post.get_attribute('href')
            if link.startswith('https://www.instagram.com/p/'):
                posts.append(link)
        print('[Instagram] Found ' + str(n) + ' posts')
        return posts[:n]

    def loaded_posts(self):
        posts = []
        visible_posts = self.chrome.find_elements_by_tag_name('a')
        for post in visible_posts:
            link = post.get_attribute('href')
            if link.startswith('https://www.instagram.com/p/'):
                posts.append(link)
        return len(posts)
    
    def get_replied_to_posts(self):
        with open(self.variables['REPLIED_TO'], 'r') as f:
            replied_to = f.read().split('\n')
        return replied_to

    def add_post_to_replied(self, link):
        with open(self.variables['REPLIED_TO'], 'a') as f:
            f.write('\n' + link)

    def already_replied(self, link):
        replied_to = self.get_replied_to_posts()        
        if link in replied_to:
            print('[Instagram] Already replied to this post')
            return True
        return False
    
    def is_followed(self, header):
        follow_btn = header.find_element_by_tag_name('button')
        if follow_btn.text == 'Follow':
            return False
        return True
    
    def follow(self, username, header):
        print('[Instagram] Following ' + username)
        follow_btn = header.find_element_by_tag_name('button')
        follow_btn.click()

    def save_to_csv(self, username):
        with open(self.variables['FOLLOWS_CSV'], 'a') as f:
            print('[Instagram] Adding ' + username + ' to database') 
            link = 'https://instagram.com/' + username
            data = ','.join([username, link, 'true'])
            f.write(data + '\n')
    
    def reply_to_posts(self, posts):
        print('[Instagram] Replying to posts')
        for post in posts:
            self.chrome.get(post)
            print('[Instagram] Going to another post')
            print('[Instagram] Waiting 10 secs')
            time.sleep(10)

            header = self.chrome.find_element_by_tag_name('header')
            username = header.find_element_by_css_selector('div:nth-child(2) > div > div').text

            # Remove verified text
            if username.endswith('\nVerified'):
                username = username.split('\n')[0]

            if not self.is_followed(header):
                self.follow(username, header)
                self.save_to_csv(username)
            else: 
                print('[Instagram] Already following ' + username)

            if self.already_replied(post):
                print('[Instagram] Already replied to this post')
                continue
            
            print('[Instagram] Replying to post')
            reply_box = self.chrome.find_element_by_tag_name('textarea')
            reply_box.click()

            # Needs to be selected again or will cause StaleElementException
            reply_box = self.chrome.find_element_by_tag_name('textarea')
            reply_box.send_keys(self.reply, Keys.RETURN)

            self.add_post_to_replied(post)

            # Wait for 55 to 65 seconds
            print('[Instagram] Wait for 60 secs')
            for _ in range(random.randint(55, 65)):
                time.sleep(1)

    def reply_to_keyword(self, keyword, n):
        self.search(keyword)
        posts = self.get_posts(n)
        self.reply_to_posts(posts)

    def main(self, keywords, n):
        self.login_to_instagram()

        print('[Instragram] Waiting for 10 secs')
        time.sleep(10)

        print('[Instagram] Starting the keyword search and reply operation')
        for keyword in keywords:
            self.reply_to_keyword(keyword, n)
        
        print('[Instagram] Done')
