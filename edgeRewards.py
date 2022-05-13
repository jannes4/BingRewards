from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from random_word import RandomWords
from overViewWindow import create_overview_window

dir = r'C:\Users\Admin\AppData\Local\MicrosoftEdge\User\Default'

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end-start} seconds')
        return result
    return wrapper


class Selector:
    def __init__(self, selectBy: By, value: str):
        self.selectBy = selectBy
        self.value = value


class Browser:
    def __init__(self):
        self.in_mobile_view = False

        self.options = Options()
        self.options.add_argument(f"--user-data-dir={dir}")

        self.driver = webdriver.Edge(options=self.options)

    def __del__(self):
        self.driver.close()

    def switch_to_modile_view(self):
        self.in_mobile_view = True

        self.driver.close()

        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        }

        self.options.add_experimental_option(
            "mobileEmulation", mobile_emulation)
        self.driver = webdriver.Edge(options=self.options)

    def load_page(self, url):
        self.driver.get(url)

    def wait_for_rewards_initialisation(self):
        if self.in_mobile_view:
            time.sleep(2)
            return

        try:
            element = browser.find_element(Selector(By.CSS_SELECTOR, ".rhlined.serp"))
        except:
            print("Rewards ready indicator not Found. Waiting 2s")
            time.sleep(1)
            return

        try:
            start_time = time.time()
            while(element.is_displayed() and time.time() - start_time < 2.5):
                time.sleep(.1)
        except:
            pass

    def switch_to_tab(self, index: int):
        try:
            self.driver.switch_to.window(self.driver.window_handles[index])
        except:
            try:
                amount_tabs_open = len(self.driver.window_handles)
                print("Invalid tab")
            except:
                print("All tabs closed!")

    def close_tab(self, index=-1):
        if index != -1:
            self.switch_to_tab(index)
        self.driver.close()
        self.switch_to_tab(0)

    def click_element(self, element, clickType=0):
        if(isinstance(element, Selector)):
            element = self.find_element(element)
        # isinstance(element, webdriver.remote.webelement.WebElement)

        if clickType == 0:
            return element.click()
        if clickType == 1:
            return self.driver.execute_script("arguments[0].click();", element)

    def find_element(self, selector: Selector, time_to_wait = 10) -> webdriver.remote.webelement.WebElement:
        try:
            element = WebDriverWait(self.driver, time_to_wait).until(
                EC.presence_of_element_located((selector.selectBy, selector.value))
            )
            return element
        except:
            return None

    def find_elements(self, selector: Selector) -> list:
        try:
            print("Waiting for selector")
            elements = WebDriverWait(self.driver, 3).until(
                EC.presence_of_all_elements_located(
                    (selector.selectBy, selector.value))
            )
            print(f"{len(elements)} Elements found")
            return elements
        except:
            return []


class Reward_type:
    def __init__(self, strings, function):
        self.string = strings
        self.function = function


class Actions:
    @staticmethod
    def open_rewards() -> int:
        browser.load_page("https://rewards.bing.com/")
        cards = browser.find_elements(
            Selector(By.CSS_SELECTOR, ".mee-icon-AddMedium"))
        for card in cards:
            browser.click_element(card)
        
        if(len(cards) > 0):
            browser.close_tab(0)
        else:
            print("No rewards found. Copilot activated!")

        return len(cards)

    @staticmethod
    def identify_reward_type():
        page_url = browser.driver.current_url

        for reward_type in Reward_functions.reward_types:
            matching = True
            for string in reward_type.string:
                if string not in page_url:
                    matching = False
                    break
            if matching:
                return reward_type.function()

        if "bing.com" not in page_url:
            print("url does not include bing.com. Tab closed instantly!")
            return

        print("not reward type found for url: " + page_url)
        browser.wait_for_rewards_initialisation()

    @staticmethod
    def start_searches():
        def get_random_words():
            r = RandomWords()
            random_words = r.get_random_words()

            while True:
                for word in random_words:
                    yield word

        def search_x_times(x):
            for i, word in zip(range(x), random_word_generator):
                browser.load_page(f"https://www.bing.com/search?q={word}")
                browser.wait_for_rewards_initialisation()

        random_word_generator = get_random_words()

        r = RandomWords()
        random_words = r.get_random_words()

        search_x_times(30)

        browser.switch_to_modile_view()

        search_x_times(20)


class Reward_functions:
    @staticmethod
    def survey():
        print("Survey")

        browser.click_element(Selector(By.CSS_SELECTOR, "#btoption0"), 1)
        # wait until there is the correct image
        browser.find_element(Selector(By.CSS_SELECTOR, ".cico.bt_pocheckmark"))

        print("Survey finished")

    @staticmethod
    def quiz():
        print("Quiz")

        def get_amount_answer_options() -> int:
            try:
                browser.driver.find_element(
                    By.CSS_SELECTOR, "#rqAnswerOption7")
                return 8
            except:
                try:
                    browser.driver.find_element(
                        By.CSS_SELECTOR, "#rqAnswerOption3")
                    return 4
                except:
                    return 1

        # start button
        browser.click_element(Selector(By.CSS_SELECTOR, "#rqStartQuiz"), 1)

        total_points = browser.find_element(
            Selector(By.CSS_SELECTOR, ".rqMCredits")).text
        amount_answer_options = get_amount_answer_options()
        print(f"{amount_answer_options} answer options")

        current_iteration = 0
        while(browser.find_element(Selector(By.CSS_SELECTOR, ".rqECredits")).text != total_points):
            for i in range(amount_answer_options):
                if browser.find_element(Selector(By.CSS_SELECTOR, ".rqECredits")).text == (str)((current_iteration + 1) * 10):
                    break

                browser.click_element(
                    Selector(By.CSS_SELECTOR, f"#rqAnswerOption{i}"), 1)

            current_iteration += 1
        browser.wait_for_rewards_initialisation()
        print("quiz finished")

    reward_types = [
        Reward_type(["DailyPoll"], survey.__func__),
        Reward_type(["QUIZ"], quiz.__func__),
    ]

def show_stats():
    browser.load_page("https://www.bing.com/rewards/")
    points = browser.find_element(Selector(By.CSS_SELECTOR, "#dashboard-set-goal > mee-card > div > card-content > mee-rewards-redeem-goal-card > div > div.contentContainer > p > b")).text
    username = browser.find_element(Selector(By.CSS_SELECTOR, "#meeBanner > div > div > mee-persona > div:nth-child(2) > persona-body > h2")).text

    value_in_microsoft_products = ((5 / 4650) * int(points.replace(".", ""))).__round__(2)
    real_value = ((5 / 7500) * int(points.replace(".", ""))).__round__(2)

    create_overview_window(username, points, value_in_microsoft_products, real_value)
    

browser = Browser()
amount_open_tasks = Actions.open_rewards()
for i in range(0, amount_open_tasks):
    Actions.identify_reward_type()
    if i < amount_open_tasks - 1:
        browser.close_tab()
Actions.start_searches()
show_stats()
browser.close_tab() 

time.sleep(10000)