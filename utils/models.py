import json
import os

def load_categories():
    categories = {}
    category_path = 'categories'
    for filename in os.listdir(category_path):
        if filename.endswith('.json'):
            category_name = os.path.splitext(filename)[0]
            with open(os.path.join(category_path, filename), 'r') as f:
                questions = json.load(f)
                categories[category_name] = parse_questions(questions)
    return categories

def parse_questions(questions):
    parsed_questions = []
    for question_data in questions:
        question = question_data['question']
        answer_options = question_data['choices']
        correct_answer = question_data['answer']
        parsed_questions.append({
            'question': question,
            'answer_options': answer_options,
            'correct_answer': correct_answer
        })
    return parsed_questions
