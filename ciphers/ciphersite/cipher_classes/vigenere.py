class VigenereCipher:
    @staticmethod
    def encrypt(key, decrypted_text):
        print("encrypting")
        return key + " " + decrypted_text

    @staticmethod
    def decrypt(key, encrypted_text):
        print("decrypting")
        return key + " " + encrypted_text

