from operator import itemgetter
import enchant

# Global variables ########################################################################################################
base_64 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/')
check_if_english = enchant.Dict("en_US")
###########################################################################################################################

# Helper Functions ########################################################################################################

# Imports a file from command prompt
def import_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

# Returns the amount of english words in a text
def amount_english_words(text):
    splitted = text.split()
    correct_words = 0
    for word in splitted:
        if (word.isalnum() == False):
            continue
        if (check_if_english.check(word) == True):
            correct_words = correct_words + 1
    return correct_words

###########################################################################################################################


# Challenge 1 #####################################################################
# Converts a hex string to base 64 string
def hex_to_base64(hex_string):
    number = int(hex_string, 16)
    broken_down = []

    for step in range(0, number.bit_length(), 6):
        broken_down.append((number & (63 * (2 ** step))) >> step)

    char_list = []
    for number in broken_down:
        char_list.append(base_64[number])

    char_list = list(reversed(char_list))
    return ''.join(char_list)

# Challenge 2 #####################################################################
# Xors two hex strings and returns the result
def fixed_xor(string1, string2):
    return hex(int(string1, 16) ^ int(string2, 16))[2:]

# Challenge 3 #####################################################################
# Takes a hex string which is caesar encoded with a single character. Function encodes the string with all common characters
# and checks which permutation result in an english translation. This char is the correct key
def single_byte_xor_cipher(hex_string):
    byte_list = bytes.fromhex(hex_string)
    permutations = []

    # 32 to 127 are relevant unicode characters, basically every char on the keyboard
    for i in range(0, 255):
        potential = b''
        for byte in byte_list:
            check = i ^ byte
            potential += bytes([check])
        permutations.append(potential)

    permutations_encoded = []

    for text in permutations:
        encodings = []
        for letter in text:
            encodings.append(chr(letter))
        permutations_encoded.append("".join(encodings))

    scoring = []
    for text in permutations_encoded:
        scoring.append([amount_english_words(text), text])
    in_order = sorted(scoring, key = itemgetter(0,1))
    return in_order[-1]

# Challenge 4 #####################################################################
# Checks which line out of multiple lines is caesar encrypted
def detect_single_character_xor(file):
    hex_strings = import_text(file).split('\n')
    highest = []
    for i in hex_strings:
        highest.append(single_byte_xor_cipher(i))
    in_order = sorted(highest, key = itemgetter(0,1))
    return in_order[-1][1]

# Challenge 5 #####################################################################
# encrypts a string with a key. Returns a hex string
def repeating_key_xor(text, key):
    key = key.encode()
    text = text.encode()
    xored = b''
    for i in range(len(text)):
        xored += bytes([key[i % 3] ^ text[i]])
    return xored.hex()

# Challenge 6 #####################################################################
def break_repeating_key_xor(base64d):
    

# print(single_byte_xor_cipher('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))
# print(amount_english_words('cooking MCs like a pound of bacon'))
# print(detect_single_character_xor('detect_single.txt'))
# if (repeating_key_xor('Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal', 'ICE') == '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'):
#     print(True)
