import os
import json

old_db_path = os.path.join('..','database.json')
new_db_path = os.path.join('..','new_database.json')

old_db = json.load(open(old_db_path))


new_db = {}

for round in old_db['Category'].keys():
    categoires = []

    for category_number in old_db['Category'][round].keys():
        #print(old_db['Category'][round][category_number])
        category_name = old_db['Category'][round][category_number].keys()[0]
        questions = []
        for question_number in old_db['Category'][round][category_number][category_name].keys():
            question_data = {}
            question_data['number'] = question_number
            question_data['question'] = old_db['Category'][round][category_number][category_name][question_number]['question']
            question_data['answer'] = old_db['Category'][round][category_number][category_name][question_number][
                'answer']
            question_data['wrong_answer'] = old_db['Category'][round][category_number][category_name][question_number][
                'wrong_answers']
            questions.append(question_data)

        category = {}
        category['category_name'] = category_name
        category['category_number'] = category_number
        category['questions'] = questions

        categoires.append(category)

    new_db[round]  = categoires

# for round in new_db.keys():
#     for category in new_db[round]:
#         for question in category['questions']:
#             print(question)

with open(new_db_path, 'w') as fp:
    fp.write(json.dumps(new_db, indent=4, sort_keys=True))
