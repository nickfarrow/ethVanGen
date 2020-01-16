Bruteforce Ethereum vanity addresses like `0xda66666666c3a809ADA79D93114a3662073cC0`, with ability to search for words from a dictionary and alphanumeric combinations.

# Dependencies
Requires `ethereum` library:
```
python -m pip install ethereum
```

# Usage
```
Bruteforce Ethereum Vanity Addresses. [-h] [-f FILE] [-r] [-m MIN] [-n] [-e] [-o OUTPUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Search for words from a file.
  -r, --replace         Allow for swapping letters with hex characters, e.g. o -> 0.
  -m MIN, --min MIN     Minimum word length
  -n, --numbers         Search for 444444, 99999999 etc.
  -e, --ends            Check only start and ends of address for match.
  -o OUTPUT, --output OUTPUT
                        File to write found addresses to.
  -v, --verbose         Print out addresses as they are being checked
```


# Examples
To search for words from a file, with some letter replacement (e.g. allow  `e` to be substituded with `3`):
```
python ethVanGen.py -r -f FILE
```


To search for more than 6 consecutive numbers in an address
```
python ethVanGen.py -m 6 -n
...
0xC103A3f79c7b1f12222221bD149653fc448dE7Bf
```


To search for words longer than 4 characters from the default dictionary, with replacement, at the start or end of the address:
```
python ethVanGen.py -r -f dict.txt -m 4 -e
0xc0de6c3fbB1966b5433026BB5219CF6a8C306A3f
```


# Editing Letter Replacements
To change what letters are replaced (`-r`), edit `ethVanGen.py` and edit the following:
```
replaceOptions = {
    #'a': ['a' ,'4'],
    #'b': ['b','8'],
    #'e': ['e', '3'],
    'g': ['6'],
    #'i': ['1'],
    #'l': ['1'],
    'o': ['0'],
    's': ['5'],
    #'t': ['7'],
    #'z': ['2']
}

```
