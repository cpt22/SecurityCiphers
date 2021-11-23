import math


# Sources:
# https://www.educba.com/md5-alogrithm/
# https://www.rfc-editor.org/rfc/rfc1321 (MD5 RFC)
# https://en.wikipedia.org/wiki/MD5#Algorithm (Pseudo code was used from here to create this algorithm)
class MD5:
    rotation_arr = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                    5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    constants = [
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
    ]

    initial_counter_values = [
        0x67452301,
        0xefcdab89,
        0x98badcfe,
        0x10325476,
    ]

    @staticmethod
    def left_rotate(x, amount):
        # Logical ANDing with 0xFFFFFFFF ensures that the integers do not become too large
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    @staticmethod
    def hash(data):
        data = bytearray(data)
        # calculate the length of data in bits and logical and that with 0xFFFFFFFFFFFFFFFF to restrict the size to 64 bits
        data_length = (8 * len(data)) & 0xFFFFFFFFFFFFFFFF
        # Append the first padding bit
        data.append(0x80)
        # Pad data with zeroes until it is correctly size aligned
        while len(data) % 64 != 56:
            data.append(0x00)
        # Append the data length to the data byte array in little endian order
        data += data_length.to_bytes(8, byteorder="little")

        # duplicate the initial values into a new arr
        segments = MD5.initial_counter_values[:]

        # Loop through all of the data in 512 bit (64 byte, hence the 64 step) chunks
        for chunk_512 in range(0, len(data), 64):
            a, b, c, d = segments
            # Obtain 512 bits (64 bytes) of data (the current chunk)
            current_chunk = data[chunk_512:chunk_512+64]
            for i in range(64):
                # Run the appropriate function and calculate the correct G value for the index
                if i in range(16):
                    f = (b & c) | (~b & d)
                    g = i
                elif i in range(16, 32):
                    f = (b & d) | (c & ~d)
                    g = (5 * i + 1) % 16
                elif i in range(32, 48):
                    f = b ^ c ^ d
                    g = (3 * i + 5) % 16
                elif i in range(48, 64):
                    f = c ^ (b | ~d)
                    g = (7 * i) % 16

                # Calculates the value to be rotated
                pre_rotation_value = a + f + MD5.constants[i] + int.from_bytes(current_chunk[4*g:4*g+4], byteorder="little")
                # Gets the correct new b value after rotation, the 0xFFFFFFFF is used to ensure that the ouput is limited to 8 bytes
                post_rotation_value = (b + MD5.left_rotate(pre_rotation_value, MD5.rotation_arr[i])) & 0xFFFFFFFF
                # Shuffle the values
                a, b, c, d = d, post_rotation_value, b, c

            # Update the segments list with the new values
            for ind, val in enumerate([a, b, c, d]):
                segments[ind] += val
                segments[ind] &= 0xFFFFFFFF

        # Bit shift each of the segments so that we can sum them appropriately
        for i, val in enumerate(segments):
            segments[i] = val << (i * 32)

        # Sum all of the byte-shifted pieces
        return sum(segments)

    @staticmethod
    def hex_hash(data):
        output = MD5.hash(data)
        byte_arr = output.to_bytes(16, byteorder='little')
        big_endian_int = int.from_bytes(byte_arr, byteorder="big")
        return f'{big_endian_int:032x}'
