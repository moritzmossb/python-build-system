#!/usr/bin/env python3
import inquirer

config_file_name = 'config'
config_file_extension = 'json'
encoding = 'utf-8'
config = f'{config_file_name}.{config_file_extension}'
data_file_name = 'data'

data = f'{data_file_name}.{config_file_extension}'

logging_enabled = True
log_ext = 'log'

valid_skip_values      = ('skip', '', ' ')
valid_input_separators = (' ', ',', '/')

object_flag = 'c'
dump_indent = 4

question_dict = {'checkbox': inquirer.Checkbox, 'text': inquirer.Text, 'editor': inquirer.Editor,
                 'list': inquirer.List, 'password': inquirer.Password, 'confirm': inquirer.Confirm,}