import unittest
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
import random

#wrapper help functions to control the browser
import PlayGameUtil


'''
    The TestBlackboxGame class is the base and used for setup
    
    Then testsuite is used because Unittest execute the test cases in alphabetical order
    Testsuite can specify the test cases to run in a certain order. This will come in handy
    when testing the game play flow.
'''

#basic test suite. Creates a webdriver and a PlayGameUtil object to be used for interating with game
class TestBlackboxGame(unittest.TestCase):
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

        cls.play_game_util = PlayGameUtil.GameUtil(cls.driver, cls.max_players)

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
        self.driver.get(self.game_path)
        #check if wheel is in title
        self.assertTrue('Wheel' == self.play_game_util.read_title_value())

    #get Timer value
    def test_timer_zero(self):
        timer_value = self.play_game_util.read_timer_value()
        #check if Timer = zero
        self.assertEqual(int(timer_value),0)

    #check that the spin left is 50
    def test_spin_left_50(self):
        state_indicators = self.play_game_util.read_state_indicators()
        spins_left_value = state_indicators['spinsLeft']
        #check spins left is 50
        self.assertEqual(spins_left_value,50)

    #check player scores are zero
    def test_player_values_zero(self):
        player_infos = self.play_game_util.read_player_info()
        #loop through each player and check score
        for player in player_infos:
            self.assertEqual(player['playerScore'],0)

    #check player free spin token are zero
    def test_player_token_zero(self):
        player_infos = self.play_game_util.read_player_info()
        #loop through each player and check free tokens
        for player in player_infos:
            self.assertEqual(player['playerToken'],0)

    def test_player0_turn(self):
        spinner_status = self.play_game_util.read_spiner_status()
        #check if first player is spinable
        self.assertTrue(spinner_status[0])

        #the rest of the spinners should be disabled
        for spinner in spinner_status[1:]:
            self.assertFalse(spinner)

        #should return that player0 should be the current player
        self.assertEqual(self.play_game_util.read_player_turn(),0)

    #check selected category, selected question, and answer should be empty:
    def test_question_info_empty(self):
        question_info = self.play_game_util.read_question_info()
        #empty string should be false
        self.assertFalse(question_info['selectedCategory'])
        self.assertFalse(question_info['selectedQuestion'])
        self.assertFalse(question_info['answer'])

    def test_state_indicators(self):
        state_indicators = self.play_game_util.read_state_indicators()
        self.assertEqual(state_indicators['spinsLeft'],50)
        self.assertEqual(state_indicators['roundNumber'],1)
        player_infos = self.play_game_util.read_player_info()
        player0_name = player_infos[0]['playerName']
        #check player's turn indicator is correct
        self.assertEqual(state_indicators['currentPlayer'],player0_name)

    def test_correct_not_clickable(self):
        self.assertFalse(self.play_game_util.do_answer_correct())

    def test_incorrect_not_clickable(self):
        self.assertFalse(self.play_game_util.do_answer_incorrect())

    def test_time_expired_not_clickable(self):
        self.assertFalse(self.play_game_util.do_time_expired())

    def test_all_prices(self):
        board = self.play_game_util.read_jeopardy_board()
        prices = board['prices']

        #make sure each price is 200+i*200, where i is the row starting from zero
        for column in prices:
            for row,price in enumerate(column):
                self.assertEqual(price, '${0}'.format(200+row*200))

#suite used to run the TestOpenNewGame in order
def testsutie_TestOpenNewGame():
    suite = unittest.TestSuite()
    suite.addTest(TestOpenNewGame('test_game_started'))
    suite.addTest(TestOpenNewGame('test_timer_zero'))
    suite.addTest(TestOpenNewGame('test_spin_left_50'))
    suite.addTest(TestOpenNewGame('test_player_values_zero'))
    suite.addTest(TestOpenNewGame('test_player0_turn'))
    suite.addTest(TestOpenNewGame('test_question_info_empty'))
    suite.addTest(TestOpenNewGame('test_state_indicators'))
    suite.addTest(TestOpenNewGame('test_correct_not_clickable'))
    suite.addTest(TestOpenNewGame('test_incorrect_not_clickable'))
    suite.addTest(TestOpenNewGame('test_time_expired_not_clickable'))
    suite.addTest(TestOpenNewGame('test_all_prices'))
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
        self.assertTrue('Wheel' == self.play_game_util.read_title_value())

    def test_get_question(self):
        game_util = PlayGameUtil.GameUtil(self.driver)
        print(game_util.read_player_turn())
        print(game_util.read_state_indicators())
        print(game_util.read_player_info())
        print(game_util.read_jeopardy_board())
        print(game_util.read_question_info())
        while True:
            print(game_util.do_spin_wheel())
            question_info = game_util.read_question_info()
            question = question_info['selectedQuestion']
            category = question_info['selectedCategory']
        # print(game_util.pick_wrong_answer(question,category))
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
    runner.run(testsutie_TestOpenNewGame())
    runner.run(testsuite_TestRandomGame())