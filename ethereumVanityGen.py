import os
from ethereum import utils

def openDictionary():
    with open('dict.txt') as f:
        wordList = f.read().splitlines() 
    
    letterPairs = [['o', '0'], ['i', '1'], ['l', '1'], ['z', '2'], ['s', '5'], ['g', '6'], ['t', '7']]    

    wordDict = []   
    for word in wordList:
        if all(letter in word for letter in ['i', 'l']):
            print("Not including {}".format(word))
            continue

        for letterPair in letterPairs:
            #print(letterPair[0], letterPair[1])
            if letterPair[0] in word:
                word = word.replace(letterPair[0], letterPair[1])  
        wordDict.append(word)

    return wordDict

def writeFind(addressDetails, textFile):
    coolFile = open(textFile, 'a')
    coolFile.write("%s\n" % addressDetails)
    coolFile.close()
    return

addressList = []


def main(checkList, extraList=[], fullDict=True, endsOnly=True, startLen=3, textFile='found.txt'):
    searchLength = startLen
    repeatList = [value*searchLength for value in checkList]
    
    while True:
        if fullDict:
            wordSieve = wordDict + repeatList + extraList
        else:
            wordSieve = repeatList + extraList


        exit = False
        while True:
            privKey = utils.sha3(os.urandom(4096))
            rawAddress = utils.privtoaddr(privKey)
            accAddress = utils.checksum_encode(rawAddress)
            accPrivateKey = utils.encode_hex(privKey)

            lowerAddress = accAddress.lower()
            
            for checkStr in wordSieve:
                
                found = False
                if endsOnly:
                    if (checkStr in lowerAddress[1:len(checkStr) + 2]) or (checkStr in lowerAddress[-len(checkStr):]):
                            found = True
                else:
                    if checkStr in lowerAddress:
                            found = True

                if found:
                    addressList.append([checkStr, accAddress, accPrivateKey])
                    writeFind([checkStr, accAddress, accPrivateKey], textFile)
                    
                    if checkStr in extraList:
                        print("{} - SOUGHT WORD FOUND".format(checkStr))
                    
                    else:
                        print("{} - FOUND".format(checkStr))
                        searchLength += 1
                        repeatList = [value*searchLength for value in checkList]
                        
                        exit = True
                        
                        break
            if exit:
                break
                        
    return


print(addressList)
