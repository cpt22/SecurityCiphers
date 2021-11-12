
import string

class VigenereCipher:

    #create  ASCII charset and Vigenere square
    chars = ''.join(chr(i) for i in range(32,127))
    manip = chars
    grid = []
    grid.append(manip)
    for i in range(94):
        first = manip[0]
        manip = manip[1:]+first
        grid.append(manip)

    # sample A-Z charset and vigenere square for testing purposes
    # chars = string.ascii_uppercase
    # manip = chars
    # grid = []
    # grid.append(manip)
    # for i in range(25):
    #     first = manip[0]
    #     manip = manip[1:]+first
    #     grid.append(manip)

    #generate key of adequate length
    def genKey(key , ptext):
        for i in range(len(ptext) - len(key)):
            key = key + (key[i % len(key)])
        return key

    @staticmethod
    def encrypt(key , ptext):
        ciphertext= ""
        key = genKey(key, ptext)
        i = 0

        for letter in ptext:
            charLoc = chars.find(letter)
            keyLoc = chars.find(key[i])
            i = i + 1
            ciphertext = ciphertext + grid[keyLoc][charLoc]

        return ciphertext

    @staticmethod
    def decrypt(key, ctext):
        key = genKey(key, ctext)
        plaintext = ""
        i = 0

        for letter in ctext:
            keyLoc = chars.find(key[i])
            i = i + 1
            charLoc = getPChar(letter, keyLoc)
            plaintext = plaintext + chars[charLoc]
        
        return plaintext

    def getPChar(cchar, keyLoc):
        i = 0
        for letter in grid[keyLoc]:
            if letter == cchar:
                return i
            i = i + 1

    #old sample method to get raw inputs for testing.
    # def getAnswers():
    #     pt = raw_input("plaintext:")
    #     key = raw_input("key:")
    #     print(encrypt(key, pt))
    #     print(decrypt(key, "svs"))
    #     #print(decrypt('lpon' , r'nrq'))





