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

from config import MeetupVariables
from config import GlobalVariables


class Meetup:

    def __init__(self):
        self.variables = MeetupVariables.__dict__
        self.globals = GlobalVariables.__dict__
        self.timeout = self.globals['TIMEOUT']
        self.username = self.variables['USERNAME']
        self.password = self.variables['PASSWORD']
        self.message = self.variables['MESSAGE_TEXT']

    def login_to_meetup(self):
        options = Options()
        options.headless = self.globals['HEADLESS']
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        self.chrome = webdriver.Chrome(
            self.globals['CHROMEDRIVER'], options=options)
        self.wait = WebDriverWait(self.chrome, self.timeout)

        self.chrome.get(self.variables['LOGIN_URL'])

        print('[Meetup] Logging in as ' + self.username)
        username = self.chrome.find_element_by_name('email')
        username.send_keys(self.username)

        password = self.chrome.find_element_by_name('password')
        password.send_keys(self.password)

        # Submit
        password.send_keys(Keys.RETURN)

    def search(self, tag):
        print('[Meetup] Searching for ' + tag)
        link = self.variables['SEARCH_URL'] + tag
        self.chrome.get(link)

    def get_groups(self):
        print('[Meetup] Getting all available groups')
        groups = []
        visible_groups = self.chrome.find_elements_by_css_selector(
            'a.groupCard--photo')
        for group in visible_groups:
            link = group.get_attribute('href')
            if link.startswith('https://www.meetup.com/'):
                groups.append(link)
        print('[Meetup] Found ' + str(len(groups)) + ' groups.')
        return groups

    def get_admin_name(self):
        print('[Meetup] Getting admin name')
        full_name = self.chrome.find_element_by_css_selector(
            'a.orgInfo-name > span').text
        name = full_name.split(' ')
        return name[0]

    def get_message_link(self):
        link = self.chrome.find_element_by_css_selector(
            'a.orgInfo-message').get_attribute('href')
        return link

    def send_message(self, name, link):
        print('[Meetup] Messaging ' + name)

        self.chrome.get(link)
        time.sleep(5)

        message_box = self.chrome.find_element_by_css_selector(
            'textarea#messaging-new-convo')
        message_to_send = 'Hi ' + name + ', ' + self.message
        message_box.send_keys(message_to_send)

        send_btn = self.chrome.find_element_by_css_selector(
            'button#messaging-new-send')
        send_btn.click()

    def already_messaged(self, group):
        with open(self.variables['MESSAGED_GROUPS'], 'r') as f:
            messaged_groups = f.read().split('\n')

        if group in messaged_groups:
            return True
        return False

    def add_to_messaged(self, group):
        with open(self.variables['MESSAGED_GROUPS'], 'a') as f:
            f.write('\n' + group)

    def message_groups(self, groups):
        print('[Meetup] Messaging group admins')
        for group in groups:
            self.chrome.get(group)
            print('[Meetup] Going to group')
            print('[Meetup] Waiting 10 secs')
            time.sleep(10)

            name = self.get_admin_name()
            message_link = self.get_message_link()

            if self.already_messaged(group):
                print('[Meetup] Already messaged this group')
            else:
                self.send_message(name, message_link)
                self.add_to_messaged(group)

            # Wait for 55 to 65 seconds
            print('[Meetup] Wait for 60 secs')
            for _ in range(random.randint(55, 65)):
                time.sleep(1)

    def message_keyword(self, keyword):
        self.search(keyword)
        groups = self.get_groups()
        self.message_groups(groups)

    def main(self, keywords):
        self.login_to_meetup()

        print('[Meetup] Waiting for 10 secs')
        time.sleep(10)

        print('[Meetup] Starting keyword search')
        for keyword in keywords:
            self.message_keyword(keyword)

        print('[Meetup] Done')
