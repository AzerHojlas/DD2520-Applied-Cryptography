# Author: Azer Hojlas
# Date: 2023-01-26
# Functionality: Encode and decode text using key; find IOC of text and period (keylength) of ciphertext; brute force 
#                for keys with key size n < 6; statistical analysis for keys > 6
#
# Usage: Run file and simply input filename or path, the code will take care of the rest

from itertools import permutations
import enchant
import time
import re
from collections import Counter
from operator import itemgetter

# Global variables
check_if_english = enchant.Dict("en_US")
alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#"
english_index_of_coincidence = 0.0660

# Counts the index of coincidence of a text
def index_of_coincidence(text):
    counter = Counter(text)
    total = sum(counter.values())
    sum_for_each = 0
    for i in alphabet:
        sum_for_each = sum_for_each + counter[i]*(counter[i] - 1)
    return (sum_for_each / (total*(total - 1)))

# Builds a list with strings built with every nth letter of a string, iteratively
def slice_into_groupings(text, n):
    return [text[i::n] for i in range(n)]

# Divides ciphertext into groupings, the n-size numbered grouping with the highest ioc is the key-size, and multiples of it
def period_finder(text):
    list_of_strings = []
    for i in range(1, len(alphabet)):
        list_of_strings.append(slice_into_groupings(text, i))

    dict_of_IOCs = {}

    for list in list_of_strings:
        sum_average = 0
        for string in list:
            ioc = index_of_coincidence(string)
            sum_average = sum_average + ioc
        dict_of_IOCs[len(list)] = sum_average / len(list)

    return dict_of_IOCs

# Find the key given frequency analysis of the groupings based on key length
def key_finder(ciphertext, n):
    list_of_strings = slice_into_groupings(ciphertext, n)
    key = []
    for text in list_of_strings:
        letter_scores = []
        for letter in alphabet:
            decoded = decode(text, letter)
            decoded_score = is_english(decoded)
            letter_scores.append([letter, decoded_score])
        letter_scores_sorted = sorted(letter_scores, key=itemgetter(1))
        key.append(letter_scores_sorted[-1][0])        
    return listToString(key)

# Give a score based on the frequency of common english letters
def is_english(text):
    score = 0
    counted = Counter(sorted(text)).most_common()
    if (counted[0][0] == '_' or counted[0][0] == 'E'):
        score = score + 1
    if (counted[1][0] == '_' or counted[1][0] == 'E'):
        score = score + 1
    if (counted[2][0] == '_' or counted[2][0] == 'E' or counted[2][0] == 'A'):
        score = score + 1
    return score


# imports a text file
def import_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

# Converts list to string
def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

# Takes the key and repeats it until it matches the length of the ciphertext
def key_matcher(text, key):
    key = list(key)
    for i in range(len(text) - len(key)):
        key.append(key[i % len(key)])
    return("" . join(key))

# Takes plaintext and key and creates a vigenere ciphertext
def encode(plaintext, key):
    key_elongated = key_matcher(plaintext, key)
    cipher_text = []
    for i in range(len(plaintext)):
        index = (alphabet.find(plaintext[i]) + alphabet.find(key_elongated[i])) % len(alphabet)
        letter = alphabet[index]
        cipher_text.append(letter)
    return("" . join(cipher_text))

# Takes ciphertext and key and decodes into plaintext
def decode(ciphertext, key):
    key_elongated = key_matcher(ciphertext, key)
    cipher_text = []
    for i in range(len(ciphertext)):
        index = (alphabet.find(ciphertext[i]) - alphabet.find(key_elongated[i])) % len(alphabet)
        letter = alphabet[index]
        cipher_text.append(letter)
    return("" . join(cipher_text))

# Finds all key permutations given a key size n. Used for brute force
def key_generator(n_gram):
    return tuple_to_string_list(list(permutations(alphabet, n_gram)))

# Converts tuple to string
def tuple_to_string_list(tuple_list):
    remade = []
    for i in tuple_list:
        remade.append("" . join(i))
    return remade

# Declared checker as a global variable, which saves a lot of time. Checks for the amount of english words in decoded text
def amount_english_words(text):
    splitted = re.split(r'_|#', text)
    correct_words = 0
    for word in splitted:
        if (len(word) < 2):
            continue
        if (check_if_english.check(word) == True):
            correct_words = correct_words + 1
    return correct_words

# Brute force guesses keys until correct one is found, each text is checked if written in english. Feasable up to key size 4
def brute_force(ciphertext, cutoff, n_keys):
    shortened = ciphertext[:cutoff] 
    keys = key_generator(n_keys)
    lookup = {}
    for key in keys:
        plaintext = decode(shortened, key)
        lookup[key] = amount_english_words(plaintext)
    descending = sorted(lookup.items(), key = lambda x: x[1], reverse = True)
    print("\n")
    print(decode(shortened, descending[0][0]))
    print("\n")
    print("Second closest key with corresponding correct amount of words: " + str(descending[1]))
    print("Closest key with corresponding correct amount of words: " + str(descending[0]))
    print("\n")

# Can be used for any key size
def statistical_analysis(ciphertext):
    ciphertext_cleaned = re.split(r'_|#', ciphertext)
    key_sizes = []
    table = period_finder(ciphertext)
    for length in table:
        if (table[length] > english_index_of_coincidence):
            key_sizes.append(length)
    for n in key_sizes:
        key = key_finder(ciphertext, n)
        decoded = decode(ciphertext, key)
        if ((amount_english_words(decoded) / len(ciphertext_cleaned)) > 0.8):
            print(decoded, "\n\n", "key length: ", n, "\n\n", "Key: ", key)
            break
        else:
            print("key not found")


def main():
   
    start_time = time.time()
    ciphertext = import_text(input("Please input filepath or filename of ciphertext: "))
    statistical_analysis(ciphertext)
    print("\n Runtime: %s seconds \n" % (time.time() - start_time))
    

if __name__ == "__main__":
    main()

