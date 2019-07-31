import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class oneClickApp:
    def __init__(self, platform, username, password):
        self.platform = platform
        self.username = username
        self.password = password
        self.beginBot = webdriver.Firefox()

    def login(self):
        if self.platform.lower() == 'twitter':
            self.login_Twitter()
        elif self.platform.lower() == 'facebook':
            self.login_Facebook()
        else:
            return -1

    def scroll_down(self):
        try:
            last_height = self.beginBot.execute_script("return document.body.scrollHeight")
            while True:
                self.beginBot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.beginBot.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break

                last_height = new_height
        except Exception as error:
            print(error)

    def login_Twitter(self):
        beginBot = self.beginBot
        beginBot.get('https://twitter.com/login')
        userTag = "js-username-field"
        passwordTag = "js-password-field"
        try:
            WebDriverWait(beginBot, 10).until(
                EC.presence_of_all_elements_located)
            user = WebDriverWait(beginBot, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, userTag)))
            password = WebDriverWait(beginBot, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, passwordTag)))
            user.clear()
            user.send_keys(self.username)
            password.clear()
            password.send_keys(self.password)
            time.sleep(1)
            login_button = beginBot.find_element_by_css_selector(
                'button.submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
            login_button.submit()
        except Exception as error:
            print(error)

    def login_Facebook(self):
        beginBot = self.beginBot
        beginBot.get('https://facebook.com/login')
        userTag = "email"
        passwordTag = "pass"
        try:
            user = WebDriverWait(beginBot, 10).until(
                EC.presence_of_element_located((By.ID, userTag)))
            password = WebDriverWait(beginBot, 10).until(
                EC.presence_of_element_located((By.ID, passwordTag)))
            user.clear()
            user.send_keys(self.username)
            password.clear()
            password.send_keys(self.password)
            login_button = beginBot.find_element_by_id('loginbutton')
            login_button.submit()
            beginBot.quit()
        except Exception as error:
            print(error)

    def mass_follow_twitter(self, keywords):
        start_time = time.time()
        beginBot = self.beginBot
        try:
            time.sleep(2)
            search = beginBot.find_element_by_id('search-query')

            search.clear()
            search.send_keys(keywords)
            search.send_keys(Keys.ENTER)

        except Exception as error:
            print(error)
        WebDriverWait(beginBot, 10).until(
            EC.presence_of_all_elements_located)
        self.scroll_down()  # Scrolling to end of page for max tweets
        try:
            WebDriverWait(beginBot, 10).until(
                EC.presence_of_all_elements_located)
            tweets = beginBot.find_elements_by_class_name('tweet')
            links = [elem.get_attribute('data-permalink-path') for elem in tweets]
            print(len(links))
            for inner in range(0, len(links) - 1):
                beginBot.get('https://twitter.com' + links[inner])
                try:
                    WebDriverWait(beginBot, 10).until(
                        EC.presence_of_all_elements_located)
                    beginBot.find_element(
                        By.XPATH, "//span[text() = 'Follow']").click()
                    time.sleep(2)
                    print("Followed: " + links[inner].split("/")[1] + " " + str(inner + 1))
                except Exception as error:
                    print(error)

        except Exception as error:
            print(error)
        print("Time taken: " + str(int((time.time() - start_time) / 60)) + " minutes")
        beginBot.get('https://twitter.com/')

    def get_followed_users(self):
        beginBot = self.beginBot
        beginBot.get('https://twitter.com/following')
        try:
            self.scroll_down()
            # Getting the usernames of all the followed accounts
            pagesrc = beginBot.page_source
            soup = BeautifulSoup(pagesrc, "lxml")
            username = []
            for users in soup.find_all("b", class_="u-linkComplex-target"):
                username.append(users.text)
            username.pop(0)
            username.pop(0)
            return username
        except Exception as error:
            print(error)

    def unfollow_all(self):
        try:
            self.unfollow_specific_amount(1, 1)
        except Exception as error:
            print(error)

    def unfollow_specific_amount(self, amount, flag=0):
        start_time = time.time()
        unfollowed = 0
        beginBot = self.beginBot
        try:
            username = self.get_followed_users()
            if flag == 1:
                amount = len(username)
            for user in username:
                if unfollowed == amount:
                    break
                beginBot.get('https://twitter.com/' + user)
                WebDriverWait(beginBot, 10).until(
                    EC.presence_of_all_elements_located)
                beginBot.find_element_by_xpath(
                    '//div[@class = "UserActions   u-textLeft"]//span[contains(@class, "user-actions-follow-button '
                    'js-follow-btn follow-button")]').click()
                unfollowed += 1
                time.sleep(2)
                print("Unfollowed: " + user + " " + str(unfollowed))

        except Exception as error:
            print(error)
        print("Time taken: " + str(int((time.time() - start_time) / 60)) + " minutes")
        beginBot.get('https://twitter.com/')

    def delete_tweets(self):
        start_time = time.time()
        beginBot = self.beginBot
        beginBot.get('https://twitter.com/search?q=&src=typd')
        self.scroll_down()  # Scrolling to end of page for max tweets
        try:
            WebDriverWait(beginBot, 10).until(
                EC.presence_of_all_elements_located)
            tweets = beginBot.find_elements_by_class_name('tweet')
            links = [elem.get_attribute('data-permalink-path') for elem in tweets]
            print(len(links))
            for inner in range(0, len(links) - 1):
                beginBot.get('https://twitter.com' + links[inner])
                try:
                    WebDriverWait(beginBot, 10).until(
                        EC.presence_of_all_elements_located)
                    beginBot.find_element(
                        By.XPATH, "//span[text() = 'Follow']").click()
                    time.sleep(2)
                    print("Followed: " + links[inner].split("/")[1] + " " + str(inner + 1))
                except Exception as error:
                    print(error)

        except Exception as error:
            print(error)
        print("Time taken: " + str(int((time.time() - start_time) / 60)) + " minutes")
        beginBot.get('https://twitter.com/')

    def scrap_tweets(self, keywords):
        start_time = time.time()
        beginBot = self.beginBot
        scrapped = []
        try:
            time.sleep(2)
            search = beginBot.find_element_by_id('search-query')

            search.clear()
            search.send_keys(keywords)
            search.send_keys(Keys.ENTER)

        except Exception as error:
            print(error)

        try:
            WebDriverWait(beginBot, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'HTML')))
            self.scroll_down()  # Scrolling to end of page for max tweets
            WebDriverWait(beginBot, 10).until(
                EC.presence_of_all_elements_located)
            tweets = beginBot.find_elements_by_class_name('tweet')
            links = [elem.get_attribute('data-permalink-path') for elem in tweets]
            print(len(links))
            for inner in range(0, len(links) - 1):
                beginBot.get('https://twitter.com' + links[inner])
                try:
                    WebDriverWait(beginBot, 10).until(
                        EC.presence_of_all_elements_located)
                    scrapped.append(beginBot.find_element_by_xpath(
                        "//div[@class='css-901oao r-hkyrab r-1qd0xha r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-19yat4t "
                        "r-bnwqim r-qvutc0']").get_attribute(
                        'innerHTML'))
                    time.sleep(2)
                    print("Scrapped " + str(inner + 1))
                except Exception as error:
                    print(error)

        except Exception as error:
            print(error)
        print("Time taken: " + str(int((time.time() - start_time) / 60)) + " minutes")
        beginBot.get('https://twitter.com/')


if __name__ == "__main__":
    username = input("Input Username: ")
    password = input("Input Password: ")
    bot = oneClickApp("twitter", username, password)
    bot.login()
    time.sleep(2)
    # bot.mass_follow_twitter("elon musk")
    # bot.unfollow_all()
    bot.scrap_tweets("deep learning")
