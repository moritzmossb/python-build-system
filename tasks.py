#!/usr/bin/env python3
from invoke import task
import json
import os
from datetime import datetime

config = 'config.json'
configures = ('invoking configure', f'editing {config} manually')

enc = 'utf-8'
skip_values    = ('skip', '', ' ') 
valid_input_separators = (' ', ',', '/')

src_languages  = ('C++', 'C')
src_extensions = ('.cpp', '.c')
hdr_extensions = ('.hpp', '.h')

c_standards   = (89, 90, 95, 99, 11, 17)
cpp_standards = (11, 14, 17, 20)
compilers = ('gcc', 'clang')
common_warning_flags = ('Wall', 'pedantic', 'Wextra')
common_libraries = ('lm', 'pthread')

default_build = 'build'
default_src   = 'src'
default_log   = 'logs'

object_flag = '-c'

compiler_error_kwd = 'error'

class CompilationUnit:
    def __init__(self, name, src_file, **kwargs):
        self.data = {'name': name, 'src': src_file}
        libraries = kwargs.get('libs', None)
        if libraries is None:
            self.data['libraries'] = []
            self.data['use_libs'] = False
        else:
            self.data['libraries'] = libraries
            self.data['use_libs'] = True
            
    def asdict(self):
        return {'name':self.name, 'src': self.src_file, 'libs': self.libraries}
        
    def __getattr__(self, __name: str):
        if __name in self.data:
            return self.data[__name]
        else:
            raise AttributeError
        
    def object(self, compiler, flags, **kwargs):
        less = kwargs.get('less', False)
        print(f'[CXX] {self.name}')
        output = os.popen(f'{compiler} {flags} -o {self.name} {self.src}').read()
        
        found_errors = check_for_errors(output)
        
        with open(config, 'r') as file:
            data = json.load(file)
            with open(f'{data["log_dir"]}{self.name}.txt') as logfile:
                logfile.write(output)
        
        if found_errors:
            print('[WRN] found errors')
            if less:
                os.system(f'less {data["log_dir"]}{self.name}.txt')
            else:
                print(output)


@task
def setup(c):
    print('entering build-system setup')
    
    if os.path.isfile(config):
        if not yn_prompt(f'{config} already exists, replace with new one?'):
            print('aborting')
            return
    
    print('any settings you initially set here can be changed later by:')
    option_print(configures)
    print('')
    cppstd = choose_option_default(cpp_standards, 'newest', cpp_standards[-1], 'enter your C++ standard', 'ignore')
    print('')
    cstd = choose_option_default(c_standards, 'newest', c_standards[-1], 'enter your C standard', 'ignore')

    data = {}
    if cppstd is not None:
        data['cppstd'] = cppstd
    if cstd is not None:
        data['cstd'] = cstd
        
    data['date'] = datetime.today().strftime('%d.%m,%Y, %H:%M:%S')
    data['rootdir'] = str(os.getcwd()) + '/'
    print('')
    author = usr_input_skip('enter the project author')
    if author:
        data['author'] = author
        print('')
        email = usr_input_skip('enter your email-address')
        if email:
            data['email'] = email
    
    data['compiler'] = {}
    print('')
    compiler = choose_option_default(compilers, '', compilers[0], 'choose your compiler')
    data['compiler']['which'] = compiler
    print('')
    warnings = multi_select(common_warning_flags, 'choose common warning flags')
    if warnings is not None:
        data['compiler']['warnings'] = warnings
    print('')
    libs = multi_select(common_libraries, 'choose common libraries')
    if libs is not None:
        data['compiler']['libraries'] = libs
        
    data['objects'] = []
    data['compilation_units'] = []
    data['libraries'] = []
    print('')
    builddir = usr_input_default('enter the build-dir', default_build)
    data['build_dir'] = f'{os.getcwd()}/{builddir}/'
    print('')
    srcdir = usr_input_default('enter the source-dir', default_src)
    data['src_dir'] = f'{os.getcwd()}/{srcdir}/'
    print('')
    logdir = usr_input_default('enter the log-dir', default_log)
    data['log_dir'] = f'{os.getcwd()}/{logdir}/'
    
    # TODO: outsource this to a function
    try:
        if not os.path.isdir(builddir):
            os.mkdir(builddir)
    except FileExistsError:
        print(f'{builddir} exists, skipping creation')
    
    try:
        if not os.path.isdir(srcdir):
            os.mkdir(srcdir)
    except FileExistsError:
        print(f'{srcdir} exists, skipping creation')
        
    try:
        if not os.path.isdir(logdir):
            os.mkdir(logdir)
    except FileExistsError:
        print(f'{logdir} exists, skipping creation')
    
    with open(config, 'w', encoding=enc) as file:
        json.dump(data, file, ensure_ascii=False)

@task
def add_library(c):
    print('creating new library')
    lib_name = usr_input_default('enter the library name', 'new_lib')
    print(lib_name)
    data = None
    with open(config, 'r', encoding=enc) as file:
        data = json.load(file)
    
    lang = get_target_lang(data, True)
    src_file = usr_input_default('enter the name of the source-file', f'{lib_name}')
    
    try:
        if not src_file in data['libraries']:
            f = open(f'{data["src_dir"]}{src_file}.{lang}', 'x')
            f.close()
        else:
            raise FileExistsError()
    except FileExistsError:
        print('src-file already exists, aborting')
        
    lib = {'name': lib_name, 'target_language': lang, 'src': src_file}
    data["libraries"].append(lib)
    
    with open(config, 'w', encoding=enc) as file:
        json.dump(data,file)
    print('done')
    

@task
def add_compilation_unit(c):
    print('creating new compilation unit')
    unit_name = usr_input_default('enter the unit-name', 'new_unit')
    data = None
    with open(config, encoding=enc) as file:
        data = json.load(file)
    data['compilation_units'][unit_name] = {}
    lang = usr_input_default('enter the target language', 'cpp')
    src_file = usr_input_default('enter the name of the source-file', f'{unit_name}.{lang}')

    

@task
def help(c):
    print('you can configure the project by:')
    option_print(configures)
                
def option_print(options, default = None):
    for index, option in enumerate(options):
        if default is not None:
            if option == default:
                print(f' {index}) {option} [default]')
            else:
                print(f' {index}) {option}')
        else:
            print(f' {index}) {option}')

def get_target_lang(data,header=False):
    lang = ''
    if data.get('cstd', None) is None:
        lang = 'hpp' if header else 'cpp'
    elif data.get('cppstd', None) is None:
        lang = 'h' if header else 'c'
    else:
        lang = usr_input_default('enter the target language', 'hpp' if header else 'cpp')
    return lang
        
def choose_option_single(options, text=''):
    if text != '':
        print(text)
        
    option_print(options)
    
    while True:
        print(f'[0, {len(options)-1}]:', end=' ')
        usr_input = input().lower()
        try:
            choice = int(usr_input)
        except ValueError:
            print(f'please enter a number between 0 and {len(options)-1}')
            continue
            
        if choice in range(len(options)):
            return choice
        else:
            print('invalid choice, please enter a valid option')
        

def choose_option_default(options, default_name, default_value, text=' ', ignore=None):
    if text != ' ':
        print(text)
    print('valid choices are:', end=' ')
    if default_name == '':
        default_name = '<enter>'
    print(f'{default_name}', end=', ')
    if ignore:
        print(ignore, end=', ')
    print(f'0-{len(options)-1}')
    option_print(options, default_value)
    while True:
        print('>', end=' ')
        usr_input = input().lower()
        if usr_input == '':
            return default_value
        elif usr_input in (default_name, ignore):
            if usr_input == default_name:
                return default_value
            if usr_input == ignore:
                return None
        else:
            try:
                choice = int(usr_input)
                if choice > len(options):
                    print('please enter a valid choice')
                    continue
                return options[choice]
            except ValueError:
                print('please enter a valid choice')

def multi_select(options, text=' '):
    if text != ' ':
        print(text)
    print('<enter> for no choice')
    print('separeate your choices with: ', end=' ')
    for index, sep in enumerate(valid_input_separators):
        if index < len(valid_input_separators)-1:
            if sep == ' ':
                print('<space>', end=' ')
            else:
                print(sep, end=' ')
        else:
            print(sep)
    option_print(options)
    while True:
        print('>', end=' ')
        usr_input = input().lower()
        if usr_input == '':
            return None
        delim = ''
        for sep in valid_input_separators:
            if usr_input.find(sep) != -1:
                delim = sep
                break
        if delim == '':
            try:
                choice = int(usr_input)
                return options[choice]
            except ValueError:
                print('please enter a valid option')
                continue
        else:
            try:
                choices = [int(s.strip()) for s in usr_input.split(delim)]
                data = [options[i] for i in choices]
                return data
            except ValueError:
                print('please enter valid options')
                continue
            
            

def yn_prompt(text):
    valid_choices = {'yes': True, 'y': True, 'no': False, 'n': False}
    print(f'{text} [y/n]', end=' ')
    while True:
        choice = input().lower()
        if choice in valid_choices:
            return valid_choices[choice]
        else:
            print(f'invalid choice: {choice}')
            print(f'{text} [y/n] ', end=' ')
            
def usr_input_skip(prompt):
    print(prompt)
    print('<enter> for no choice\n>', end=' ')
    usr_input = input()
    if usr_input in skip_values:
        return False
    else:
        return usr_input
    
def usr_input_default(prompt, default_value):
    print(f'{prompt} or <enter> to use "{default_value}"')
    print('> ', end=' ')
    usr_input = input()
    if usr_input == '':
        return default_value
    else:
        return usr_input
    
def check_for_errors(txt):
    if txt.find(compiler_error_kwd) != -1:
        return True
    else:
        return False
