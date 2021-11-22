class DESCipher:
    IP_table = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48,
                40,
                32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13,
                5,
                63, 55, 47, 39, 31, 23, 15, 7]
    FP_table = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45,
                13,
                53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58,
                26,
                33, 1, 41, 9, 49, 17, 57, 25]
    right_expansion_table = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17,
                             18,
                             19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    s_box_table = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

                   [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

                   [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

                   [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

                   [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

                   [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

                   [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

                   [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
    right_perm_table = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13,
                        30, 6, 22, 11, 4, 25]
    key_table_56 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52,
                    44,
                    36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28,
                    20,
                    12, 4]
    key_table_48 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31,
                    37,
                    47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    keys = []

    def generate_keys(self, key):
        # Step 1: permute to 56 bits
        key_56 = self.permute(key, self.key_table_56)
        # Step 2: chop key in half
        key_part_1 = key_56[:28]
        key_part_2 = key_56[28:]

        # Generate 16 keys
        shift_table = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)
        for index in range(0, 16):
            # Step 3: perform left shift amount of times designated in shift table
            for _ in range(0, shift_table[index]):
                key_part_1.append(key_part_1[0])
                key_part_1.pop(0)
                key_part_2.append(key_part_2[0])
                key_part_2.pop(0)
            # Step 4: recombine and permute to 48 bits
            key_combo = key_part_1 + key_part_2
            key_48 = self.permute(key_combo, self.key_table_48)
            # Step 5: add key to table
            self.keys.append(key_48)

    def s_box(self, arr_48):
        arr_32 = []
        # Do s box for each chunk of 6
        s_box_index = 0
        index = 0
        while s_box_index < 8:
            part = arr_48[index:index + 6]
            row_str = str(part[0]) + str(part[5])
            row_int = int(row_str, 2)
            column_str = ''.join(format(str(i)) for i in part[1:5])
            column_int = int(column_str, 2)
            s_box_int = self.s_box_table[s_box_index][row_int][column_int]
            for i in format(s_box_int, 'b').zfill(4):  # potentially do differently
                arr_32.append(int(i))
            s_box_index += 1
            index += 6
        return arr_32

    # Message and key inputs are arrays of binary (64 bits)
    def des(self, message, key, input_range):
        # Generate 16 keys
        self.generate_keys(key)

        # Start DES
        # Step 1: perform initial permutation
        initial_perm = self.permute(message, self.IP_table)

        # Step 2: chop in half
        left_32 = initial_perm[:32]
        right_32 = initial_perm[32:]

        # Step 3: repeat for each key
        for key_index in input_range:
            # Step 4: do stuff on right side
            # 32 bit to 48 bit expansion
            right_48 = self.permute(right_32, self.right_expansion_table)
            # XOR with subkey 1
            right_xor_48 = self.xor(right_48, self.keys[key_index])

            # s-box for each group of 6
            right_s_box_32 = self.s_box(right_xor_48)

            # Permutation
            right_perm_32 = self.permute(right_s_box_32, self.right_perm_table)
            # Step 5: do stuff on left side
            # Set left side equal to right side
            new_left_32 = right_32
            # XOR left with right_perm_32
            right_32 = self.xor(left_32, right_perm_32)
            # Update left_32 var to be equal to original right side
            left_32 = new_left_32

        # Step 6: switch right and left
        final_64 = right_32 + left_32
        final_perm = self.permute(final_64, self.FP_table)
        hex_val = hex(int(''.join(format(str(i)) for i in final_perm), 2))[2:]
        return final_perm, hex_val

    def des_helper(self, message_bit_arr, key_bit_arr, input_range):
        final_bin = []
        final_hex_val = ""
        index = 64
        while index <= len(message_bit_arr):
            bin_arr, hex_val = self.des(message_bit_arr[index - 64:index], key_bit_arr, input_range)
            final_bin += bin_arr
            final_hex_val += hex_val
            index += 64
        # Add padding if not all bytes were covered
        if index - 64 < len(message_bit_arr):
            pad_message_bit_arr = message_bit_arr[index - 64:]
            while len(pad_message_bit_arr) != 64:
                pad_message_bit_arr.append(0)
            bin_arr, hex_val = self.des(pad_message_bit_arr, key_bit_arr, input_range)
            final_bin += bin_arr
            final_hex_val += hex_val
        return self.hex_to_byte_array(final_hex_val)

    # Inputs are byte arrays
    def encrypt(self, message_byte_arr, key_byte_arr):
        message_bit_arr = self.byte_array_to_bit_array(message_byte_arr)
        key_bit_arr = self.byte_array_to_bit_array(key_byte_arr)
        return self.des_helper(message_bit_arr, key_bit_arr, range(0, 16))

    # Inputs are byte arrays
    def decrypt(self, message_byte_arr, key_byte_arr):
        message_bit_arr = self.byte_array_to_bit_array(message_byte_arr)
        key_bit_arr = self.byte_array_to_bit_array(key_byte_arr)
        return self.des_helper(message_bit_arr, key_bit_arr, range(15, -1, -1))

    @staticmethod
    def permute(input_arr, table):
        permutation = []
        for i in range(0, len(table)):
            permutation.append(input_arr[table[i] - 1])
        return permutation

    @staticmethod
    def xor(arr1, arr2):
        xor_list = []
        index = 0
        while index < len(arr1):
            xor_list.append(arr1[index] ^ arr2[index])
            index += 1
        return xor_list

    @staticmethod
    def byte_array_to_bit_array(byte_array):
        bit_array = []
        for byte in byte_array:
            bit_array += list(map(int, format(byte, '#010b')[2:]))
        return bit_array

    @staticmethod
    def bit_array_to_string(bit_array):
        bin_string = ''.join(str(i) for i in bit_array)
        binary_int = int(bin_string, 2)
        byte_number = binary_int.bit_length() + 7 // 8
        binary_array = binary_int.to_bytes(byte_number, "big")
        return binary_array.decode()

    @staticmethod
    def hex_to_ascii(hex_value):
        return bytearray.fromhex(hex_value).decode()

    @staticmethod
    def hex_to_byte_array(hex_value):
        return bytearray(bytes.fromhex(hex_value))
