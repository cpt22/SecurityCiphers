import random
import math

class RSA_Cipher:
    def __init__(self):
        self.p, self.q, self.m, self.phi_m, self.encryption_val, self.decryption_val, self.private_key, self.public_key = self.generate_values()

    def generate_values(self):
        p = self.generate_primes_in_range(100, 200)  ## Idk how we want the user to generate random primes. Do they pick random primes?
        q = self.generate_primes_in_range(201, 300)
        m = p * q
        phi_m = (p - 1) * (q - 1)
        encryption_val = self.generate_encryption_val(m, phi_m)  # coprime with m and phi_m
        decryption_val = self.generate_decryption_val(encryption_val, phi_m)
        private_key = [encryption_val, m]
        public_key = [decryption_val, m]
        return p, q, m, phi_m, encryption_val, decryption_val, private_key, public_key

    def RSA_encryption(self, input_bytes_arr, public_key):
        output = []
        for byte in input_bytes_arr:
            # output.append(pow(byte, public_key[0]) % public_key[1]) <-- This is fine for small x^k (mod m)
            output.append(self.successive_square(byte, public_key[0], public_key[1]))
        return output

    def RSA_decryption(self, encrypted_string_byte, private_key):
        output = []
        for byte in encrypted_string_byte:
            # output.append(pow(byte, private_key[0]) % private_key[1])
            output.append(self.successive_square(byte, private_key[0], private_key[1]))
        output_as_string = "".join(map(chr, output))
        return output_as_string

    # returns x^k % m (where x^k >> Int.MAX)
    # Idea: Number Theory
    def successive_square(self, base, power, modulo):
        result = 1
        while power > 0:
            if power % 2 == 1:
                result = (result * base) % modulo

            power = power // 2
            base = (base * base) % modulo

        return result

    def generate_encryption_val(self, m, phi_m):
        for i in range(2, m):
            if math.gcd(i, m) == 1 and math.gcd(i, phi_m) == 1:
                return i

    def generate_decryption_val(self, encryption_val, phi_m):
        for i in range(2, 100000000):
            if i*encryption_val % phi_m == 1:
                return i

    def generate_primes_in_range(self, start, end):
        primes = [i for i in range(start, end) if self.isPrime(i)]
        return random.choice(primes)

    def isPrime(self, x):
            count = 0
            for i in range(int(x/2)):
                if x % (i+1) == 0:
                    count = count+1
            return count == 1
    

    def main(self):
        print("First randomly generated prime, p: " + str(self.p))
        print("Second randomly generated prime, q: " + str(self.q))
        print("Given the prime numbers, the private key: [" + str(self.private_key[0]) + "," + str(self.private_key[1]) + "]")
        print("Given the prime numbers, the public key: [" + str(self.public_key[0]) + "," + str(self.public_key[1]) + "]")
        print("Totient of m: " + str(self.phi_m))
        input_byte = [72,101,108,108,111,32,109,121,32,110,97,109,101,32,105,115,32,69,100,100,105,101]
        print("The input byte given by Christian (user's string converted to bytes): [" + ",".join([str(int) for int in input_byte]) + "]")
        test = self.RSA_encryption(input_byte, self.public_key)
        print("The encrypted output byte: [" + ",".join([str(int) for int in test]) + "]")
        # decrypted can also be done with separate encrypted string and key
        decrypted = self.RSA_decryption(test, self.private_key)
        print("The decryption of the encrypted input string: " + decrypted)


if __name__ == "__main__":
    RSA_Cipher().main()
