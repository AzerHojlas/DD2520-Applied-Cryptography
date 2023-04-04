
# Difference between desired length and unpadded length modulo desired length is both the amount of bytes to add and the 
# specific byte to add
def pad(unpadded, desired_length):
    add_amount_and_pad = desired_length - (len(unpadded) % desired_length)
    for i in range(add_amount_and_pad):
        unpadded += bytes([add_amount_and_pad])
    return unpadded

def main():
    block = b"YELLOW SUBMARINE"
    desired_length = 20
    padded = pad(block, desired_length)
    print(padded)

if __name__ == "__main__":
    main()