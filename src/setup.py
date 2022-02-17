#!/usr/bin/env python3

from ctypes import util
from json import load, dump
import logging
from datetime import datetime
import constants
import inquirer
from os import getcwd

from util import generate_questions_list, generate_condition_questions

def setup():
    answers = inquirer.prompt(generate_questions_list())
    langs = answers['target_languages']
    languages = {'C++': {'use': False, 'name': 'cpp', 'src_ext': 'cpp', 'hdr_ext': 'hpp', 'ans_var': 'cpp_std'},
                 'C': {'use': False, 'name': 'c', 'src_ext': 'c', 'hdr_ext': 'h', 'ans_var': 'c_std'} }
    
    for lang in constants.languages:
        if lang in langs:
            languages[lang]['use'] = True
        
    data = {}
    data['compilation_units'] = []
    data['libraries'] = []
    data['compiled_objects'] = []
    data['languages'] = {}
    
    cond_answers = inquirer.prompt(generate_condition_questions(languages))
    
    for cond in languages:
        if not languages[cond]['use']:
            continue
        l = languages[cond]
        lang = {'name': l['name'], 'src_extension': l['src_ext'], 'hdr_extension': l['hdr_ext'], 
                'standard': cond_answers[l['ans_var']]}
        data['languages'][l['name']] = lang
    
    data['root_dir'] = str(getcwd())
    data['build_dir'] = answers['build_dir']
    data['src_dir'] = answers['src_dir']
    data['log_dir'] = answers['log_dir']
    
    with open(constants.config, 'w', encoding=constants.encoding) as file:
        dump(data, file, indent=constants.dump_indent)

setup()