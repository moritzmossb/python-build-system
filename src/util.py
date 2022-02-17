#!/usr/bin/env python3
from constants import question_dict, data, encoding
from json import load
        
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
        if t == 'list':
            questions[-1].carousel= True
        
    return questions

def generate_condition_questions(conditions):
    qdata = None
    with open(data, 'r', encoding=encoding) as file:
        qdata = load(file)['conditional_questions']
    if qdata is None:
        return False
    
    questions = []
    for q in qdata:
        cond  = q['condition']
        if not conditions[cond]['use']:
            continue
        name = q['name']
        t = q['type']
        default = q.get('default', None)
        message = q['description']
        choices = q.get('options', None)
        questions.append(question_dict[t](name, message=message, choices=choices, default=default, ignore=False,
                                          validate=True))
        if t == 'list':
            questions[-1].carousel= True
        else:
            questions[-1].show_default = True
            
    return questions