from io import TextIOWrapper
from json import JSONDecodeError, load, dump
from datetime import datetime
import argparse
import os

R_OK       : int = 0
E_ERROR    : int = 1
E_NOCONFIG : int = 2
E_INCONFIG : int = 3
E_NOTARGET : int = 10

def get_args() -> argparse.Namespace :
    parser = argparse.ArgumentParser(description = 'pass some flags')
    parser.add_argument('target', help ='the target to compile / add', type = str, default = '', nargs='?')
    parser.add_argument('-c', '--clean', help='remove object-files', type = bool, default=False, 
                        action=argparse.BooleanOptionalAction)
    return parser.parse_args()

def smkdir(name : str) -> bool :
    try:
        os.mkdir(name)
    except FileExistsError:
        return True
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
        print(f'missing file: {file}, creating')
        d = {}
        with open(file, 'w') as file:
            dump(d, file)
        
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
    
    smkdir(source)
    smkdir(build)
    
    about : dict = {'name': name}
    env : dict = {'root-dir': root, 'directories': {}, 'compiler': {}, 'libraries': {}, 
                  'compile-types': {}, 'executable': {}, 'compile-units': [],
                  'objects': []}
    
    env['directories'] = { 'source': source, 'build': build }
    env['compile-types'] = { 'object': { 'flags': ['c'] } }
    env['compiler'] = {'name': '', 'command': '', 'version': '', 'global-flags': []}
    env['executable'] = { 'name': name, 'file': 'main.cpp' }
    
    return { 'about': about, 'environment': env }
    
    
def compile(target : str):
    data : dict = sopen_read('data.json')
    
    is_target = False
    index = 0
    for i, t in enumerate(data['environment']['compile-units']):
        if t['name'] == target:
            is_target = True
            index = i
            break            
        
    if not is_target:
        print(f'{target} is not a target')
        exit(E_NOTARGET)
        
    unit = data['environment']['compile-units'][index]
    deps = unit['dependencies']
        
    # TODO: find iterative solution
    for d in deps:
        compile(d)
    
    gcc = data['environment']['compiler']['command']
    flags = ''
    gflags = ''
    for f in data['environment']['compiler']['global-flags']:
        gflags += f' -{f}'
    for f in data['environment']['compile-types'][unit['type']]['flags']:
        if f == 'o':
            if unit['type'] != 'exec':
                flags += f' -{f} {unit["name"]}'
        else:
            flags += f' -{f}'
    
    build = data['environment']['directories']['build']
    
    if target not in data['environment']['objects']:
        data['environment']['objects'].append(target)
    
    sopen_write('data.json', data)
    
    if 'c' not in data['environment']['compile-types'][unit['type']]:
        flags += ' -c'
    
    path = data['environment']['directories']['source'] + '/' + unit['file']
    print(f'{gcc}{gflags}{flags} {path}')
    os.system(f'{gcc} {gflags} {flags} {path}')
    os.rename(f'{target}.o', f'{build}/{target}.o')
    
    if unit['type'] == 'exec':
        obj = ''
        name = data['environment']['executable']['name']
        for o in data['environment']['objects']:
            obj += f' {build}/{o}.o'
        os.system(f'{gcc} {gflags} -o {name} {obj}')
    
    

def main() -> int :
    data : dict = sopen_read('data.json') or {}
            
    if data == {}:
        print('empty data.json, starting setup')
        data = setup()
        sopen_write('data.json', data)
        print('rerun to compile a target')
    else:
        args = get_args()
        if args.clean:
            build = data['environment']['directories']['build']
            for o in data['environment']['objects']:
                os.remove(f'{build}/{o}.o')
        else:
            compile(args.target)
    return R_OK
    
    
if __name__ == '__main__':
    rcode : int = main()
    exit(rcode)
