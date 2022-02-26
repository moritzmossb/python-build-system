from io import TextIOWrapper
from json import JSONDecodeError, load, dump
from datetime import datetime
import argparse
import os

E_ERROR    : int = 1
E_NOCONFIG : int = 2
E_INCONFIG : int = 3

def get_args() -> argparse.Namespace :
    parser = argparse.ArgumentParser(description = 'pass some flags')
    parser.add_argument('target', help ='the target to compile / add', type = str, default = '', nargs='?')
    parser.add_argument('-a', '--add', help ='add a target (compile-unit, library)', type = bool,
                        action = argparse.BooleanOptionalAction, default = False)
    return parser.parse_args()

def smkdir(name : str) -> bool :
    try:
        os.mkdir(name)
    except FileExistsError:
        print(f'{name} already exists, skipping')
    return True

def sopen_read(file : str) -> dict :
    try:
        with open(file, 'r', encoding='utf-8') as file:
            try:
                data = load(file)
                return data
            except JSONDecodeError as e:
                print(f'invalid json file: {file}')
                print(f'\t{e}')
                exit(E_INCONFIG)
    except FileNotFoundError:
        print(f'missing file: {file}')
        return exit(E_NOCONFIG)
        
def sopen_write(file : str, data : dict) -> bool :
    try:
        with open(file, 'w', encoding='utf-8') as file:
            dump(data, file, indent=4)
            return True
    except FileNotFoundError:
        print(f'missing file: {file}')
        return False

def setup() -> dict :
    source : str = input('enter the source-dir name: ')
    build : str = input('enter the build-dir name: ')
    name : str = input('enter the project name: ')
    root : str = os.getcwd()
    
    about : dict = {'name': name}
    env : dict = {'root-dir': root, 'directories': {}, 'compiler': {}, 'libraries': {}, 
                  'compile-types': {}, 'executable': {}, 'compile-units': [],
                  'objects': []}
    
    env['directories'] = { 'source': source, 'build': build }
    env['compile-types'] = { 'object': { 'flags': ['c'] } }
    env['executable'] = { 'name': name, 'file': 'main.cpp' }
    
    return { 'about': about, 'environment': env }
    

def main() -> int :
    data : dict = sopen_read('data.json') or {}
            
    if data == {}:
        print('empty data.json, starting setup')
        data = setup()
        sopen_write('data.json', data)
    else:
        args = get_args()
    
    
if __name__ == '__main__':
    rcode : int = main()
    exit(rcode)
