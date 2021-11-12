import string


class VigenereCipher:
    # create  ASCII charset and Vigenere square

    def __init__(self):
        self.chars = ''.join(chr(i) for i in range(32, 127))
        self.manip = self.chars
        self.grid = [self.manip]
        for i in range(94):
            first = self.manip[0]
            self.manip = self.manip[1:] + first
            self.grid.append(self.manip)

    # sample A-Z charset and vigenere square for testing purposes
    # chars = string.ascii_uppercase
    # manip = chars
    # grid = []
    # grid.append(manip)
    # for i in range(25):
    #     first = manip[0]
    #     manip = manip[1:]+first
    #     grid.append(manip)

    # generate key of adequate length
    def genKey(self, key, ptext):
        for i in range(len(ptext) - len(key)):
            key = key + (key[i % len(key)])
        return key

    def encrypt(self, key, ptext):
        ciphertext = ""
        key = self.genKey(key, ptext)
        i = 0

        for letter in ptext:
            charLoc = self.chars.find(letter)
            keyLoc = self.chars.find(key[i])
            i = i + 1
            ciphertext = ciphertext + self.grid[keyLoc][charLoc]

        return ciphertext

    def decrypt(self, key, ctext):
        key = self.genKey(key, ctext)
        plaintext = ""
        i = 0

        for letter in ctext:
            keyLoc = self.chars.find(key[i])
            i = i + 1
            charLoc = self.getPChar(letter, keyLoc)
            plaintext = plaintext + self.chars[charLoc]

        return plaintext

    def getPChar(self, cchar, keyLoc):
        i = 0
        for letter in self.grid[keyLoc]:
            if letter == cchar:
                return i
            i = i + 1

    # old sample method to get raw inputs for testing.
    # def getAnswers():
    #     pt = raw_input("plaintext:")
    #     key = raw_input("key:")
    #     print(encrypt(key, pt))
    #     print(decrypt(key, "svs"))
    #     #print(decrypt('lpon' , r'nrq'))
