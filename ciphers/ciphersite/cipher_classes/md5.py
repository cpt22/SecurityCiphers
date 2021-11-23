import math


# Sources:
# https://www.educba.com/md5-alogrithm/
# https://en.wikipedia.org/wiki/MD5#Algorithm
class MD5:
    # Buffer values in little endian format
    initial_abcd = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

    F = lambda self, x, y, z: (x & y) | (~x & z)
    G = lambda self, x, y, z: (x & z) | (y & ~z)
    H = lambda self, x, y, z: x ^ y ^ z
    I = lambda self, x, y, z: y ^ (x | ~z)

    rotation_arr = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                    5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    constants = [int(math.floor(2**32 * abs(math.sin(i + 1)))) & 0xFFFFFFFF for i in range(64)]

    def hash(self, data):
        data = bytearray(data)
        length = (8 * len(data)) & 0xffffffffffffffff
        data.append(0x80)
        while (len(data) * 8) % 64 != 56:
            data.append(0x00)
        data += length.to_bytes(8, byteorder="little")

        a0, b0, c0, d0 = self.initial_abcd[0:4]

        # Loop through the data in 512 bit chunks. The step is 64 since 64 bytes *8 bits/byte = 512 bits
        for chunk_512 in range(0, len(data), 64):
            chunk = data[chunk_512:chunk_512 + 64]
            a, b, c, d = a0, b0, c0, d0
            
            for i in range(64):
                print(f'i:{i}, b:{b}, c:{c}, d:{d}')
                if i in range(16):
                    print(chunk)
                    f = self.F(b, c, d)
                    g = i
                elif i in range(16, 32):
                    print("b")
                    f = self.G(b, c, d)
                    g = (5 * i + 1) % 16
                elif i in range(32, 48):
                    print("c")
                    f = self.H(b, c, d)
                    g = (3 * i + 5) % 16
                elif i in range(48, 64):
                    print("d")
                    f = self.I(b, c, d)
                    g = (7 * i) % 16

                rot = a + f + self.constants[i] + int.from_bytes(chunk[4*g:4*g+4], byteorder='little')
                rot_output = (b + self.left_rotate(rot, self.rotation_arr[i])) & 0xFFFFFFFF
                a = d
                b = rot_output
                c = b
                d = c

            a0 = (a + a0) & 0xFFFFFFFF
            b0 = (b + b0) & 0xFFFFFFFF
            c0 = (c + c0) & 0xFFFFFFFF
            d0 = (d + d0) & 0xFFFFFFFF

            items = [a0 << 0, b0 << 32, c0 << 64, d0 << 96]

        return sum(items) #sum(x << (32*i) for i, x in enumerate(items))

    def left_rotate(self, x, amnt):
        x &= 0xFFFFFFFF
        return ((x << amnt) | (x >> (32 - amnt))) & 0xFFFFFFFF


def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

if __name__ == "__main__":
    st = "poop".encode('utf-8')
    md5 = MD5()
    #out = md5(st)
    out = md5.hash(st)
    print(md5_to_hex(out))
    #print(out)
