'''
Utility library of helper functions for playing the game. Such as selecting wrong answer,
connecting to database to pick right answer or picking the wrong answer,
and spinng.
'''

import random
import json
import os
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
#import helper functions to control the game

class GameUtil(object):
    def __init__(self, driver, max_player = 3):
        self.driver = driver
        self.max_player = max_player

        #database to questions
        self.database_path = os.path.join('..', 'database.json')
        if (os.path.exists(self.database_path)):
            # if valid put it into self.databse for reference in other test
            with open(self.database_path) as fp:
                self.database = json.load(fp)

        self.database_get_all_categories()

    ###Database helper functions
    '''
        get all categories and questions into a dictionary for faster referencing
    '''
    def database_get_all_categories(self):
        self.categories = {}
        for round in self.database.keys():
            for categories in self.database[round]:
                category_number = categories['category_number']
                '''
                    to_do:
                        update categories by name instead of numbers
                '''
                if category_number not in self.categories.keys():
                    self.categories[category_number] = []
                self.categories[category_number].append(categories)

    def get_all_categories(self):
        return self.categories

    ###Game logic helper functions

    #return a random number to pick a random answer choice
    def pick_random_answer(self):
        raise NotImplementedError
        return random.randint(0,4)

    #should connect to database and retrun a choice that is not the right answer
    def pick_wrong_answer(self, question, category):
        category = self.categories[category][0]
        print(category)

    def pick_right_answer(self, question, category):
        raise NotImplementedError

    ###WebDriver related helper functions

    '''
        spin wheel for current player or specify a player index 0...max_player
    '''
    def do_spin_wheel(self, player_number = None):
        if player_number == None:
            #read the board and see who the current player is
            player_number = self.read_player_turn()
            self.driver.find_element_by_xpath('// *[ @ id = "player{0}Spin"]'.format(player_number)).click()
            #wait for wheel to stop spinning. timeout + 1
            # WebDriverWait(self.driver, 11).until(
            #     lambda driver: driver.find_element(By.ID, "incorrectButton").is_enabled()
            #                    or driver.find_element(By.ID, "correctButton").is_enabled()
            #                    or driver.find_element(By.ID, "messageModal").is_displayed()
            #                    or driver.find_element(By.ID, "gameMessage").is_displayed()
            #                    or driver.find_element(By.ID, "useTokenModal").is_displayed())
            time.sleep(11)
        return True

    '''
        return if click was sucessful
        accept answer as incorrect
    '''
    def do_answer_incorrect(self):
        incorrect_button = self.driver.find_element_by_xpath('//*[@id="incorrectButton"]')

        # if not clickable return error
        if incorrect_button.is_enabled():
            incorrect_button.click()
            return True
        else:
            return False

    '''
        return if click was sucessful
        accept answer as correct
    '''
    def do_answer_correct(self):
        correct_button = self.driver.find_element_by_xpath('//*[@id="correctButton"]')

        #if not clickable return error
        if correct_button.is_enabled():
            correct_button.click()
            return True
        else:
            return False


    '''
        return if click was timeExpiredButton
        click timeExpiredButton
    '''
    def do_time_expired(self):
        expired_button = self.driver.find_element_by_xpath('//*[@id="timeExpiredButton"]')

        #if not clickable return error
        if expired_button.is_enabled():
            expired_button.click()
            return True
        else:
            return False

    '''
        return if answer select screen
    '''
    def is_select_answer_present(self):
        incorrect_button = self.driver.find_element_by_xpath('//*[@id="incorrectButton"]')
        correct_button = self.driver.find_element_by_xpath('//*[@id="correctButton"]')
        expired_button = self.driver.find_element_by_xpath('//*[@id="timeExpiredButton"]')
        if incorrect_button.is_enabled() or correct_button.is_enabled() or expired_button.is_enabled():
            return True
        else:
            return False
    '''
        click on a random categorybutton
    '''
    def do_select_random_categoy(self):
        #get element of id = categoryButtonId
        board = self.read_jeopardy_board()
        categoryButtons = board['categoyButtons']

        #get index of all category buttons that are enabled
        enabled_buttons = []
        for index,categoryButton in enumerate(categoryButtons):
            name,is_enabled = categoryButton
            if is_enabled:
                enabled_buttons.append(index)
        random_button_number = random.choice(enabled_buttons)
        self.do_select_categoy('categoryButton{0}'.format(random_button_number))
        return True

    '''
        click on categorybutton
    '''
    def do_select_categoy(self, categoryButtonId):
        wait = WebDriverWait(self.driver, 5)
        #get element of id = categoryButtonId
        xpath = '//*[@id="{0}"]'.format(categoryButtonId)
        categoryButton = self.driver.find_element_by_xpath(xpath)
        if categoryButton.is_enabled() and categoryButton.is_displayed():
            categoryButton.click()
        return True

    '''
        return the state indicators such as current_player_turn, spins_left, round#
    '''
    def read_state_indicators(self):
        state_indicators = {}

        while( any([key not in state_indicators.keys() for key in ['currentPlayer','spinsLeft','roundNumber']]) ):
            try:
                #get each element by id
                current_player = self.driver.find_element_by_xpath('//*[@id="currentPlayerName"]')
                spins_left = self.driver.find_element_by_xpath('//*[@id="spinsLeft"]')
                round_number = self.driver.find_element_by_xpath('//*[@id="roundNumber"]')

                state_indicators['currentPlayer'] = current_player.text
                state_indicators['spinsLeft'] = int(spins_left.text)
                state_indicators['roundNumber'] = int(round_number.text)
            except:
                print('Could\'t find all the state indecaitors')
        return state_indicators

    '''
        return the question_info such as category, question, and answer
    '''
    def read_question_info(self):
        question_info = {}
        while (any([key not in question_info.keys() for key in ['selectedCategory', 'selectedQuestion', 'answer']])):
            try:
                selected_category = self.driver.find_element_by_xpath('//*[@id="selectedCategory"]')
                selected_question = self.driver.find_element_by_xpath('//*[@id="selectedQuestion"]')
                answer = self.driver.find_element_by_xpath('//*[@id="answer"]')

                question_info['selectedCategory'] = selected_category.text
                question_info['selectedQuestion'] = selected_question.text
                question_info['answer'] = answer.text

                self.question_info = question_info
            except:
                print('Could\'t find all the question_info')
        return  question_info

    '''
        return all spinner status enable/disabled
    '''
    def read_spiner_status(self):
        spiner_status = []
        for i in range(0, self.max_player):
            try:
                # get each element by id
                xpath = '// *[ @ id = "player{0}Spin"]'.format(i)
                playerSpin = self.driver.find_element_by_xpath(xpath)
                #add to boolen list if spinner is enabled
                spiner_status.append(playerSpin.is_enabled())
            except:
                print('Could not find state info')

        return spiner_status

    '''
        return the current player number 0...to...max_player
        read all spin button and see which one is enabled. Compare with the current player turn according to the board
    '''
    def read_player_turn(self):
        enabled_player = None
        while (enabled_player == None):
            try:
                for i in range(0, self.max_player):
                    # get each element by id
                    xpath = '// *[ @ id = "player{0}Spin"]'.format(i)
                    playerSpin = self.driver.find_element_by_xpath(xpath)
                    #set enabled_player to i if their spin is enabled
                    if playerSpin.is_enabled():
                        if enabled_player:
                            #found multiple player with spin enabled
                            raise ValueError
                        else:
                            enabled_player = i
            except:
                print('Couldn\'t find a player with spinner enabled')

        # #check if we found at least one. If not found, raise exception
        # if enabled_player == None:
        #     raise ValueError

        #double checking with state indecators "Players {playerName}'s turn"
        state_indecators = self.read_state_indicators()
        current_player = state_indecators['currentPlayer']
        #subtracting 'Player ' from the string
        current_player.replace('Player ','')
        current_player.replace('\'s turn','')

        player_infos = self.read_player_info()
        for player in player_infos:
            if player['playerName'] == current_player:
                return enabled_player

        #if the current_player does not match with the spin enabled, raise error
        raise ValueError

    '''
        return a list of players info (name, score, Free spin tokens)
    '''
    def read_player_info(self):
        player_infos = []
        #keep trying to get all max_player info
        while (not player_infos) and (len(player_infos) < self.max_player):
            try:
                for i in range(0, self.max_player):
                    xpath_name = '// *[ @ id = "player{0}Name"]'.format(i)
                    xpath_score = '// *[ @ id = "player{0}Score"]'.format(i)
                    xpath_tokens = '// *[ @ id = "player{0}Tokens"]'.format(i)
                    player_info = {}
                    # get the values
                    player_name = self.driver.find_element_by_xpath(xpath_name)
                    player_score = self.driver.find_element_by_xpath(xpath_score)
                    player_tokens = self.driver.find_element_by_xpath(xpath_tokens)
                    player_info['playerName'] = player_name.text
                    player_info['playerScore'] = int(player_score.text)
                    player_info['playerToken'] = int(player_tokens.text)
                    player_infos.append(player_info)
            except:
                player_infos = []
                print('Failed to get all {0} players info'.format(self.max_player))
        return player_infos

    '''
        return if the jeopardy board category is clickable
    '''
    def is_jeopardy_board_clickable(self):
        for i in range(0,5):
            xpath = '//*[@id="categoryButton{0}"]'.format(i)
            category_button = self.driver.find_element_by_xpath(xpath)
            #if one of the category is not clickable return False
            if (not category_button.is_enabled()) or (not category_button.is_displayed()):
                return False

        #all is clickable return True
        return True

    '''
        read the jeopardy board
    '''
    def read_jeopardy_board(self):

        #get all category buttons
        category_buttons = []
        for i in range(0,5):
            xpath = '//*[@id="categoryButton{0}"]'.format(i)
            category_button = self.driver.find_element_by_xpath(xpath)
            category_buttons.append((category_button.text,category_button.is_enabled()))

        all_prices = []
        #get all prices
        for i in range(0,5):
            category_prices = []
            for j in range(0,5):
                xpath = '//*[@id="valueC{0}Q{1}"]'.format(i,j)
                category_price = self.driver.find_element_by_xpath(xpath)
                category_prices.append(category_price.text)
            all_prices.append(category_prices)

        board = {}
        board['categoyButtons'] = category_buttons
        board['prices'] = all_prices
        return board

    '''
        return the timer value
    '''
    def read_timer_value(self):
        xpath_timer = '//*[@id="timer"]'
        try:
            # get the values
            timer = self.driver.find_element_by_xpath(xpath_timer)
            timer_value = timer.text
        except ValueError:
            print('Could not find timer ')
        return timer_value

    '''
        return the title
    '''
    def read_title_value(self):
        return self.driver.title

    '''
        return if game message box is present
    '''
    def is_game_message_present(self):
        # wait = WebDriverWait(self.driver, 1)
        game_message_dialog = self.driver.find_element_by_xpath('//*[@id="messageModal"]')
        return game_message_dialog.is_displayed()

    '''
        return game message box information such as message and buttons (selenium element)
    '''
    def read_game_message(self):
        # wait = WebDriverWait(self.driver, 1)
        if self.is_game_message_present():
            game_message_box = {}
            game_message = self.driver.find_element_by_xpath('//*[@id="gameMessage"]')
            game_message_text = game_message.text
            game_message_box['message'] = game_message_text

            #buttons section
            button_footer = self.driver.find_elements_by_class_name('modal-footer')
            buttons = []
            for button in button_footer:
                buttons.append(button)
            game_message_box['buttons'] = buttons

            return game_message_box
        else:
            return None


    '''
        return if use token pupup is present
    '''
    def is_use_token_popup_present(self):
        time.sleep(2)
        popup_header_dialog = self.driver.find_element_by_xpath('//*[@id="useTokenModal"]')
        return popup_header_dialog.is_displayed()

    '''
        click yes on using free token
    '''
    def do_use_token_yes(self):
        yes_button = self.driver.find_element_by_xpath('//*[@id="useTokenYes"]')
        if yes_button.is_enabled() and yes_button.is_displayed():
            yes_button.click()
            return True
        else:
            return False

    '''
        click no on using free token
    '''
    def do_use_token_no(self):
        no_button = self.driver.find_element_by_xpath('//*[@id="useTokenNo"]')
        if no_button.is_enabled() and no_button.is_displayed():
            no_button.click()
            return True
        else:
            return False
if __name__ == '__main__':
    pass