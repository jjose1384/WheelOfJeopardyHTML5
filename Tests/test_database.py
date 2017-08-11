import unittest
import os
import json
from difflib import SequenceMatcher

class TestJsonDatabase(unittest.TestCase):

    #setup for test, run before every test
    def setUp(self):
        #set the database path
        self.database_path = os.path.join('..','database.json')

        #acess and read database
        #see if database path exist
        if(os.path.exists(self.database_path)):
            #try and prase database and see if it is a valid json format
            self.assertRaises(json.load(open(self.database_path)))
            #if valid put it into self.databse for reference in other test
            with open(self.database_path) as fp:
                self.database = json.load(fp)
            self.assertIsNotNone(self.database)

            '''
            database format for reference:
                {
                    "Category": {
                        "doubleJeopardy": {
                            "category1": {
                                ...
                            }
                        }
                        "singleJeopardy": {
                            "category1": {
                                ...
                            }
                        }
                    }
            '''

            #check if database has Category keyword and make sure it is not empty
            self.assertTrue('Category' in self.database.keys())
            self.database_jeopardy_rounds = self.database['Category']
            self.assertIsNotNone(self.database_jeopardy_rounds)

            # make sure has both a double and a single jeopardy
            self.assertEqual(len(self.database_jeopardy_rounds), 2)

            #check if doubleJeopardy exist
            self.assertTrue('doubleJeopardy' in self.database_jeopardy_rounds.keys())
            self.database_double_jeopardy = self.database_jeopardy_rounds['doubleJeopardy']
            self.assertIsNotNone(self.database_double_jeopardy)

            #check if singlJeopardy exists
            self.assertTrue('singleJeopardy' in self.database_jeopardy_rounds.keys())
            self.database_single_jeopardy = self.database_jeopardy_rounds['singleJeopardy']
            self.assertIsNotNone(self.database_single_jeopardy)
        else:
            self.assertTrue(os.path.exists(self.database_path))

    # #check if database file exist a directory up
    # def test_database_exist(self):
    #     #test correct database path
    #     self.assertTrue(os.path.exists(self.database_path))
    #     # #test incorrect database path
    #     # self.assertFalse(os.path.exists(self.database_path + 'wrong'))
    #
    # #checking database is a valid json format
    # def test_read_database(self):
    #     with open(self.database_path) as fp:
    #         self.assertRaises(json.load(fp))
    #
    # #check if database has jeopardy_rounds:
    # def test_has_category(self):
    #     with open(self.database_path) as fp:
    #         database = json.load(fp)
    #     self.assertTrue('Category' in database.keys())
    #     self.assertTrue('doubleJeopardy' in database['Category'].keys())
    #     self.assertTrue('singleJeopardy' in database['Category'].keys())

    #check if database has at least one doubleJeopardy
    def test_has_doubleJeopardy(self):
        #make sure doubleJeopardy has at least one category in it and
        self.assertIsNotNone(self.database_double_jeopardy)
        self.assertEqual(len(self.database_double_jeopardy),1)

        #get the first category of double jeopardy
        double_jeopardy_categories = self.database_double_jeopardy.keys()
        self.assertIsNotNone(double_jeopardy_categories)
        double_jeopardy_first_category = self.database_double_jeopardy[double_jeopardy_categories[0]]
        self.assertIsNotNone(double_jeopardy_first_category)
        double_jeopardy_first_category_name = double_jeopardy_first_category.keys()[0]

        #check questions has at least 5 questions
        questions = double_jeopardy_first_category[double_jeopardy_first_category_name]
        self.assertGreaterEqual(len(questions), 5)

        for q_number in questions:
            question = questions[q_number]['question']
            #check has one question and is a string
            self.assertTrue(isinstance(question,str) or isinstance(question,unicode) )
            #check has one answer
            answer = questions[q_number]['question']
            self.assertTrue(isinstance(answer, str) or isinstance(answer, unicode))
            #check has at least 4 wrong answers
            self.assertGreaterEqual(len(questions[q_number]['wrong_answers']), 4)


        # check if database has at least one singleJeopardy
        def test_has_singleJeopardy(self):
            # make sure doubleJeopardy has at least one category in it and
            self.assertIsNotNone(self.database_single_jeopardy)
            self.assertGreaterEqual(len(self.database_single_jeopardy), 5)

            # get the first category of double jeopardy
            single_jeopardy_categories =self.database_single_jeopardy.keys()
            self.assertIsNotNone(single_jeopardy_categories)
            single_jeopardy_first_category = self.database_single_jeopardy[single_jeopardy_categories[0]]
            self.assertIsNotNone(single_jeopardy_first_category)
            single_jeopardy_first_category_name = single_jeopardy_first_category.keys()[0]

            # check questions has at least 5 questions
            questions = single_jeopardy_first_category[single_jeopardy_first_category_name]
            self.assertGreaterEqual(len(questions), 5)

            for q_number in questions:
                question = questions[q_number]['question']
                # check has one question and is a string
                self.assertTrue(isinstance(question, str) or isinstance(question, unicode))
                # check has one answer
                answer = questions[q_number]['question']
                self.assertTrue(isinstance(answer, str) or isinstance(answer, unicode))
                # check has at least 4 wrong answers
                self.assertGreaterEqual(len(questions[q_number]['wrong_answers']), 4)

    def test_has_all_questions_has_answer_and_wrong_answers(self):
        '''
        database format for reference:

            "doubleJeopardy": {
                "category1": {
                    "Solar System": {
                        "question1": {
                            ...
                        }
                        "question2": {
                            ...
                        }
                    }
                }
            }
            "singleJeopardy": {
                "category1": {
                    "Potent Potables": {
                        "question1": {
                            ...
                        }
                        "question2": {
                            ...
                        }
                    }
                }
            }
        '''

        #get categories number for double_jeopardy
        double_jeopardy_categories = self.database_double_jeopardy.keys()
        for category_number in double_jeopardy_categories:
            #check has at least 5 questions in each category
            number_questions = len(self.database_double_jeopardy[category_number])
            print(number_questions)
        # get categories number for single_jeopardy
        single_jeopardy_categories = self.database_single_jeopardy.keys()
        for category_number in single_jeopardy_categories:
            # check has at least 5 questions in each category
            number_questions = len(self.database_single_jeopardy[category_number])
            print(number_questions)


    def test_has_atleast_10_category(self):
        #make sure database has at least 10 category
        double_jeopardy_categories = self.database_double_jeopardy.keys()
        number_double_jeopardy_categories = len(double_jeopardy_categories)
        single_jeopardy_categories = self.database_single_jeopardy.keys()
        number_single_jeopardy_categories = len(single_jeopardy_categories)
        self.assertGreaterEqual(10, number_double_jeopardy_categories + number_single_jeopardy_categories)

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()