import threading
import sys
import argparse
import hashlib
import time

print('''
\033[0;34m
████████╗███████╗██╗   ██╗███╗   ██╗ █████╗ ███╗   ███╗██╗
╚══██╔══╝██╔════╝██║   ██║████╗  ██║██╔══██╗████╗ ████║██║
   ██║   ███████╗██║   ██║██╔██╗ ██║███████║██╔████╔██║██║
   ██║   ╚════██║██║   ██║██║╚██╗██║██╔══██║██║╚██╔╝██║██║
   ██║   ███████║╚██████╔╝██║ ╚████║██║  ██║██║ ╚═╝ ██║██║
   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
''')

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--wordlist', type=str, help='The wordlist to bruteforce with.')
parser.add_argument('-t', '--thread', default=1, type=int, help='The number of threads to use. Default 1.')
parser.add_argument('-f', '--format', type=str, help='The hash format.')
parser.add_argument('hash', type=str, help='The hash itself.')

args = parser.parse_args(sys.argv[1:])

if not args.wordlist:
    print('\033[0;31mError: a wordlist is required\033[0;0m')
    sys.exit(1)

wordlist = open(args.wordlist).read().split('\n')
found = False

formats = {}
for item in dir(hashlib):
    if item in hashlib.algorithms_available: # Detect all available hashing algorithms
        formats[item] = lambda s: getattr(hashlib, item)(bytes(s, 'utf-8')).hexdigest()
if not args.format or args.format not in formats:
    print(f'\033[0;31mError: invalid format {args.format}. Expected one of: {", ".join(formats.keys())}\033[0;0m')
    sys.exit(1)
f = formats[args.format]

def brute():
    global found
    if not wordlist: # Because threads are weird about sys.exit
        return
    word = wordlist.pop(0)
    if f(word) == args.hash:
        found = word

threads = []
old = len(wordlist)
print(f'\033[0;34mTrying {old} words...')
start = time.time() # Get the start time
while True:
    if not wordlist:
        brute = lambda: 0
        sys.exit(1)
    threads = []
    for i in range(args.thread): # Since we cannot stop a thread, we just create new ones each time
        threads.append(threading.Thread(target=brute))
    for thread in threads:
        thread.start()
    print(f'\033[10D{str(100 * (old - len(wordlist)) / old).split(".")[0]}%', end='') # Percent
    if found:
        print(f'\n\033[0;32mMatch: {found}\033[0;0m')
        print(f'Cracked in {time.time() - start} seconds')
        sys.exit(0)
