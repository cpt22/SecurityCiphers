import math


# Sources:
# https://www.educba.com/md5-alogrithm/
# https://en.wikipedia.org/wiki/MD5#Algorithm
class MD5:
    rotation_arr = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                    5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    constants = [int(abs(math.sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(len(rotation_arr))]

    @staticmethod
    def E(x, y, z):
        return (x & y) | (~x & z)

    @staticmethod
    def F(x, y, z):
        return (x & z) | (y & ~z)

    @staticmethod
    def G(x, y, z):
        return x ^ y ^ z

    @staticmethod
    def H(x, y, z):
        return y ^ (x | ~z)

    initial_counter_values = [
        0x67452301,
        0xefcdab89,
        0x98badcfe,
        0x10325476,
    ]

    shuffle_index_functions = [
        lambda ind: ind,
        lambda ind: (5 * ind + 1) % 16,
        lambda ind: (3 * ind + 5) % 16,
        lambda ind: (7 * ind) % 16,
    ]

    @staticmethod
    def hash(self, data):
        data = bytearray(data)
        # calculate the length of data in bits and L_AND that with 0xFFFFFFFFFFFFFFFF to restrict the size to 64 bits
        data_length = (8 * len(data)) & 0xFFFFFFFFFFFFFFFF
        # Append the first padding bit
        data.append(0x80)
        # Pad data with zeroes until it is correctly size aligned
        while len(data) % 64 != 56:
            data.append(0x00)
        # Append the data length to the data byte array in little endian order
        data += data_length.to_bytes(8, byteorder="little")

        # duplicate the initial values into a new arr
        segments = self.initial_counter_values[:]

        # Loop through all of the data in 512 bit (64 byte, hence the 64 step) chunks
        for chunk_512 in range(0, len(data), 64):
            a, b, c, d = segments
            print(segments)
            # Obtain 512 bits (64 bytes) of data (the current chunk)
            current_chunk = data[chunk_512:chunk_512+64]
            for i in range(64):
                if i in range(16):
                    f = MD5.E(b, c, d)
                    g = i
                elif i in range(16, 32):
                    f = MD5.F(b, c, d)
                    g = (5 * i + 1) % 16
                elif i in range(32, 48):
                    f = MD5.G(b, c, d)
                    g = (3 * i + 5) % 16
                elif i in range(48, 64):
                    f = MD5.H(b, c, d)
                    g = (7 * i) % 16

                # calculates the index to get the correct function from the arrays
                ind = math.floor(i / 16)
                # Calls the correct lambda to process the values
                f = self.bitwise_functions[ind](b, c, d)
                g = self.shuffle_index_functions[ind](i)
                # Calculates the value to be rotated
                pre_rotation_value = a + f + self.constants[i] + int.from_bytes(current_chunk[4*g:4*g+4], byteorder="little")
                # Gets the correct new b value after rotation, the 0xFFFFFFFF is used to ensure that the ouput is limited to 8 bytes
                post_rotation_value = (b + self.left_rotate(pre_rotation_value, self.rotation_arr[i])) & 0xFFFFFFFF
                a, b, c, d = d, post_rotation_value, b, c

                for ind, val in enumerate([a, b, c, d]):
                    segments[i] += val
                    segments[i] &= 0xFFFFFFFF

            return sum(x << (32 * i) for i, x in enumerate(segments))

    def left_rotate(self, x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

# rotation_arr = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
#                 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
#                 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
#                 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
#
# constants = [int(abs(math.sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(len(rotation_arr))]
#
# bitwise_functions = [
#     lambda x, y, z: (x & y) | (~x & z),
#     lambda x, y, z: (x & z) | (y & ~z),
#     lambda x, y, z: x ^ y ^ z,
#     lambda x, y, z: y ^ (x | ~z),
# ]
#
# initial_counter_values = [
#             0x67452301,
#             0xefcdab89,
#             0x98badcfe,
#             0x10325476,
#         ]
#
# shuffle_index_functions = [
#     lambda ind: ind,
#     lambda ind: (5 * ind + 1) % 16,
#     lambda ind: (3 * ind + 5) % 16,
#     lambda ind: (7 * ind) % 16,
# ]
#
# def left_rotate(val, amnt):
#     val &= 0xFFFFFFFF
#     return ((val << amnt) | (val >> (32 - amnt))) & 0xFFFFFFFF
#
# # Hash the incoming bytearray
# def hash(data):
#     data = bytearray(data)
#     # calculate the length of data in bits and L_AND that with 0xFFFFFFFFFFFFFFFF to restrict the size to 64 bits
#     data_length = (8 * len(data)) & 0xFFFFFFFFFFFFFFFF
#     # Append the first padding bit
#     data.append(0x80)
#     # Pad data with zeroes until it is correctly size aligned
#     while len(data) % 64 != 56:
#         data.append(0x00)
#     # Append the data length to the data byte array in little endian order
#     data += data_length.to_bytes(8, byteorder="little")
#
#     bits_and_pieces = initial_counter_values[:]
#
#     # Loop through all of the data in 512 bit (64 byte, hence the 64 step) chunks
#     for chunk_512 in range(0, len(data), 64):
#         a, b, c, d = bits_and_pieces
#         # Obtain 512 bits (64 bytes) of data (the current chunk)
#         current_chunk = data[chunk_512:chunk_512+64]
#         for i in range(64):
#             # calculates the index to get the correct function from the arrays
#             ind = math.floor(i / 16)
#             # Calls the correct lambda to process the values
#             f = bitwise_functions[ind](b, c, d)
#             g = shuffle_index_functions[ind](i)
#             # Calculates the value to be rotated
#             pre_rotation_value = a + f + constants[i] + int.from_bytes(current_chunk[4*g:4*g+4], byteorder="little")
#             # Gets the correct new b value after rotation, the 0xFFFFFFFF is used to ensure that the ouput is limited to 8 bytes
#             post_rotation_value = (b + left_rotate(pre_rotation_value, rotation_arr[i])) & 0xFFFFFFFF
#             a, b, c, d = d, post_rotation_value, b, c
#         for i, val in enumerate([a, b, c, d]):
#             bits_and_pieces[i] += val
#             bits_and_pieces[i] &= 0xFFFFFFFF
#
#         return sum(x << (32 * i) for i, x in enumerate(bits_and_pieces))


def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

if __name__ == "__main__":
    print(md5_to_hex(MD5().hash("poop".encode())))
