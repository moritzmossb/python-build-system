import os
from util import smkdir

def setup() -> dict :
    source : str = input('enter the source-dir name: ')
    build : str = input('enter the build-dir name: ')
    name : str = input('enter the project name: ')
    root : str = os.getcwd()
    
    
    if source == '':
        source = '.'
    else:
        smkdir(source)
        
    if build == '':
        build = '.'
    else:  
        smkdir(build)
    
    about : dict = {'name': name}
    env : dict = {'root-dir': root, 'directories': {}, 'compiler': {}, 'libraries': {}, 
                  'compile-types': {}, 'executable': {}, 'compile-units': [],
                  'objects': []}
    
    env['directories'] = { 'source': source, 'build': build }
    env['compile-types'] = { 'object': { 'flags': ['c'] }, 'exec': { 'flags': [] } }
    env['compiler'] = {'name': '', 'command': '', 'version': '', 'global-flags': []}
    env['executable'] = { 'name': name, 'target': 'main' }
    env['compile-units'] = [{
        'name': 'main',
        'file': 'main.cpp',
        'type': 'exec',
        'dependencies': []
    }]
    
    return { 'about': about, 'environment': env }