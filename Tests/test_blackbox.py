import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
import random
import time
import itertools

#wrapper help functions to control the browser
import PlayGameUtil
import logging

'''
    The TestBlackboxGame class is the base and used for setup

    Then testsuite is used because Unittest execute the test cases in alphabetical order
    Testsuite can specify the test cases to run in a certain order. This will come in handy
    when testing the game play flow.
'''

#setting up the logging for test results
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('test_black_box.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


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
        # cls.driver = webdriver.Chrome(chrome_options=options)
        cls.driver = webdriver.Firefox()
        cls.driver.get('file:///' + cls.game_path)
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

        #make sure each price is 200+i*200 and is present, where i is the row starting from zero
        for column in prices:
            for row,price in enumerate(column):
                self.assertEqual(price, '${0}'.format(200+row*200))

    def test_category_not_clickable(self):
        board = self.play_game_util.read_jeopardy_board()

        for category in board['categoyButtons']:
            text,is_enabled = category
            self.assertFalse(is_enabled)

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
    def test_random_game(self):
        # logger.info('Starting New Random Game Test ')
        # # logger.info('Visiting game at ' + self.game_path)
        # self.driver.get(self.game_path)
        # # check if wheel is in title
        # self.assertTrue('Wheel' == self.play_game_util.read_title_value())
        logger.info('Setting test_spins_left to 50')
        test_spins_left = 50

        #get player info at the start
        player_infos = self.play_game_util.read_player_info()

        #create a list of player tokens and scores
        player_scores = [0]*self.max_players
        player_tokens = [0]*self.max_players

        while True:
            #get current player index
            current_player_index = self.play_game_util.read_player_turn()
            #read the player name
            current_player_name = player_infos[current_player_index]['playerName']

            #spin the current player, wait 10 seconds for it to land
            self.play_game_util.do_spin_wheel()

            #get the question info and spin result
            question_info = self.play_game_util.read_question_info()
            spin_result = question_info['selectedCategory']

            logger.info('{0} spin : {1}'.format(current_player_name,spin_result))

            #check if the spin resulted in a message box
            if self.play_game_util.is_game_message_present():

                #try read message box, if enabled or not
                game_message_box = self.play_game_util.read_game_message()
                if game_message_box:
                    message = game_message_box['message']
                    logger.info('Message box: {0}'.format(message))

                    startRound2_button = self.driver.find_element_by_xpath('//*[@id="startRound2"]')
                    ok_button = self.driver.find_element_by_xpath('//*[@id="ok"]')

                    if ok_button.is_enabled() and ok_button.is_displayed():
                        ok_button.click()
                    if startRound2_button.is_enabled() and startRound2_button.is_displayed():
                        time.sleep(1000)
                        startRound2_button.click()

                    #check if the message is about player or opponents choice
                    if ('Player\'s Choice' in spin_result):
                        #check if the message contains the person name
                        self.assertTrue(current_player_name in message)

                        #make sure jeopardy_board is clickable
                        self.assertTrue(self.play_game_util.is_jeopardy_board_clickable())

                        try:
                            self.play_game_util.do_select_random_categoy()
                        except :
                            logger.info('Failed to select category')
                        logger.info('{0} picked a category'.format(current_player_name))

                    if ('Opponent\'s Choice' == spin_result):
                        players_cycle = itertools.cycle(range(0,self.max_players))
                        for x in range(0,current_player_index):
                            opponet_index = next(players_cycle)
                        #make sure message is has opponents name and current player name
                        #eg. Opponents's Choice! <opponentName>, please select a category for <currentPlayerName>!
                        opponet_name = player_infos[opponet_index]['playerName']
                        self.assertTrue(player_infos[opponet_index]['playerName'] in message)
                        self.assertTrue(current_player_name in message)
                        logger.info('{0} selecting a category for {1}'.format(opponet_name,current_player_name))

                        # make sure jeopardy_board is clickable
                        self.assertTrue(self.play_game_util.is_jeopardy_board_clickable())
                        try:
                            self.play_game_util.do_select_random_categoy()
                        except :
                            logger.info('Failed to select category')
                        logger.info('{0} picked a category'.format(opponet_name))

                    if ('Bankrupt' in message):
                        #only reset player score if they are above zero
                        if player_scores[current_player_index] > 0:
                            player_scores[current_player_index] = 0
                            logger.info('{0} score was set to 0'.format(current_player_name))
                        time.sleep(10)

                    if ('won a free spin token' in message):
                        player_tokens[current_player_index] = player_tokens[current_player_index] + 1
                        logger.info('{0} has {1} tokens'.format(current_player_name, player_tokens[current_player_index]))

            #Check for answer prompt
            if self.play_game_util.is_select_answer_present():
                question_info = self.play_game_util.read_question_info()
                question = question_info['selectedQuestion']
                category = question_info['selectedCategory']
                #log the information
                logger.info(u'Category: {0}'.format(category))
                logger.info(u'Question: {0}'.format(question))

                #randomly pick if correct or incorrect
                random_answer = [True,False]
                answer = random.choice(random_answer)
                if answer:
                    logger.info('{0} answered correct!'.format(current_player_name))
                    self.play_game_util.do_answer_correct()

                else:
                    logger.info('{0} answered incorrect!'.format(current_player_name))
                    self.play_game_util.do_answer_incorrect()


            #Check token use prompt
            if self.play_game_util.is_use_token_popup_present():
                #make sure player has at least one token to use to even get this popup
                self.assertTrue(player_tokens[current_player_index] > 0)
                use_token_random = [True, False]
                use_token = random.choice(use_token_random)
                if use_token:
                    self.play_game_util.do_use_token_yes()
                    logger.info('{0} : {1}'.format(current_player_name, message))
                    logger.info('{0} : selected to use free spin token'.format(current_player_name))
                    player_tokens[current_player_index] = player_tokens[current_player_index] - 1
                    logger.info('{0} has {1} tokens'.format(current_player_name, player_tokens[current_player_index]))
                else:
                    self.play_game_util.do_use_token_no()
                    logger.info('{0} : {1}'.format(current_player_name, message))
                    logger.info('{0} : selected not to use free spin token'.format(current_player_name))
                    logger.info('{0} has {1} tokens'.format(current_player_name, player_tokens[current_player_index]))

            # each spin should decreemnt spins left
            test_spins_left = test_spins_left - 1
            logger.info('{0} spins left'.format(test_spins_left))
            # read game and get spins left
            state_indecators = self.play_game_util.read_state_indicators()
            actual_spins = state_indecators['spinsLeft']

            # test actual and test spins left
            self.assertEqual(actual_spins, test_spins_left)

def testsuite_TestRandomGame():
    suite = unittest.TestSuite()
    # suite.addTest(TestRandomGame('test_game_started'))
    suite.addTest(TestRandomGame('test_random_game'))
    return suite

if __name__ == '__main__':
    # unittest.main()
    # loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(failfast=True)
    # runner.run(testsutie_TestOpenNewGame())
    runner.run(testsuite_TestRandomGame())