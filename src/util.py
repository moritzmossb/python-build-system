#!/usr/bin/env python3
from constants import question_dict, data, encoding
from json import load

def option_print(options: list, default : str = None):
    default_text = '[default]'
    default_index = -1
    if default is not None:
        default_index = extract_default(options, default)
    for index, option in enumerate(options):
        print(f'[{index}] {option} {default_text if default_index == index else ""}')

def extract_default(options: list, default: str):
    for index, option in enumerate(options):
        if str(option) == default:
            return index
        
def generate_questions_list():
    qdata = None
    with open(data, 'r', encoding=encoding) as file:
        qdata = load(file)['setup_questions']
    if qdata is None:
        return False
    
    questions = []
    for question in qdata:
        name = question['name']
        t = question['type']
        default = question.get('default', None)
        message = question['description']
        choices = question.get('options', None)
        questions.append(question_dict[t](name, message=message, choices=choices, default=default, ignore=False, 
                                          validate=True, show_default=True))
        
    return questions