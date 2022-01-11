import argparse, sys

from .superblock import Superblock

parser = argparse.ArgumentParser(description='put tool description here')
#parser.add_argument('-d', '--dump', help='write superblocks to local files')
parser.add_argument('-v', '--verbose', action='store_true', help='list all superblock properties')
parser.add_argument('paths', nargs='+', help='help for paths argument')
args = parser.parse_args()

for path in args.paths:
    with open(path, 'rb') as devfile:
        try:
            block = Superblock(devfile)
        except Exception as e:
            print(path, e)
            continue
        if args.verbose:
            print(path)
            for name, value in block.values.items():
                if name == 'dev_roles':
                    while value[-1] == 65535:
                        value = value[:-1]
                print(f' {name}: {value}')
        else:
            print(path, block.dev_number, block.events)
