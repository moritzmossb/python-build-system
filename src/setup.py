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
    use_cpp = False
    use_c   = False
    if 'C++' in langs:
        use_cpp = True
    if 'C' in langs:
        use_c = True
            
    data = {}
    data['compilation_units'] = []
    data['libraries'] = []
    data['compiled_objects'] = []
    data['languages'] = {}
    
    conditions = {'use_cpp': use_cpp, 'use_c': use_c}
    cond_answers = inquirer.prompt(generate_condition_questions(conditions))
    
    if use_cpp:
        cpp = {'name': 'C++', 
               'src_extension': 'cpp', 
               'hdr_extension': 'hpp',
               'standard': cond_answers['cpp_std']}
        
        data['languages']['cpp'] = cpp
    if use_c:
        c = {'name': 'C', 
               'src_extension': 'c', 
               'hdr_extension': 'h',
               'standard': cond_answers['c_std']}
        data['languages']['c'] = c
    
    data['root_dir'] = str(getcwd())
    data['build_dir'] = answers['build_dir']
    data['src_dir'] = answers['src_dir']
    data['log_dir'] = answers['log_dir']
    
    with open(constants.config, 'w', encoding=constants.encoding) as file:
        dump(data, file, indent=constants.dump_indent)
    
setup()