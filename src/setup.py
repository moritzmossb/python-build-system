#!/usr/bin/env python3

from json import load, dump
import logging
from datetime import datetime
import constants
import inquirer
from os import getcwd

from util import generate_questions_list

def setup():
    answers = inquirer.prompt(generate_questions_list())
    langs = answers['target_languages']
    use_cpp = False
    use_c   = False
    if 'C++' in langs:
        use_cpp = True
    if 'C' in langs:
        use_c = True
    
    cpp_stds = None
    c_stds   = None
    with open(constants.data, 'r') as file:
        data = load(file)
        if use_cpp:
            cpp_stds = data['languages']['cpp']['standards']
            cpp_def_std = data['languages']['cpp']['default_std']
        if use_c:
            c_stds = data['languages']['c']['standards']
            c_def_std = data['languages']['c']['default_std']
    
    if use_cpp:
        cpp_std = inquirer.prompt([inquirer.List("cpp_std", 
                                                     message="Choose your C++ standard",
                                                     choices=cpp_stds,
                                                     default=cpp_def_std,
                                                     ignore=False,
                                                     validate=True)])
    if use_c:
        c_std = inquirer.prompt([inquirer.List("c_std", 
                                                    message="Choose your C standard",
                                                    choices=c_stds,
                                                    default=c_def_std,
                                                    ignore=False,
                                                    validate=True)])
    data = {}
    data['compilation_units'] = []
    data['libraries'] = []
    data['compiled_objects'] = []
    data['languages'] = []
    if use_cpp:
        cpp = {'name': 'C++', 
               'src_extension': 'cpp', 
               'hdr_extension': 'hpp',
               'standard': cpp_std['cpp_std']}
        
        data['languages'].append(cpp)
    if use_c:
        c = {'name': 'C', 
               'src_extension': 'c', 
               'hdr_extension': 'h',
               'standard': c_std['c_std']}
        data['languages'].append(c)
    
    data['root_dir'] = str(getcwd())
    data['build_dir'] = answers['build_dir']
    data['src_dir'] = answers['src_dir']
    data['log_dir'] = answers['log_dir']
    
    with open(constants.config, 'w', encoding=constants.encoding) as file:
        dump(data, file)
    
setup()