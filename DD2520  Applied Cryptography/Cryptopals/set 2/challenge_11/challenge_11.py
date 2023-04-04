import random 
import base64
import aes_ecb
import aes_cbc
import sys

def pad(unpadded, desired_length):
    add_amount_and_pad = desired_length - (len(unpadded) % desired_length)
    for i in range(add_amount_and_pad):
        unpadded += bytes([add_amount_and_pad])
    return unpadded

# Generate a 16 byte key or IV
def generate_16_bytes():
    send_back = b''
    for i in range(16):
        send_back += bytes([random.randint(0, 255)])
    return send_back

def count(candidates_in_bytes):
    candidate_scores = []
    for candidate in candidates_in_bytes:
        lst = []
        for i in range(16, len(candidate), 16):
            lst.append(candidate[i - 16: i])
        score = len(lst) - len(set(lst))
        candidate_scores.append([candidate, score])
    
    return sorted(candidate_scores, key = lambda x: x[1], reverse = True)

def encryption_oracle(key_in_bytes, data_in_bytes):
    # data_based = base64.b64encode(pad(b'1' * random.randint(5, 10) + data_in_bytes + b'1' * random.randint(5, 10), 16))
    # data_adjusted = pad(b'1' * random.randint(5, 10) + data_in_bytes + b'1' * random.randint(5, 10), 16)
    data_adjusted = b'1' * random.randint(5, 10) + data_in_bytes + b'1' * random.randint(5, 10)

    iv_in_bytes = generate_16_bytes()

    decider = random.randint(0, 1)

    if (decider == 1):
        encrypted = aes_ecb.cryptopals_encrypt(key_in_bytes, data_adjusted)
        correct = 'ECB'
    if(decider == 0):
        encrypted = aes_cbc.cryptopals_encrypt(key_in_bytes, data_adjusted, iv_in_bytes)
        correct = 'CBC'

    score = count([encrypted])

    # print(str(score[0][1]) + '   ' + correct)

    if (score[0][1] > 0):
        return [encrypted, 'ECB', correct]
    else:
        return [encrypted, 'CBC', correct]
    

def main():

    # First decrypt and then encrypt tp check if they are the same
    # cryptopals_decrypt(password, import_text('challenge_input.txt'), initialization_vector)
    # cryptopals_encrypt(password, open("challenge_output.txt", "rb").read(), initialization_vector)
    
    key_in_bytes = generate_16_bytes()
    data_in_bytes = b'YELLOW SUBMARINE'*10
    guesses = []
    totals = 100
    for i in range(totals):
        guesses.append(encryption_oracle(key_in_bytes, data_in_bytes))

    amount_correct = 0

    for i in guesses:
        if(i[1] == i[2]):
            amount_correct += 1

    print('Correct guesses: ' + str(amount_correct) + ' out of: ' + str(totals))


if __name__ == "__main__":
    main()