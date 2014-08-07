#!/usr/bin/env python3
#----------------
#Name: wordgen
#Version: 0.0.1
#Date: 2014-03-30
#----------------
#About the reference file...
#The expected format of the file is as follows:
#CATEGORY(1)
#ITEM(1),ITEM(2),...,ITEM(N)
#CATEGORY(2)
#ITEM(1),ITEM(2),...,ITEM(N)
# .
# .
# .
#CATEGORY(N)
#ITEM(1),ITEM(2),...,ITEM(N)
#EOF

import os
import sys
import argparse
import random

#Setup all of the flags and options to be passed from the CLI
parser = argparse.ArgumentParser(add_help=False, description='Welcome to words version 0.0.1, a program which allows you to randomly generate words for imagined languages based on word components of your choosing.')
parser.add_argument("-h", action='store_true', help="Display the help page.")
parser.add_argument("-s", nargs='?', help="Use a custom seed for the random number generator.", metavar='seed')
parser.add_argument("-f", nargs='?', help="Use a custom reference file for code word generation.", metavar='filename')
group = parser.add_mutually_exclusive_group()
group.add_argument('-lc', action='store_true', help="List categories and indices from the reference file.")
group.add_argument('-lv', action='store_true', help="Verbosely list word categories from the reference file.")
parser.add_argument("-g", nargs='+', type=int, help="Generate a code word via a list of category index numbers.", metavar='#')
parser.add_argument("-n", nargs='?', type=int, default=1, help="Number of phrases to generate.", metavar='number')
args = parser.parse_args()

if args.h :
    print('Introduction to wordgen v0.0.1:')
    print('  The wordgen.py program is a word generator which allows you to randomly')
    print('  generate a sequence of words built with components from a reference file.  Feel free')
    print('  to customize your own word source files by creating your own reference file.')
    print('  The categories can be re-used as many times in the generation process, in any')
    print('  order, as you see fit.  The default reference file (spanish.txt) is used if the')
    print('  -f flag is omitted.')
    print('\nSYNTAX\n  python3 wordgen.py [-h] [-f [filename]] [-lc | -lv] [-g # [# ...]]')
    print('\nARGUMENTS')
    print('  -h Displays this help page.')
    print('  -s <seed string> Utilize a user-defined seed for the random number generator.')
    print('  -f <filename> References <filename> instead of spanish.txt for word lists.')
    print('  -lc List categories and indices from the reference file.')
    print('  -lv Verbosely list word categories from the reference file.')
    print('  -g {c1 c2 ... cN} Generates a code word via the listed category indices.')
    print('  -n {n} Specifies the number of words to create.')
    print('\nEXAMPLES\n  python3 wordgen.py -g 0 1 2 ... cN')
    print('    Outputs a single word built with the components \"w1 w2 w3 w4 ... wM\":')
    print('      Where w1 is chosen from category 0, w2 from category 7 ... to wM from')
    print('      category cN referenced from the default reference file (spanish.txt)')
    print('\n  python3 wordgen.py -f foo.txt -lc')
    print('    Lists the categories contained in foo.txt.')
    print('\n  python3 wordgen.py -f foo.txt -g 0 2 1')
    print('    Outputs a single word \"w1 w2 w3\":')
    print('      Where w1 is chosen from category 3, w2 from category 2 and w3 from')
    print('      category 5 referenced from the file foo.txt.')
    print('\n  python3 wordgen.py -f foo.txt -g 0 2 1 -n 30')
    print('    Outputs a sequence of 30 words \"w1 w2 w3\":')
    print('      Where w1 is chosen from category 3, w2 from category 2 and w3 from')
    print('      category 5 referenced from the file foo.txt')
    sys.exit()

code_list = []
file_name = 'spanish.txt' #Set the default reference file name.

if args.f :
    file_name = args.f

try :
    for raw in open(file_name, encoding = 'utf-8', mode = 'r'):
        line = raw[:-1] #Get rid of new line characters
        if ',' in line : #Split strings with CSV into a list
            code_list.append(line.split(','))
        else :
            code_list.append(line) #Set strings w/o a CSV to be a single string
    list_count = len(code_list) #Count the lines from codex.txt; it should be even

    if list_count % 2 != 0 :
        sys.exit(1) #The following except will catch this error
except :
    print('ERROR: Either can\'t find the file [',file_name,'] or incorrect reference file format.')
    sys.exit(1)

if args.lc :
    #Print the even lines of the codex.txt file, which should be the categories
    print('Listing category indices from reference file [', file_name,']\n')
    for x in range(list_count) :
        if x % 2 == 0 :
            print(int(x / 2), code_list[x])
    sys.exit()

if args.lv :
    print('Listing categories verbosely from reference file [', file_name,']')
    for x in range(list_count) :
        if x % 2 == 0 :
            print('\n', int(x / 2), end = ' ', sep = '')
        print(code_list[x])
    sys.exit()

if args.g :
    print('Word generation from reference file [',file_name,']\n')

    i = args.n

    while i > 0:
        for x in args.g : #Gen a random number and pick aa code word for each category index
            try :
                y = int(x) * 2
                if y < list_count and y >= 0 :
                    if args.s :
                        s = args.s
                    else :
                        s = os.urandom(16) #gen 16 bytes of crypto-sound sudo-random data
                    random.seed(s)  #Initialize the random number generator with of random data
                    l = len(code_list[y+1]) #Remember that lists count 0 -> x not 1 -> x hence the l-1 in r
                    r = random.randint(0,l-1)
                    print(code_list[y+1][r], end = '')
                else :
                    sys.exit(1) #the following except will catch this error
            except :
                print('\nERROR: Invalid category index [', x, '] used.') 
                print('Please check available category indices with the -lc flag.')
                sys.exit(2)
        print('\n', end = '')
        i = i - 1
    sys.exit()


parser.print_help()
