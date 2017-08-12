import unittest
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

class TestBlackboxGame(unittest.TestCase):

    #ran once at the start of testsuite
    @classmethod
    def setUpClass(cls):
        cls.public_path = os.path.join('public', 'index.html')
        cls.game_path = os.path.abspath(os.path.join('..', cls.public_path))
        # make sure index.html path exist
        assert(os.path.exists(cls.game_path))

        cls.driver = webdriver.Chrome()

    #ran once after testing is done
    @classmethod
    def tearDownClass(cls):
        pass

    #setUp, ran once before each test
    def setUp(self):
        pass

    #tearDown, ran after each test case
    def tearDown(self):
        pass

    #open the game test for title == 'Wheel'
    def test_open_game(self):
        print('Visiting game at ' + self.game_path)
        self.driver.get(self.game_path)
        print(self.driver.title)
        self.assertTrue('Wheel' == self.driver.title)
        self.driver.quit()

    #open chrome, visit bing.com and search for "cheese!", check for cheese in title of result page, close chrome
    def test_selenium_start(self):
        # go to the google home page
        self.driver.get("http://www.bing.com")

        # the page is ajaxy so the title is originally this:
        print self.driver.title

        # find the element that's name attribute is q (the google search box)
        inputElement = self.driver.find_element_by_name("q")

        # type in the search
        inputElement.send_keys("cheese!")

        # submit the form (although google automatically searches now without submitting)
        inputElement.submit()

        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        # WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

        # You should see "cheese! - Google Search"
        self.assertTrue('cheese' in self.driver.title)

        self.driver.quit()

def testsuite_open_game():
    suite = unittest.TestSuite()
    suite.addTest(TestBlackboxGame('test_open_game'))
    return suite

if __name__ == '__main__':
    # unittest.main()
    # loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(testsuite_open_game())