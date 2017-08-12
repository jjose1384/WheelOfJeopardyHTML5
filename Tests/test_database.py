import unittest
import os
import json
from difflib import SequenceMatcher

#return probability a and b are similar
#used for filtering out wrong_answers that are similar to the answer
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#get only letters of word
#used with similar to find the probability that words are similar to each other
def letters(input):
    valids = []
    for character in input.lower():
        if character.isalpha():
            valids.append(character)
    return ''.join(valids)

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

                for question_data in questions:
                    #make sure question has the question, answer, and wrong_answers
                    self.assertTrue('question' in question_data)
                    self.assertTrue('answer' in question_data)
                    self.assertTrue('wrong_answers' in question_data)

                    #make sure question, answer, wrong_answers are not empty
                    question_text = question_data['question']
                    question_answer = question_data['answer']
                    wrong_answers = question_data['wrong_answers']
                    self.assertIsNotNone(question_text)
                    self.assertIsNotNone(question_answer)
                    self.assertIsNotNone(wrong_answers)
                    #make sure there is at least 4 wrong answers to have 4 multiple choice
                    self.assertGreaterEqual(len(wrong_answers), 4)

                    #get the lowercase of question answer and remove any "the" from the word
                    # to get a higher probability of matching
                    question_answer = question_answer.lower()
                    question_answer.replace('the','')

                    #get only the letters, remove spaces
                    answer_check = letters(question_answer)

                    for wrong_answer in wrong_answers:
                        #get the wrong answer to lowercase
                        wrong_answer = wrong_answer.lower()
                        wrong_answer.replace('the','')
                        wrong_answer_check = letters(wrong_answer)

                        #check the probability that the answer and wrong answer are similar
                        similarity = similar(answer_check, wrong_answer_check)
                        if similarity >= 0.8:
                            print(answer_check)
                            print(wrong_answer)
                        self.assertLessEqual(similarity,0.8)

    def test_has_atleast_10_category(self):
        #make sure database has at least 10 category
        category_count = 0
        for rounds in self.database.keys():
            category_count += len(self.database[rounds])

        self.assertGreaterEqual(category_count,10)


if __name__ == '__main__':
    unittest.main()