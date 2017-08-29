import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import PlayGameUtil
import logging
import random
import time
import unicodedata

import logging

#setting up the logging for test results
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('test_user_input.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

class TestUserInputForm(unittest.TestCase):
    #ran once at the start of testsuite
    @classmethod
    def setUpClass(cls):
        cls.public_path = os.path.join('public', 'index.html')
        cls.game_path = os.path.abspath(os.path.join('..', cls.public_path))
        # make sure index.html path exist
        assert(os.path.exists(cls.game_path))

        cls.max_players = 3

        #adding open maximized option
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        cls.driver = webdriver.Chrome(chrome_options=options)
        # cls.driver = webdriver.Firefox()
        cls.driver.get('file:///' + cls.game_path)

        #hold the categories we've selected
        cls.categories = []
        #hold the player names
        cls.player_infos = []
        #create a PlayGameUtil to help us with some common functions
        cls.play_game_util = PlayGameUtil.GameUtil(cls.driver, cls.max_players)

    #ran once after testing is done
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        pass

    #setUp, ran once before each test
    def setUp(self):
        pass

    #tearDown, ran after each test case
    def tearDown(self):
        pass

#test to see if the userInput form has fields for users to input
class TestLoadUserInput(TestUserInputForm):
    def setUp(self):
        logging.info('Loading userInput')

    def test_load_user_input_form(self):
        logging.info('Title: {0}'.format(self.driver.title))
        self.assertTrue('Wheel of Jeopardy Setup' == self.driver.title)

    def test_has_field_for_player_name(self):
        for i in range(1,self.max_players+1):
            player_input_name = self.driver.find_element_by_xpath('//*[@id="p{0}Name"]'.format(i))
            self.assertTrue(player_input_name.is_displayed())
            logging.info('Has player{0} input'.format(i))

    #check that there is at least 12 categories to choose from
    def test_has_at_least_12_categories(self):
        waitForOptions = WebDriverWait(self.driver, 10)
        waitForOptions.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="cats"]/option[12]')))
        category_options = Select(self.driver.find_element_by_xpath('//*[@id="cats"]'))
        number_options = len(category_options.options)
        self.assertGreaterEqual(number_options,12)
        logging.info('Found {0} category options'.format(number_options))

    def test_has_start_game_button(self):
        start_game_button = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td/input[1]')
        self.assertTrue(start_game_button.is_enabled())
        self.assertTrue(start_game_button.is_displayed())
        logging.info('Found Start Game button')

    def test_has_add_category_button(self):
        add_category_button = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td/input[2]')
        self.assertTrue(add_category_button.is_enabled())
        self.assertTrue(add_category_button.is_displayed())
        logging.info('Found Add Category button')

    def test_has_update_delete_category(self):
        update_delete_category_button = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td/input[3]')
        self.assertTrue(update_delete_category_button.is_enabled())
        self.assertTrue(update_delete_category_button.is_displayed())
        logging.info('Found Update Delete Category button')

def testsuite_load_user_input():
    suite = unittest.TestSuite()
    suite.addTest(TestLoadUserInput('test_load_user_input_form'))
    suite.addTest(TestLoadUserInput('test_has_field_for_player_name'))
    suite.addTest(TestLoadUserInput('test_has_at_least_12_categories'))
    suite.addTest(TestLoadUserInput('test_has_start_game_button'))
    suite.addTest(TestLoadUserInput('test_has_add_category_button'))
    suite.addTest(TestLoadUserInput('test_has_update_delete_category'))
    return suite


#enter random information to start game and check if game is started with entered info
class TestTryGoodInputStartGame(TestUserInputForm):
    def setUp(self):
        logging.info('Loading userInput')

    def test_random_name_input(self):
        with open('FakeNameGenerator.com_cfc6c845.txt') as fp:
            lines = fp.readlines()
        name_set = [line.strip().split('\t')[1:] for line in lines]
        logging.info('Loaded names set')

        for i in range(1,self.max_players+1):
            logging.info('Filling in name for player{0}'.format(i))
            player_input_name = self.driver.find_element_by_xpath('//*[@id="p{0}Name"]'.format(i))
            self.assertTrue(player_input_name.is_displayed())
            random_name = ' '.join(random.choice(name_set))
            player_input_name.send_keys(Keys.CONTROL, "a")
            player_input_name.send_keys(random_name)
            #store the names for checking later
            self.player_infos.append(random_name)
            self.assertTrue(player_input_name.get_attribute('value') == random_name)
            logging.info('player{0} name is set {0}'.format(i,player_input_name.get_attribute('value') ))

    def test_random_categories_select(self):
        waitForOptions = WebDriverWait(self.driver, 10)
        waitForOptions.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="cats"]/option[12]')))
        el_category_option = Select(self.driver.find_element_by_xpath('//*[@id="cats"]'))
        category_options = el_category_option.options
        number_options = len(category_options)
        self.assertGreaterEqual(number_options, 12)
        logging.info('Selecting from {0} categories options'.format(number_options))
        logging.info('Shuffling category options')
        random.shuffle(category_options)
        #must select 12 of the items
        for x in range(0,12):
            option = category_options[x]
            option.click()
            logging.info('Selected {0}'.format(option.text))
            #store the information for later
            self.categories.append(option.text)
        self.chosen_categories = category_options[0:12]

    def test_random_start_game(self):
        start_game_button = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td/input[1]')
        self.assertTrue(start_game_button.is_enabled())
        self.assertTrue(start_game_button.is_displayed())
        logging.info('Starting game!')
        start_game_button.click()

        #wait for new tab to load
        waitForOptions = WebDriverWait(self.driver, 10)
        waitForOptions.until(EC.number_of_windows_to_be(2))
        windows = self.driver.window_handles
        logging.info('Number of windows {0}'.format(len(windows)))

        #switch to new window
        self.driver.switch_to.window(windows[1])
        #make sure the new open tab is the wheel.
        logging.info(self.driver.title)
        self.assertTrue('Wheel' == self.driver.title)

    def test_game_started_with_entered_inputs(self):
        #check names
        logging.info('Entered players name: {0}'.format(self.player_infos))
        actual_player_infos = self.play_game_util.read_player_info()
        for index,player in enumerate(actual_player_infos):
            self.assertEqual(str(player['playerName']), str(self.player_infos[index]))
            logging.info("Player{0} actual name: {1} , tested name: {2}".format(index, player['playerName'], self.player_infos[index]))

        #check categories
        logging.info('Entered categories: {0}'.format(self.categories))
        board = self.play_game_util.read_jeopardy_board()
        category_buttons = [category_button[0] for category_button in board['categoyButtons']]
        for index,category_button in enumerate(category_buttons):
            self.assertTrue(str(category_button) in self.categories)
            logging.info('{0} not in tested categories'.format(category_button))

def testsuite_try_good_input_start_game():
    suite = unittest.TestSuite()
    suite.addTest(TestTryGoodInputStartGame('test_random_name_input'))
    suite.addTest(TestTryGoodInputStartGame('test_random_categories_select'))
    suite.addTest(TestTryGoodInputStartGame('test_random_start_game'))
    suite.addTest(TestTryGoodInputStartGame('test_game_started_with_entered_inputs'))
    return suite


#enter extreamly large names and random byte array names
class TestTryBadInputNameStartGame(TestUserInputForm):
    def setUp(self):
        logging.info('Loading userInput')

    def test_random_name_input(self):
        with open('FakeNameGenerator.com_cfc6c845.txt') as fp:
            lines = fp.readlines()
        name_set = [line.strip().split('\t')[1:] for line in lines]
        logging.info('Loaded names set')

        for i in range(1,self.max_players+1):
            logging.info('Filling in name for player{0}'.format(i))
            player_input_name = self.driver.find_element_by_xpath('//*[@id="p{0}Name"]'.format(i))
            self.assertTrue(player_input_name.is_displayed())
            random_name = u'\x00' + u''.join(unichr(random.randint(0,255)) for _ in range(120)) + u'\x00'
            player_input_name.send_keys(Keys.CONTROL, "a")
            player_input_name.send_keys(random_name)
            #store the names for checking later
            self.player_infos.append(random_name)
            # self.assertTrue(player_input_name.get_attribute('value') == random_name)
            logging.info('player{0} name is set {0}'.format(i,player_input_name.get_attribute('value') ))

    def test_random_categories_select(self):
        waitForOptions = WebDriverWait(self.driver, 10)
        waitForOptions.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="cats"]/option[12]')))
        el_category_option = Select(self.driver.find_element_by_xpath('//*[@id="cats"]'))
        category_options = el_category_option.options
        number_options = len(category_options)
        self.assertGreaterEqual(number_options, 12)
        logging.info('Selecting from {0} categories options'.format(number_options))
        logging.info('Shuffling category options')
        random.shuffle(category_options)
        #must select 12 of the items
        for x in range(0,12):
            option = category_options[x]
            option.click()
            logging.info('Selected {0}'.format(option.text))
            #store the information for later
            self.categories.append(option.text)
        self.chosen_categories = category_options[0:12]

    def test_random_start_game(self):
        start_game_button = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td/input[1]')
        self.assertTrue(start_game_button.is_enabled())
        self.assertTrue(start_game_button.is_displayed())
        logging.info('Starting game!')
        start_game_button.click()

        #wait for new tab to load
        waitForOptions = WebDriverWait(self.driver, 10)
        waitForOptions.until(EC.number_of_windows_to_be(2))
        windows = self.driver.window_handles
        logging.info('Number of windows {0}'.format(len(windows)))

        #switch to new window
        self.driver.switch_to.window(windows[1])
        #make sure the new open tab is the wheel.
        logging.info(self.driver.title)
        self.assertTrue('Wheel' == self.driver.title)

    def test_game_started_with_entered_inputs(self):
        #check names
        logging.info('Entered players name: {0}'.format(self.player_infos))
        actual_player_infos = self.play_game_util.read_player_info()
        for index,player in enumerate(actual_player_infos):
            logging.info(u"Player{0} actual name: {1} , tested name: {2}".format(index, player['playerName'], self.player_infos[index]))

        #check categories
        logging.info('Entered categories: {0}'.format(self.categories))
        board = self.play_game_util.read_jeopardy_board()
        category_buttons = [category_button[0] for category_button in board['categoyButtons']]
        for index,category_button in enumerate(category_buttons):
            self.assertTrue(str(category_button) in self.categories)
            logging.info('{0} in tested categories'.format(category_button))

def testsuite_try_bad_input_name_start_game():
    suite = unittest.TestSuite()
    suite.addTest(TestTryBadInputNameStartGame('test_random_name_input'))
    suite.addTest(TestTryBadInputNameStartGame('test_random_categories_select'))
    suite.addTest(TestTryBadInputNameStartGame('test_random_start_game'))
    suite.addTest(TestTryBadInputNameStartGame('test_game_started_with_entered_inputs'))
    return suite



#not putting enough category
class TestTryBadInputCategoryStartGame(TestUserInputForm):
    def setUp(self):
        logging.info('Loading userInput')

    def test_random_name_input(self):
        with open('FakeNameGenerator.com_cfc6c845.txt') as fp:
            lines = fp.readlines()
        name_set = [line.strip().split('\t')[1:] for line in lines]
        logging.info('Loaded names set')

        for i in range(1,self.max_players+1):
            logging.info('Filling in name for player{0}'.format(i))
            player_input_name = self.driver.find_element_by_xpath('//*[@id="p{0}Name"]'.format(i))
            self.assertTrue(player_input_name.is_displayed())
            random_name = ' '.join(random.choice(name_set))
            player_input_name.send_keys(Keys.CONTROL, "a")
            player_input_name.send_keys(random_name)
            #store the names for checking later
            self.player_infos.append(random_name)
            # self.assertTrue(player_input_name.get_attribute('value') == random_name)
            logging.info('player{0} name is set {0}'.format(i,player_input_name.get_attribute('value') ))

    def test_random_categories_select(self):
        waitForOptions = WebDriverWait(self.driver, 10)
        waitForOptions.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="cats"]/option[12]')))
        el_category_option = Select(self.driver.find_element_by_xpath('//*[@id="cats"]'))
        category_options = el_category_option.options
        number_options = len(category_options)
        self.assertGreaterEqual(number_options, 12)
        logging.info('Selecting from {0} categories options'.format(number_options))
        logging.info('Shuffling category options')
        random.shuffle(category_options)
        #must select 12 of the items
        for x in range(0,10):
            option = category_options[x]
            option.click()
            logging.info('Selected {0}'.format(option.text))
            #store the information for later
            self.categories.append(option.text)
        self.chosen_categories = category_options[0:12]

    def test_random_start_game(self):
        start_game_button = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[4]/td/input[1]')
        self.assertTrue(start_game_button.is_enabled())
        self.assertTrue(start_game_button.is_displayed())
        logging.info('Starting game!')
        start_game_button.click()

        #expect alert
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            logging.info('Alert found!')
            self.assertEqual('Error - Please select 12 categories.', alert.text)
            alert.accept()
        except TimeoutException:
            raise ValueError
            logging.info('Alert not found!')

def testsuite_try_not_enough_category_name_start_game():
    suite = unittest.TestSuite()
    suite.addTest(TestTryBadInputCategoryStartGame('test_random_name_input'))
    suite.addTest(TestTryBadInputCategoryStartGame('test_random_categories_select'))
    suite.addTest(TestTryBadInputCategoryStartGame('test_random_start_game'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(testsuite_load_user_input())
    runner.run(testsuite_try_good_input_start_game())
    runner.run(testsuite_try_bad_input_name_start_game())
    runner.run(testsuite_try_not_enough_category_name_start_game())