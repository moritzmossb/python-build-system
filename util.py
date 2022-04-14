#!/usr/bin/env python3
"""utility-functions and constants used for pybuild"""

from fnmatch import fnmatch
from os import mkdir, system
from json import JSONDecodeError, dump, load

R_OK       : int = 0
E_ERROR    : int = 1
E_NOCONFIG : int = 2
E_INCONFIG : int = 3
E_NOTARGET : int = 10

DEFAULT_FILE_ENCODING = 'utf-8'
DEFAULT_JSON_INDENT = 4
INVALID_DIRNAMES = ('', '.', '..', '/')
CONFIG_FILE = 'pybuild.json'

# not great, not too bad
objects = []


def smkdir(name : str, overwrite : bool = False) -> bool :
    if name in INVALID_DIRNAMES:
        return False
    try:
        mkdir(name)
    except FileExistsError:
        return overwrite
    return True

def sopen_read(file : str, enc : str = DEFAULT_FILE_ENCODING) -> dict :
    data = {}
    valid_json = False
    try:
        with open(file, 'r', encoding=enc) as f:
            try:
                data = load(f)
                valid_json = True
            except JSONDecodeError as e:
                print(f'invalid json file: {file}')
                print(f'\t{e}')
    except FileNotFoundError:
        return {}
        
    if valid_json:
        return data
    else:
        exit(E_INCONFIG)
        
def sopen_write(file : str, data : dict, enc : str = DEFAULT_FILE_ENCODING) -> bool :
    with open(file, 'w', encoding=enc) as f:
        dump(data, f, indent = DEFAULT_JSON_INDENT)
        
    return True

def generate_flag_string(flags: list, exclude : list = []):
    flag_str = ''
    for f in flags:
        if f not in exclude:
            flag_str += f' -{f}'
    return flag_str

def compile_unit(fname : str, flags : list, compiler : str, src_dir : str,
                 name : str = '', is_object : bool = False):
    exclude = ['c']
    if name != '':
        exclude = ['c', 'o']
    flag_str = generate_flag_string(flags, exclude)
    
    if name != '':
        flag_str += f' -o {name}'
    
    if is_object:
        flag_str += ' -c'
        
    path = src_dir + '/' + fname
    print(f'[CXX] {fname}')
    system(f'{compiler}{flag_str} {path}')
    
def generate_objstring() -> str:
    ostr = ''
    for o in objects:
        ostr += ' ' + o
    return ostr

def compile_target(target : str) -> bool:
    data = sopen_read(CONFIG_FILE)
    is_target = False
    index = 0
    
    # check if supplied target exists
    c_units = data['environment']['compile-units']
    for i, u in enumerate(c_units):
        if u['name'] == target:
            is_target = True
            index = i
            break
        
    if not is_target:
        print(f'{target} is not a target')
        exit(E_NOTARGET)
        
    unit = c_units[index]
    deps = unit['dependencies']
    cxx = data['environment']['compiler']['command']
    flags = data['environment']['compile-types'][unit['type']]['flags']
    global_flags = data['environment']['compiler']['global-flags']
    flags += global_flags
    build_dir = data['environment']['directories']['build']
    src_dir = data['environment']['directories']['source']
    
    
    if unit['type'] == 'single':
        compile_unit(unit['file'], flags, cxx, src_dir, unit['name'])
        return True
    
    
    
    if unit['type'] == 'object':
        compile_unit(unit['file'], flags, cxx, src_dir, '', True)
        return True
        
    for d in deps:
        compile_target(d)
        if f'{d}.o' not in objects:
            objects.append(f'{d}.o')
            
    if unit['type'] == 'exec':
        compile_unit(unit['file'], flags, cxx, src_dir, '', True)
        print(f'[CXX]{generate_objstring()} {unit["name"]}.o -> {unit["name"]}')
        system(f'{cxx}{generate_flag_string(flags, ["o", "c"])} -o {unit["name"]}{generate_objstring()} {unit["name"]}.o')
        
    
    if build_dir not in INVALID_DIRNAMES:
        for o in objects:
            print(f'[MV ] {o} {build_dir}/{o}')
            system(f'mv {o} {build_dir}/{o}')
        if unit['type'] == 'exec':
            print(f'[MV ] {unit["name"]}.o {build_dir}/{unit["name"]}.o')
            system(f'mv {unit["name"]}.o {build_dir}/{unit["name"]}.o')
    
        
    return True