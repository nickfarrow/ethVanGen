# Nicholas Farrow 2020
import argparse
from ethereum import utils
import os
import time
import itertools

# Argument parser
parser = argparse.ArgumentParser("Bruteforce Ethereum Vanity Addresses.")
parser.add_argument("-f", "--file", 
        help="Search for words from a file.")
parser.add_argument("-r", "--replace", action='store_true', default=False, 
        help="Allow for swapping letters with hex characters, e.g. o -> 0.")
parser.add_argument("-m", "--min", default='5', 
        help="Minimum word length")
parser.add_argument("-n", "--numbers", action='store_true', default=False, 
        help="Search for 444444, 99999999 etc.")
parser.add_argument("-e", "--ends", action='store_true', default=False, 
        help="Check only start and ends of address for match.")
parser.add_argument("-o", "--output", default='found.txt', 
        help="File to write found addresses to.") 
parser.add_argument("-v", "--verbose", action='store_true', default=False, 
        help="Print out addresses as they are being checked")
args = parser.parse_args()

if args.replace:
    replaceOptions = {
            'a': ['a' ,'4'],
            'b': ['b','8'],
            'e': ['e', '3'],
            'g': ['6'],
            'i': ['1'],
            'l': ['1'],
            'o': ['0'],
            's': ['5'],
            't': ['7'],
            'z': ['2']
            }
else:
    replaceOptions = {}


def combinations(word, replaceOptions):
    '''Return all possible combinations of a word with letter replacements'''
    combos = [(c,) if c not in replaceOptions else replaceOptions[c] for c in word]
    return list((''.join(o) for o in itertools.product(*combos)))


def loadDictionary(file):
    with open(file, 'r') as f:
        wordList = f.read().splitlines()
    return wordList

def numberCombos(minLength):
    wordList = []
    for i in range(10):
        for j in range(int(minLength), 40):
            wordList.append(str(i) * j)

    return wordList


def generateWordSearch(wordList, replaceOptions, minLength):
    '''Find all possible variations of the word, \
            and add them to the searchWords if they can be created in hex'''
    availableLetters = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7',  '8', '9', '0']
    
    # Include replacable letters
    for key, letters in replaceOptions.items(): # key in replaceOptions.keys():
        availableLetters += letters

    # Words to be searched for
    searchWords = []

    # Add word and any variations to searchWords
    for word in wordList:

        if len(word) < int(minLength):
            print("Skipping {}, too short.".format(word))
            continue

        # Find alternate words
        if replaceOptions is not None:    
            alternateWordForms = combinations(word, replaceOptions)
        
        for altWord in alternateWordForms:
            # Add word to searchWords if all letters are possible
            if all(letter in availableLetters for letter in altWord):
                searchWords += alternateWordForms

            # Skip if not possible
            else:
                print("Can not create word {}".format(altWord))
    
    return searchWords


def genAddressAndCheck(searchWords, endOnly=False, verbose=False):
    privKey = utils.sha3(os.urandom(4096))
    rawAddress = utils.privtoaddr(privKey)
    accAddress = utils.checksum_encode(rawAddress)
    accPrivateKey = utils.encode_hex(privKey)
    
    if verbose:
        print("Checking {}".format(accAddress))

    # We search a lowercase version of the address for matches
    lowerAddress = accAddress.lower()
    
    found = False
    for word in searchWords:
        if endOnly:
            if (word in lowerAddress[1:len(word) + 2]) or (word in lowerAddress[-len(word):]):
                found = True

        else:
            if word in lowerAddress:
                found = True

        if found:
            return word, accAddress, accPrivateKey
    
    # No matches found
    return False


dictWords = []

if args.file is not None:
    dictWords += generateWordSearch(loadDictionary('dict.txt'), replaceOptions, args.min)

if args.numbers:
    # Add the longer numbers to list first, so they are searched first.
    # So 3333 is found rather than just 33
    dictWords += numberCombos(args.min)[::-1]

print("Exerpt of search list:")
print(dictWords[:10])
print("\n...\n...\n")
print(dictWords[-10:])

print("{} words in search list.\n\n".format(len(dictWords)))
print("Searching...\n")

i = 0
foundCount = 0
startTime = time.time()
# Search Loop
while True:
    
    if i % 10000 == 0:
        if True: #args.verbose:
            elapsed = time.time() - startTime
            checkRate = i/elapsed
            
            if foundCount != 0:
                findRate = round(elapsed/foundCount, 2)
            else:
                findRate = "infinite"

            print(("{} addresses have been searched for {} words in {:.2f} seconds."
                   " Check Rate: {:.2f} addresses per second."
                   " Expected to find address in {} seconds."
                   ).format(i, len(dictWords), elapsed, checkRate, findRate))

    # Create address and check for matches
    searchResult = genAddressAndCheck(dictWords, args.ends, args.verbose)
    if searchResult is not False:
        print("Found! : {}".format(searchResult))
        foundCount += 1

        # Write to output file
        with open(args.output, 'a+') as f:
            f.write("{} \t\t {} \t\t {} \n".format(*searchResult))
    
    i += 1
