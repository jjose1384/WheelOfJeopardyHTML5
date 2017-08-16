import unittest
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
import random
import PlayGameUtil
'''
    The TestBlackboxGame class is the base and used for setup
    
    Then testsuite is used because Unittest execute the test cases in alphabetical order
    Testsuite can specify the test cases to run in a certain order. This will come in handy
    when testing the game play flow.
'''

#basic test suite. Creates a webdriver.
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
        cls.driver.quit()

    #setUp, ran once before each test
    def setUp(self):
        pass

    #tearDown, ran after each test case
    def tearDown(self):
        pass


# test that time is set to zero, spin left = 50, player0Spin is active
class TestOpenNewGame(TestBlackboxGame):
    def test_game_started(self):
        print('Visiting game at ' + self.game_path)
        self.driver.get(self.game_path)
        #check if wheel is in title
        self.assertTrue('Wheel' == self.driver.title)

    #get Timer value
    def test_timer_zero(self):
        timer_value = self.driver.find_element_by_xpath('//*[@id="timer"]').text
        #check if Timer = zero
        self.assertEqual(int(timer_value),0)

    #check that the spin left is 50
    def test_spin_left_50(self):
        spins_left_value = self.driver.find_element_by_xpath('//*[@id="spinsLeft"]').text
        #check spins left is 50
        self.assertEqual(int(spins_left_value),50)

    #check player scores are zero
    def test_player_values_zero(self):
        '''
        player0Score = self.driver.find_element_by_xpath('//*[@id="player0Score"]')
        player1Score = self.driver.find_element_by_xpath('//*[@id="player1Score"]')
        player2Score = self.driver.find_element_by_xpath('//*[@id="player2Score"]')
        #check player score exists
        self.assertIsNotNone(player0Score)
        self.assertIsNotNone(player1Score)
        self.assertIsNotNone(player2Score)
        player0Score_value = int(player0Score.text)
        player1Score_value = int(player1Score.text)
        player2Score_value = int(player2Score.text)
        #check player scores all equal to zero
        self.assertEqual(player0Score_value, 0)
        self.assertEqual(player1Score_value, 0)
        self.assertEqual(player2Score_value, 0)
        '''

        #loop does the checks in the above
        for i in range(0,3):
            xpath = '//*[@id="player{0}Score"]'.format(i)
            playerScore = self.driver.find_element_by_xpath(xpath)
            self.assertIsNotNone(playerScore)
            playerScore_value = int(playerScore.text)
            self.assertEqual(playerScore_value, 0)


    #check player free spin token are zero
    def test_player_token_zero(self):
        for i in range(0,3):
            xpath = '//*[@id="player{0}Tokens"]'.format(i)
            playerScore = self.driver.find_element_by_xpath(xpath)
            self.assertIsNotNone(playerScore)
            playerScore_value = int(playerScore.text)
            self.assertEqual(playerScore_value, 0)

    def test_player0_turn(self):
        '''
        player0Spin = self.driver.find_element_by_xpath('// *[ @ id = "player0Spin"]')
        player1Spin = self.driver.find_element_by_xpath('// *[ @ id = "player1Spin"]')
        player2Spin = self.driver.find_element_by_xpath('// *[ @ id = "player2Spin"]')

        #make sure player spin button exists
        self.assertIsNotNone(player0Spin)
        self.assertIsNotNone(player1Spin)
        self.assertIsNotNone(player2Spin)
        # player0Spin_attruibute = player0Spin.get_attribute('innerHTML')
        # player1Spin_attruibute = player1Spin.get_attribute('innerHTML')
        # player2Spin_attruibute = player2Spin.get_attribute('innerHTML')

        #make sure only player0Spin is enabled
        self.assertTrue(player0Spin.is_enabled())
        self.assertFalse(player1Spin.is_enabled())
        self.assertFalse(player2Spin.is_enabled())
        '''

        player0Spin = self.driver.find_element_by_xpath('// *[ @ id = "player0Spin"]')
        self.assertIsNotNone(player0Spin)
        self.assertTrue(player0Spin.is_enabled())

        #loop version of the commited code above
        for i in range(1,3):
            xpath = '// *[ @ id = "player{0}Spin"]'.format(i)
            playerSpin = self.driver.find_element_by_xpath(xpath)
            self.assertIsNotNone(playerSpin)
            self.assertFalse(playerSpin.is_enabled())

def testsutie_TestOpenNewGame():
    suite = unittest.TestSuite()
    suite.addTest(TestOpenNewGame('test_game_started'))
    suite.addTest(TestOpenNewGame('test_timer_zero'))
    suite.addTest(TestOpenNewGame('test_spin_left_50'))
    suite.addTest(TestOpenNewGame('test_player_values_zero'))
    suite.addTest(TestOpenNewGame('test_player0_turn'))
    return suite

class TestFirstPlayer(TestBlackboxGame):
    def test_player_spinable(self):
        #make sure there is 3 spinner buttons, player0Spin, player1Spin, player2Spin
        for player_number in range(0,3):
            spin_id = 'player{0}Spin'.format(player_number)
            assert(self.driver.find_element_by_id(spin_id))

class TestRandomGame(TestBlackboxGame):
    def test_game_started(self):
        print('Visiting game at ' + self.game_path)
        self.driver.get(self.game_path)
        #check if wheel is in title
        self.assertTrue('Wheel' == self.driver.title)

    def test_get_question(self):
        game_util = PlayGameUtil.GameUtil(self.driver)
        print(game_util.read_player_turn())
        print(game_util.read_state_indicators())
        print(game_util.read_player_info())
        print(game_util.read_question_info())
        print(game_util.do_spin_wheel())
        question_info = game_util.read_question_info()
        question = question_info['selectedQuestion']
        category = question_info['selectedCategory']
        print(game_util.pick_wrong_answer(question,category))
    def test_play_game_random(self):
        raise NotImplementedError

def testsuite_TestRandomGame():
    suite = unittest.TestSuite()
    suite.addTest(TestRandomGame('test_game_started'))
    suite.addTest(TestRandomGame('test_get_question'))
    # suite.addTest(TestRandomGame('test_play_game_random'))
    return suite

if __name__ == '__main__':
    # unittest.main()
    # loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(failfast=True)
    # runner.run(testsutie_TestOpenNewGame())
    runner.run(testsuite_TestRandomGame())