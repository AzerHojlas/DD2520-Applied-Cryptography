import sys
import itertools

# Global variables 
########################################################################################################################################################################################################################
#  Sbox tuple
Sbox_tuple = (0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, 0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, 0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, 0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB, 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08, 0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF, 0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16)
Round_constants = (0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x1b000000, 0x36000000)

# Mixed columns lookup table
mul_02 = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254, 27, 25, 31, 29, 19, 17, 23, 21, 11, 9, 15, 13, 3, 1, 7, 5, 59, 57, 63, 61, 51, 49, 55, 53, 43, 41, 47, 45, 35, 33, 39, 37, 91, 89, 95, 93, 83, 81, 87, 85, 75, 73, 79, 77, 67, 65, 71, 69, 123, 121, 127, 125, 115, 113, 119, 117, 107, 105, 111, 109, 99, 97, 103, 101, 155, 153, 159, 157, 147, 145, 151, 149, 139, 137, 143, 141, 131, 129, 135, 133, 187, 185, 191, 189, 179, 177, 183, 181, 171, 169, 175, 173, 163, 161, 167, 165, 219, 217, 223, 221, 211, 209, 215, 213, 203, 201, 207, 205, 195, 193, 199, 197, 251, 249, 255, 253, 243, 241, 247, 245, 235, 233, 239, 237, 227, 225, 231, 229)
mul_03 = (0, 3, 6, 5, 12, 15, 10, 9, 24, 27, 30, 29, 20, 23, 18, 17, 48, 51, 54, 53, 60, 63, 58, 57, 40, 43, 46, 45, 36, 39, 34, 33, 96, 99, 102, 101, 108, 111, 106, 105, 120, 123, 126, 125, 116, 119, 114, 113, 80, 83, 86, 85, 92, 95, 90, 89, 72, 75, 78, 77, 68, 71, 66, 65, 192, 195, 198, 197, 204, 207, 202, 201, 216, 219, 222, 221, 212, 215, 210, 209, 240, 243, 246, 245, 252, 255, 250, 249, 232, 235, 238, 237, 228, 231, 226, 225, 160, 163, 166, 165, 172, 175, 170, 169, 184, 187, 190, 189, 180, 183, 178, 177, 144, 147, 150, 149, 156, 159, 154, 153, 136, 139, 142, 141, 132, 135, 130, 129, 155, 152, 157, 158, 151, 148, 145, 146, 131, 128, 133, 134, 143, 140, 137, 138, 171, 168, 173, 174, 167, 164, 161, 162, 179, 176, 181, 182, 191, 188, 185, 186, 251, 248, 253, 254, 247, 244, 241, 242, 227, 224, 229, 230, 239, 236, 233, 234, 203, 200, 205, 206, 199, 196, 193, 194, 211, 208, 213, 214, 223, 220, 217, 218, 91, 88, 93, 94, 87, 84, 81, 82, 67, 64, 69, 70, 79, 76, 73, 74, 107, 104, 109, 110, 103, 100, 97, 98, 115, 112, 117, 118, 127, 124, 121, 122, 59, 56, 61, 62, 55, 52, 49, 50, 35, 32, 37, 38, 47, 44, 41, 42, 11, 8, 13, 14, 7, 4, 1, 2, 19, 16, 21, 22, 31, 28, 25, 26)
########################################################################################################################################################################################################################

# Puts first x amount of bytes in last place, if positions = 3 then first 3 bytes are appended to the last place
def rotate_word_positions_int(word, positions):
    give_back = ((word << (8 * positions)) | (word >> (32 - (8 * positions)))) & 0xffffffff
    return give_back

# Find corresponding byte in substitution box and substitute, return the word
def substitute_word_int(word):
    byte1 = Sbox_tuple[(word >> 24) & 0xffffffff] << 24
    byte2 = Sbox_tuple[(word >> 16) & 0x00ff] << 16 
    byte3 = Sbox_tuple[(word >> 8) & 0x0000ff] << 8
    byte4 = Sbox_tuple[word & 0x000000ff]
    return (byte1 | byte2 | byte3 | byte4)

# XORS a word that has just been substituted with the appropriate round constant
def round_xor_int(word, constant):
    give_back = word ^ Round_constants[constant]
    return give_back

# Makes a list of 44 int words from the original key
def key_expansion_int():
    block = sys.stdin.buffer.read(16)
    block_int = int.from_bytes(block, 'big')
    words_int = [(block_int & 0xffffffff000000000000000000000000) >> 96, (block_int & 0x00000000ffffffff0000000000000000) >> 64, (block_int & 0x0000000000000000ffffffff00000000) >> 32, block_int & 0x000000000000000000000000ffffffff]
    
    increment = 4
    round_increment = 0
    while (increment < 43):
        xored = words_int[increment - 4] ^ round_xor_int(substitute_word_int(rotate_word_positions_int(words_int[increment - 1], 1)), round_increment)
        words_int.append(xored)
        for d in range(3):
            xored = words_int[-1] ^ words_int[increment - 3 + d]
            words_int.append(xored)
        increment = increment + 4
        round_increment = round_increment + 1
    return words_int

# Encrypt each block separately, then send out to Standard output
def encrypt():
    keys = key_expansion_int()

    block = sys.stdin.buffer.read(16)        
    block_int = int.from_bytes(block, 'big')
    block_word_1 = (block_int & 0xffffffff000000000000000000000000) >> 96  
    block_word_2 = (block_int & 0x00000000ffffffff0000000000000000) >> 64
    block_word_3 = (block_int & 0x0000000000000000ffffffff00000000) >> 32
    block_word_4 = block_int & 0x000000000000000000000000ffffffff
    
    while (block):
        lst = add_round_key_block(block_word_1, block_word_2, block_word_3, block_word_4, keys[0], keys[1], keys[2], keys[3])
        for d in range(4, 44, 4):
            lst = substitute_blocks(lst[0], lst[1], lst[2], lst[3])
            lst = shift_rows_block(lst[0], lst[1], lst[2], lst[3])
            if (d != 40):
                lst = mix_columns_block(lst[0], lst[1], lst[2], lst[3])
            lst = add_round_key_block(lst[0], lst[1], lst[2], lst[3], keys[d], keys[d + 1], keys[d + 2], keys[d + 3])

        give_back = bytes(list(itertools.chain.from_iterable(divide(lst))))
        sys.stdout.buffer.write(give_back)
        
        block = sys.stdin.buffer.read(16)
        block_int = int.from_bytes(block, 'big')
        block_word_1 = (block_int & 0xffffffff000000000000000000000000) >> 96  
        block_word_2 = (block_int & 0x00000000ffffffff0000000000000000) >> 64
        block_word_3 = (block_int & 0x0000000000000000ffffffff00000000) >> 32
        block_word_4 = block_int & 0x000000000000000000000000ffffffff

# Divides the block (list of words) into a list of bytes so that it is compatible with the bytes(function)  
def divide(lst):
    new_lst = []
    for word in lst:
        new_lst.append([(word & 0xff000000) >> 24, (word & 0x00ff0000) >> 16, (word & 0x0000ff00) >> 8, word & 0x000000ff])
    return new_lst

# add a round key to 4 block words
def add_round_key_block(word1, word2, word3, word4, keyword1, keyword2, keyword3, keyword4):
    return [word1 ^ keyword1, word2 ^ keyword2, word3 ^ keyword3, word4 ^ keyword4]

# Takes 4 words and substitutes them with Sbox
def substitute_blocks(word1, word2, word3, word4):
    return [substitute_word_int(word1), substitute_word_int(word2), substitute_word_int(word3), substitute_word_int(word4)]

# Shifts rows by first making transposes of the block column implementation, and then rotates said transposes
# Finally, the transposes are reverted to columns
def shift_rows_block(word1, word2, word3, word4):

    transpose1 = (word1 & 0xff000000) | ((word2 & 0xff000000) >> 8) | ((word3 & 0xff000000) >> 16) | ((word4 & 0xff000000) >> 24)
    transpose2 = ((word1 & 0x00ff0000) << 8) | (word2 & 0x00ff0000) | ((word3 & 0x00ff0000) >> 8) | ((word4 & 0x00ff0000) >> 16)
    transpose3 = ((word1 & 0x0000ff00) << 16) | ((word2 & 0x0000ff00) << 8) | (word3 & 0x0000ff00) | ((word4 & 0x0000ff00) >> 8)
    transpose4 = ((word1 & 0x000000ff) << 24) | ((word2 & 0x000000ff) << 16) | ((word3 & 0x000000ff) << 8) | (word4 & 0x000000ff)
    
    transpose2_shifted = rotate_word_positions_int(transpose2, 1)
    transpose3_shifted = rotate_word_positions_int(transpose3, 2)
    transpose4_shifted = rotate_word_positions_int(transpose4, 3)
   
    reverted1 = (transpose1 & 0xff000000) | ((transpose2_shifted & 0xff000000) >> 8) | ((transpose3_shifted & 0xff000000) >> 16) | ((transpose4_shifted & 0xff000000) >> 24)
    reverted2 = ((transpose1 & 0x00ff0000) << 8) | (transpose2_shifted & 0x00ff0000) | ((transpose3_shifted & 0x00ff0000) >> 8) | ((transpose4_shifted & 0x00ff0000) >> 16)
    reverted3 = ((transpose1 & 0x0000ff00) << 16) | ((transpose2_shifted & 0x0000ff00) << 8) | (transpose3_shifted & 0x0000ff00) | ((transpose4_shifted & 0x0000ff00) >> 8)
    reverted4 = ((transpose1 & 0x000000ff) << 24) | ((transpose2_shifted & 0x000000ff) << 16) | ((transpose3_shifted & 0x000000ff) << 8) | (transpose4_shifted & 0x000000ff)

    return [reverted1, reverted2, reverted3, reverted4]

# Mixes columns according to the constant matrix. I have skipped galois calculations due to them being too time consuming
# Instead, lookup tables are used
def mix_columns_block(word1, word2, word3, word4):
    word_1_1 = (mul_02[(word1 & 0xff000000) >> 24] ^ mul_03[((word1 & 0x00ff0000) >> 16)] ^ ((word1 & 0x0000ff00) >> 8) ^ (word1 & 0x000000ff)) << 24
    word_1_2 = (((word1 & 0xff000000) >> 24) ^ mul_02[((word1 & 0x00ff0000) >> 16)] ^ mul_03[((word1 & 0x0000ff00) >> 8)] ^ (word1 & 0x000000ff)) << 16
    word_1_3 = (((word1 & 0xff000000) >> 24) ^ ((word1 & 0x00ff0000) >> 16) ^ mul_02[((word1 & 0x0000ff00) >> 8)] ^ mul_03[(word1& 0x000000ff)]) << 8
    word_1_4 = mul_03[((word1 & 0xff000000) >> 24)] ^ ((word1& 0x00ff0000) >> 16) ^ ((word1& 0x0000ff00) >> 8) ^ mul_02[(word1& 0x000000ff)]
    finished1 = word_1_1 | word_1_2 | word_1_3 | word_1_4

    word_2_1 = (mul_02[(word2 & 0xff000000) >> 24] ^ mul_03[((word2 & 0x00ff0000) >> 16)] ^ ((word2 & 0x0000ff00) >> 8) ^ (word2 & 0x000000ff)) << 24
    word_2_2 = (((word2 & 0xff000000) >> 24) ^ mul_02[((word2 & 0x00ff0000) >> 16)] ^ mul_03[((word2 & 0x0000ff00) >> 8)] ^ (word2 & 0x000000ff)) << 16
    word_2_3 = (((word2 & 0xff000000) >> 24) ^ ((word2 & 0x00ff0000) >> 16) ^ mul_02[((word2 & 0x0000ff00) >> 8)] ^ mul_03[(word2 & 0x000000ff)]) << 8
    word_2_4 = mul_03[((word2 & 0xff000000) >> 24)] ^ ((word2 & 0x00ff0000) >> 16) ^ ((word2 & 0x0000ff00) >> 8) ^ mul_02[(word2 & 0x000000ff)]
    finished2 = word_2_1 | word_2_2 | word_2_3 | word_2_4

    word_3_1 = (mul_02[(word3 & 0xff000000) >> 24] ^ mul_03[((word3 & 0x00ff0000) >> 16)] ^ ((word3 & 0x0000ff00) >> 8) ^ (word3 & 0x000000ff)) << 24
    word_3_2 = (((word3 & 0xff000000) >> 24) ^ mul_02[((word3 & 0x00ff0000) >> 16)] ^ mul_03[((word3 & 0x0000ff00) >> 8)] ^ (word3 & 0x000000ff)) << 16
    word_3_3 = (((word3 & 0xff000000) >> 24) ^ ((word3 & 0x00ff0000) >> 16) ^ mul_02[((word3 & 0x0000ff00) >> 8)] ^ mul_03[(word3 & 0x000000ff)]) << 8
    word_3_4 = mul_03[((word3 & 0xff000000) >> 24)] ^ ((word3 & 0x00ff0000) >> 16) ^ ((word3 & 0x0000ff00) >> 8) ^ mul_02[(word3 & 0x000000ff)]
    finished3 = word_3_1 | word_3_2 | word_3_3 | word_3_4

    word_4_1 = (mul_02[(word4 & 0xff000000) >> 24] ^ mul_03[((word4 & 0x00ff0000) >> 16)] ^ ((word4 & 0x0000ff00) >> 8) ^ (word4 & 0x000000ff)) << 24
    word_4_2 = (((word4 & 0xff000000) >> 24) ^ mul_02[((word4 & 0x00ff0000) >> 16)] ^ mul_03[((word4 & 0x0000ff00) >> 8)] ^ (word4 & 0x000000ff)) << 16
    word_4_3 = (((word4 & 0xff000000) >> 24) ^ ((word4 & 0x00ff0000) >> 16) ^ mul_02[((word4 & 0x0000ff00) >> 8)] ^ mul_03[(word4 & 0x000000ff)]) << 8
    word_4_4 = mul_03[((word4 & 0xff000000) >> 24)] ^ ((word4 & 0x00ff0000) >> 16) ^ ((word4 & 0x0000ff00) >> 8) ^ mul_02[(word4 & 0x000000ff)]
    finished4 = word_4_1 | word_4_2 | word_4_3 | word_4_4

    return [finished1, finished2, finished3, finished4]

encrypt()