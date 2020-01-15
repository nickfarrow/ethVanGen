# Usage
```
$ python ethVanGen.py -h

usage: Bruteforce Ethereum Vanity Addresses. [-h] [-f FILE] [-r] [-m MIN] [-n] [-e] [-o OUTPUT] [-v]

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

To search for words from a file, with some letter replacement (e.g. allow  e to be substituded with 3):
```
python ethVanGen.py -r -f FILE
```

To search for more than 6 consecutive numbers in an address
```
python ethVanGen.py -m 6 -n
```

To search for words longer than 8 characters from the default dictionary, with replacement, at the start or end of the address:
```
python ethVanGen.py -f dict.txt -m 8 -r -e
```
