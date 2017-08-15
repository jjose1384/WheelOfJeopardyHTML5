'''
Utility library of helper functions for playing the game. Such as selecting wrong answer,
connecting to database to pick right answer or picking the wrong answer,
and spinng.
'''

from random import randint
import json
import os
from selenium import webdriver

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

                self.categories['']

    ###Game logic helper functions

    #return a random number to pick a random answer choice
    def pick_random_answer(self):
        return randint(0,4)

    #should connect to database and retrun a choice that is not the right answer
    def pick_wrong_answer(self, question, category):
        raise NotImplementedError

    def pick_right_answer(self, question, category):
        raise NotImplementedError

    ###WebDriver related helper functions
    '''
        return the state indicators such as current_player_turn, spins_left, round#
    '''
    def read_state_indicators(self):
        state_indicators = {}
        try:
            #get each element by id
            current_player = self.driver.find_element_by_xpath('//*[@id="currentPlayerName"]')
            spins_left = self.driver.find_element_by_xpath('//*[@id="spinsLeft"]')
            round_number = self.driver.find_element_by_xpath('//*[@id="roundNumber"]')
        except:
            print('Could not find state info')

        state_indicators['currentPlayer'] = current_player.text
        state_indicators['spinsLeft'] = spins_left.text
        state_indicators['roundNumber'] = round_number.text

        return state_indicators

    '''
        return the question_info such as category, question, and answer
    '''
    def read_question_info(self):
        question_info = {}
        try:
            selected_category = self.driver.find_element_by_xpath('//*[@id="selectedCategory"]')
            selected_question = self.driver.find_element_by_xpath('//*[@id="selectedQuestion"]')
            answer = self.driver.find_element_by_xpath('//*[@id="answer"]')
        except:
            print('Could not find state info')

        question_info['selectedCategory'] = selected_category.text
        question_info['selectedQuestion'] = selected_question.text
        question_info['answer'] = answer.text

        self.question_info = question_info
        return  question_info
    '''
        return the current player number 0...to...max_player
    '''
    def read_player_turn(self):
        for i in range(0,self.max_player):
            xpath = '// *[ @ id = "player{0}Spin"]'.format(i)
            try:
                playerSpin = self.driver.find_element_by_xpath(xpath)
            except:
                print('Could not find player {0} info'.format(str(i)))

            if playerSpin.is_enabled():
                return i

    '''
        return a list of players info (name, score, Free spin tokens)
    '''
    def read_player_info(self):
        player_infos = []
        for i in range(0, self.max_player):
            xpath_name = '// *[ @ id = "player{0}Name"]'.format(i)
            xpath_score = '// *[ @ id = "player{0}Score"]'.format(i)
            xpath_tokens = '// *[ @ id = "player{0}Tokens"]'.format(i)
            player_info = {}
            try:
                #get the values
                player_name = self.driver.find_element_by_xpath(xpath_name)
                player_score = self.driver.find_element_by_xpath(xpath_score)
                player_tokens = self.driver.find_element_by_xpath(xpath_tokens)
                player_info['playerName'] = player_name.text
                player_info['playerScore'] = player_score.text
                player_info['playerToken'] = player_tokens.text
                player_infos.append(player_info)
            except ValueError:
                print('Could not find player ' + str(i))
        return player_infos


if __name__ == '__main__':
    pass