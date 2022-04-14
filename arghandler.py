import argparse

def get_args() -> argparse.Namespace :
    parser = argparse.ArgumentParser(description = 'pass some flags')
    parser.add_argument('target', help ='the target to compile / add', type = str, default = '', nargs='?')
    parser.add_argument('-c', '--clean', help='remove object-files', type = bool, default=False, 
                        action=argparse.BooleanOptionalAction)
    return parser.parse_args()