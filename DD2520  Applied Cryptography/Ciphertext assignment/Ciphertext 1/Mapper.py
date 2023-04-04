# Author: Azer Hojlas
# Usage: simply run the program with "Ciphertext_1.txt" in the same directory and the text will be decoded
# Date: 2023-01-26

# Shifts a letter n steps in the alphabet
def letter_shifter(letter, steps):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#"
    index = alphabet.find(letter)
    newLetterIndex = (index + steps) % len(alphabet) 
    return alphabet[newLetterIndex]

# Finds the distance between two letters, made out of laziness so that i don't have to count manually
def distance_calculator(letter, secondLetter):
    alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#"
    return alphabet.find(secondLetter) - alphabet.find(letter)

# Simply imports a text with a given file path
def import_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

# Used earlier, tried all steps from 1 to 38 without result
def caesar_decryptor(ciphertext_filepath, step):
    newText = ""
    ciphertext = import_text(ciphertext_filepath)
    for i in range(len(ciphertext)):
        newText += letter_shifter(ciphertext[i], step)
    return newText

# Decoding table I created by manually checking the ocurrence of each letter, mostly a result of trial and error
def ciphertext_1_mapper():
    ciphertext = import_text("Ciphertext_1.txt")
    decode_table = {
        "W": "A",
        "J": "B",
        "6": "C",
        "V": "D",
        "I": "E",
        "5": "F",
        "U": "G",
        "H": "H",
        "4": "I",
        "T": "J",
        "G": "K",
        "3": "L",
        "S": "M",
        "F": "N",
        "2": "O",
        "R": "P",
        "E": "Q",
        "1": "R",
        "Q": "S",
        "D": "T",
        "0": "U",
        "P": "V",
        "C": "W",
        "#": "X",
        "O": "Y",
        "B": "Z",
        "N": "\n",
        "_": " "
    }
    decoded_text = ""
    for i in ciphertext:
        decoded_text += decode_table.get(i)
    return decoded_text

print(ciphertext_1_mapper())