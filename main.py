from util import compile_target, sopen_read, sopen_write, R_OK
from setup import setup
from arghandler import get_args
from os import remove

def main() -> int :
    data : dict = sopen_read('pybuild.json') or {}
    if data == {}:
        print('empty pybuild.json, starting setup')
        data = setup()
        sopen_write('pybuild.json', data)
        print('rerun to compile a target')
    else:
        args = get_args()
        if args.clean:
            build = data['environment']['directories']['build']
            for o in data['environment']['objects']:
                remove(f'{build}/{o}.o')
        else:
            compile_target(args.target)
    return R_OK

if __name__ == '__main__':
    rcode : int = main()
    exit(rcode)
