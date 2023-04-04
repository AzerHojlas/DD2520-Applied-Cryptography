
# Imports a file from command prompt
def import_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

# Set does not take in duplicates
# len counts all instances
# the difference between len and set gives the amount of duplicates
def count(candidates_in_bytes):
    candidate_scores = []
    for candidate in candidates_in_bytes:
        lst = []
        for i in range(16, len(candidate), 16):
            lst.append(candidate[i - 16: i])
        score = len(lst) - len(set(lst))
        candidate_scores.append([candidate, score])
    
    return sorted(candidate_scores, key = lambda x: x[1], reverse = True)

def main():

    # Import the text and divide into ciphertexts
    text = import_text('aes_candidates.txt')
    candidates = text.split('\n')

    # Convert hex string to bytes
    candidates_in_bytes = []
    for hexed in candidates:
        candidates_in_bytes.append(bytes.fromhex(hexed))

    # Count repeating blocks in each and every ciphertext. The cipher with most repetitions is the ECB encrypted one
    scores = count(candidates_in_bytes)

    # Print out the best candidate
    print('\n' + 'Candidate most likely to be AES:\n')
    print(scores[0][0].hex() + '\n\n' + 'Ciphertext above has ' + str(scores[0][1]) + ' duplicate blocks \n')

if __name__ == "__main__":
    main()