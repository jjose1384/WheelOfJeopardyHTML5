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
                    "doubleJeopardy": [
                        {
                            "category_name": "Solar System", 
                            "category_number": "category1", 
                            "questions": [
                                ...
                            ]
                        },
                        {
                            ...
                        }
                    ],
                    "singleJeopardy": [
                        {
                            "category_name": "Solar System", 
                            "category_number": "category1", 
                            "questions": [
                                ...
                            ]
                        }
                    ]
                }
                
            '''

            #check if database has Category keyword and make sure it is not empty
            rounds = self.database.keys()
            # make sure has both a double and a single jeopardy
            self.assertEqual(len(rounds), 2)

            #check if doubleJeopardy exist
            self.assertTrue('doubleJeopardy' in rounds)
            self.database_double_jeopardy = self.database['doubleJeopardy']
            self.assertIsNotNone(self.database_double_jeopardy)

            #check if singlJeopardy exists
            self.assertTrue('singleJeopardy' in rounds)
            self.database_single_jeopardy = self.database['singleJeopardy']
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

    #check if database has at least one doubleJeopardy and check it has category_number, category_name, and questions
    def test_has_doubleJeopardy_categories(self):
        #make sure doubleJeopardy has at least one category in it and
        self.assertIsNotNone(self.database_double_jeopardy)
        self.assertGreaterEqual(len(self.database_double_jeopardy),1)

        #check each category in double_jeopardy has a category_number, category_name, and questions
        double_categories = self.database_double_jeopardy
        for double_category in double_categories:
            #make sure that category has a number
            self.assertIsNotNone(double_category['category_number'])
            #make sure the category has category_name
            self.assertIsNotNone(double_category['category_name'])
            #make sure the category has questions
            self.assertIsNotNone(double_category['questions'])


    # check if database has at least one singleJeopardy and check it has category_number, category_name, and questions
    def test_has_singleJeopardy_categories(self):
        # make sure doubleJeopardy has at least one category in it and
        self.assertIsNotNone(self.database_single_jeopardy)
        self.assertGreaterEqual(len(self.database_single_jeopardy), 1)

        # check each category in single_jeopardy has a category_number, category_name, and questions
        single_categories = self.database_single_jeopardy
        for single_category in single_categories:
            # make sure that category has a number
            self.assertIsNotNone(single_category['category_number'])
            # make sure the category has category_name
            self.assertIsNotNone(single_category['category_name'])
            # make sure the category has questions
            self.assertIsNotNone(single_category['questions'])


    #check that all categories has at least 5 questions, each question has the question, answer, and 4+ wrong answers
    def test_has_all_questions_has_answer_and_wrong_answers(self):
        '''
        database question format for reference:
            {
                ...
                {
                    "answer": "Neptune",
                    "number": "question5",
                    "question": "This panet is the coolest in our solar system.",
                    "wrong_answer": [
                        "Uranus",
                        "Pluto",
                        "Saturn",
                        "Jupiter",
                        "Mercury",
                        "Venus",
                        "Sun",
                        "Mars",
                        "Earth",
                        "Moon",
                        "Triton",
                        "Ceres",
                        "Milky Way",
                        "Eris",
                        "Titan"
                },

                ...
        '''

        #get questions for all double_jeopardy and single_jeopardy
        for rounds in self.database.keys():
            for category in self.database[rounds]:
                #make sure category has questions
                self.assertTrue('questions' in category)
                questions = category['questions']
                # make sure it has at least 5 questions
                self.assertGreaterEqual(len(questions), 5)

                for question in questions:
                    #make sure question has the question, answer, and wrong_answers
                    self.assertTrue('question' in question)
                    self.assertTrue('answer' in question)
                    self.assertTrue('wrong_answers' in question)
                    
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