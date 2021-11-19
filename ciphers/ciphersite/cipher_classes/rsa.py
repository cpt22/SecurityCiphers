import random
import math


class RSACipher:
    def generate_keys(self):
        ## Idk how we want the user to generate random primes. Do they pick random primes?
        p = self.generate_primes_in_range(100, 200)
        q = self.generate_primes_in_range(201, 300)
        m = p * q
        phi_m = (p - 1) * (q - 1)
        encryption_val = self.generate_encryption_val(m, phi_m)  # coprime with m and phi_m
        decryption_val = self.generate_decryption_val(encryption_val, phi_m)
        private_key = [encryption_val, m]
        public_key = [decryption_val, m]
        return private_key, public_key

    def encrypt(self, input_string, public_key):
        input_bytes_arr = input_string.encode()
        output = []
        for byte in input_bytes_arr:
            # output.append(pow(byte, public_key[0]) % public_key[1]) <-- This is fine for small x^k (mod m)
            output.append(self.successive_square(byte, public_key[0], public_key[1]))
        return ",".join([str(i) for i in output])

    def decrypt(self, encrypted_string, private_key):
        arr_input = [int(i) for i in encrypted_string.split(',')]
        output = []
        for elem in arr_input:
            # output.append(pow(byte, private_key[0]) % private_key[1])
            output.append(self.successive_square(elem, private_key[0], private_key[1]))
        output_as_string = "".join(map(chr, output))
        return output_as_string

    # returns x^k % m (where x^k >> Int.MAX)
    # Idea: Number Theory
    @staticmethod
    def successive_square(base, power, modulo):
        result = 1
        while power > 0:
            if power % 2 == 1:
                result = (result * base) % modulo

            power = power // 2
            base = (base * base) % modulo

        return result

    @staticmethod
    def generate_encryption_val(m, phi_m):
        for i in range(2, m):
            if math.gcd(i, m) == 1 and math.gcd(i, phi_m) == 1:
                return i

    @staticmethod
    def generate_decryption_val(encryption_val, phi_m):
        for i in range(2, 100000000):
            if i * encryption_val % phi_m == 1:
                return i

    @staticmethod
    def generate_primes_in_range(start, end):
        primes = [i for i in range(start, end) if RSACipher.is_prime(i)]
        return random.choice(primes)

    @staticmethod
    def is_prime(x):
        count = 0
        for i in range(int(x / 2)):
            if x % (i + 1) == 0:
                count = count + 1
        return count == 1
