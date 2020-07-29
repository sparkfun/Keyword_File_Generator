#!/usr/bin/env python

import argparse
import glob
import os
import CppHeaderParser
from braceexpand import braceexpand as expand

# ***********************************************************************************
#
# Example of CppHeader Usage (helps to understand what you can access and how)
#
# ***********************************************************************************
def cpp_header_example_usage(headerpath):

    # CppHeader reveals the structure (topology, geometry, however you want to call it) of the header file
    topology = CppHeaderParser.CppHeader(headerpath)

    print()
    print('--- defines ---')
    for x in topology.defines:
        print(x)

    print()
    print('--- enums ---')
    for x in topology.enums:
        print(x['name'])

    print() # note: classes include structures
    print('--- classes (dict) ---')
    for key, val in topology.classes.items():
        print('val equals dictionary accessed by key? ', end='')
        print(val == topology.classes[key])
        print('keys available within this struct/class: ')
        for k, v in val.items():
            print('\t', end='')
            print(k)
        print('value: ', end='')
        print(val)

    print() # note: classes include structures
    print('--- classes (list) ---')
    for x in topology.classes:
        print(x)

    print()
    print('--- functions ---')
    for x in topology.functions:
        print(x['name'])

    print()
    print('--- variables ---')
    for x in topology.variables:
        print(x['name'])





# ***********************************************************************************
#
# Main function
#
# ***********************************************************************************
def main():
    verboseprint("keywords_populator.py")

    symbols = {
        "KEYWORD1": [],
        "KEYWORD2": [],
        "KEYWORD3": [],
        "LITERAL1": [],
        "LITERAL2": [],
    }

    # use brace expansion to further extend the possibilities of pattern matching
    matches = []
    specs = list(expand(args.pathspec))
    for spec in specs:
        matches.extend(glob.glob(spec, recursive=args.recursive))

    # handle all matches from the expansion / glob pattern
    commonpath = None
    for match in matches:
        filepath = os.path.normpath(match)
        if commonpath == None:
            commonpath = filepath
        else:
            commonpath = os.path.commonpath([commonpath, filepath])
        abspath = os.path.abspath(filepath)
        _, ext = os.path.splitext(filepath)

        # do not process non-header files
        if ext != '.h' and ext != '.H':
            verboseprint("ignoring non-header file: '" + filepath + "'" )
            continue

        # extract header topology
        print("accumulating data from file: '" + filepath + "'")
        topology = CppHeaderParser.CppHeader(abspath)

        # accumulate defines
        verboseprint('\tdefines:')
        for constant in topology.defines:
            name = constant.split(' ')[0]
            symbols['LITERAL1'].append(name) # split on spaces and take the first portion // todo: optionally remove header guards from defines
            verboseprint('\t\t', name)

        # accumulate enums
        verboseprint('\tenums:')
        for enum in topology.enums:
            symbols['KEYWORD1'].append(enum['name'])
            verboseprint('\t\tname: ', enum['name'])
            verboseprint('\t\tvalues: ')
            for constant in enum['values']:
                symbols['LITERAL1'].append(constant['name'])
                verboseprint('\t\t\t', constant['name'])

        # accumulate classes + structures
        verboseprint('\tclasses + structs:')
        for name, type in topology.classes.items():
            verboseprint('\t\t', name)

            # accumulate public class / struct methods
            verboseprint('\t\t\tmethods:')
            for method in type['methods']['public']: # 'protected' and 'private' also valid
                symbols['KEYWORD2'].append(method['name'])
                verboseprint('\t\t\t\t', method['name'])
    
            # accumulate class / struct properties
            verboseprint('\t\t\tproperties:')
            for property in type['properties']['public']: # 'protected' and 'private' also valid
                symbols['LITERAL2'].append(property['name'])
                verboseprint('\t\t\t\t', property['name'])

            # send class names to KEYWORD1
            if(type['declaration_method'] == 'class'):
                symbols['KEYWORD1'].append(name)
                # todo: handle things that are specific to classes?
                # todo: handle nested classes? (type['nested_classes']) (probably recursive...)
                # todo: handle parents? (type['inherits']) (not recursive)
                continue
            
            # send struct names to KEYWORD3
            if(type['declaration_method'] == 'struct'):
                symbols['KEYWORD3'].append(name)
                continue
            
            # warn if we can't distinguish between class and struct
            raise(Exception("unknown declration method in type: '" + name + "'"))
        
        # accumulate functions
        verboseprint('\tfunctions:')
        for function in topology.functions:
            symbols['KEYWORD2'].append(function['name'])
            verboseprint('\t\t', function['name'])

        # accumulate variables
        verboseprint('\tvariables:')
        for variable in topology.variables:
            symbols['LITERAL2'].append(variable['name'])
            verboseprint('\t\t', variable['name'])

    # deduplicate symbols (https://www.w3schools.com/python/python_howto_remove_duplicates.asp)
    for label, entries in symbols.items():
        symbols[label] = list(dict.fromkeys(entries))

    # check if there is any content to actually write
    content = False
    try:
        for label, entries in symbols.items():
            if len(symbols[label]):
                content = True
                break
        if not content:
            raise(Warning('No content exists - keywords file will not be generated'))
    except Warning as w:
        print('warning! ' + str(w))
        print('exiting')
        exit()

    # determine the output filepath
    outpath = args.dest
    if args.dest == None:
        outpath = os.path.dirname(commonpath)
        print("no destination specified, falling back to common path from glob pattern: '" + commonpath + "'")
        if commonpath == None or commonpath == '':
            outpath = '.'
            print('no common path found, falling back to current directory')

    outfile = os.path.normpath(outpath + '/keywords.txt')
    print(outfile)

    # use accumulated symbols to build keywords file
    with open(outfile, 'w') as fout:
        fout.write("# Syntax Coloring Map For '" + outpath + "'\n")
        
        fout.write('\n# Datatypes (KEYWORD1)\n')
        for name in symbols['KEYWORD1']:
            fout.write(name + '\tKEYWORD1\n')
        
        fout.write('\n# Functions (KEYWORD2)\n')
        for name in symbols['KEYWORD2']:
            fout.write(name + '\tKEYWORD2\n')

        fout.write('\n# Structures (KEYWORD3)\n')
        for name in symbols['KEYWORD3']:
            fout.write(name + '\tKEYWORD3\n')

        fout.write('\n# Constants (LITERAL1)\n')
        for name in symbols['LITERAL1']:
            fout.write(name + '\tLITERAL1\n')

        fout.write('\n# Properties (LITERAL2)\n')
        for name in symbols['LITERAL2']:
            fout.write(name + '\tLITERAL2\n')

    exit()


# ******************************************************************************
#
# Main program flow
#
# ******************************************************************************
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Utility to update keyword files for the Apollo3 Arduino core')

    parser.add_argument('-p', '--pathspec', dest='pathspec', default='./*/*', required=False, help='glob pathspec to the file or directory from which to generate keywords (see python glob module)')
    parser.add_argument('-d', '--dest', dest='dest', required=False, help='an optional path to the output location - uses path dirname if not specified')
    parser.add_argument('-r', '--recursive', default=0, help='handle path recursively', action='store_true')
    parser.add_argument('-v', '--verbose', default=0, help='enable verbose output', action='store_true')

    args = parser.parse_args()

    # Create print function for verbose output if caller deems it: https://stackoverflow.com/questions/5980042/how-to-implement-the-verbose-or-v-option-into-a-script
    if args.verbose:
        def verboseprint(*args):
            # Print each argument separately so caller doesn't need to
            # stuff everything to be printed into a single string
            for arg in args:
                print(arg, end='', flush=True)
            print()
    else:
        verboseprint = lambda *a: None      # do-nothing function

    def twopartprint(verbosestr, printstr):
        if args.verbose:
            print(verbosestr, end = '')

        print(printstr)

    main()