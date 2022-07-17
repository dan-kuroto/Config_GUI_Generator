import argparse
import os
import sys
from typing import Dict, Type

from generator import BaseGenerator, PyQt5Generator


support: Dict[str, Dict[str, Type[BaseGenerator]]] = { 'PYTHON3': { 'PYQT5': PyQt5Generator } }

if __name__ == '__main__':
    # avoid relative path errors due to starting programs from other paths
    os.chdir(os.path.split(os.path.realpath(__file__))[0])

    # parse args
    parser = argparse.ArgumentParser('code generator for ConfigData and ConfigWindow in GUI softwares')
    parser.add_argument('-i', '--input', type=str, help='input file path (*.html)')
    parser.add_argument('-o', '--output', type=str, help='output file path (*.py)')
    parser.add_argument('-dn', '--data-name', type=str, help='class name of ConfigData', default='ConfigData')
    parser.add_argument('-wn', '--window-name', type=str, help='class name of ConfigWindow', default='ConfigWindow')
    parser.add_argument('-l', '--language', type=str, help='language of code', default='Python3')
    parser.add_argument('-m', '--module', type=str, help='module name of GUI software', default='PyQt5')
    parser.add_argument('-v', '--version', action='version', version='ConfigGUIGenerator 0.1')
    parser.add_argument('-s', '--support', action='store_true', help='show support list')
    args = parser.parse_args()

    # check args
    if args.support:
        print('Supported languages and modules:')
        for language in support:
            print('  ' + language)
            for module in support[language]:
                print('    ' + module)
        sys.exit(0)
    if not args.input:
        print('input file path is required')
        sys.exit(1)
    if not args.output:
        print('output file path is required')
        sys.exit(1)
    args.input = os.path.abspath(args.input)
    args.output = os.path.abspath(args.output)
    args.language = args.language.upper()
    args.module = args.module.upper()
    print('test', args.input)
    print('test', args.output)
    if not os.path.exists(args.input):
        print(f'input file "{args.input}" not found')
        sys.exit(1)
    if not os.path.exists(os.path.dirname(args.output)):
        print(f'output file directory "{os.path.dirname(args.output)}" not found')
        sys.exit(1)
    if os.path.exists(args.output):
        print(f'output file "{args.output}" already exists')
        sys.exit(1)
    if args.language not in support:
        print(f'language "{args.language}" not supported')
        sys.exit(1)
    if args.module not in support[args.language]:
        print(f'language "{args.language}" not supported by module "{args.module}"')
        sys.exit(1)

    # solve
    generator = support[args.language][args.module](args.input, args.output, args.data_name, args.window_name)
    generator.generate()
