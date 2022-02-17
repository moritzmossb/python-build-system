#!/usr/bin/env python3

from json import load, dump
import logging
from datetime import datetime
import constants
import inquirer

from util import generate_questions_list

def setup():
    # log_file = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    # logging.basicConfig(filename=f'{constants.default_log_dir}/{log_file}.{constants.log_ext}', 
    #                     format='%(asctime)s %(message)s', 
    #                     filemode='w')

    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    # logger.info('setting up new project')
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
        
    
setup()