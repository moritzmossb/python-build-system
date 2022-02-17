#!/usr/bin/env python3
import constants
from json import load

class CompilationUnit:
    def __init__(self, name, file, extension, **kwargs):
        self.name = name 
        self.file = file
        self.ext  = extension
        libraries = kwargs.get('libraries', None)
        if libraries is not None:
            self.libraries = libraries
            self.use_libraries = True
        
    def object(self):
        src = ''
        with open(constants.config, 'r') as file:
            data = load(file)
            src = data['src_dir']
        return f'{constants.languages[self.ext].compiler} -{constants.object_flag} {src}/{self.file}.{self.ext}'