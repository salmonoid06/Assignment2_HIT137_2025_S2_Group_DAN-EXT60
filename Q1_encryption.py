# Encrypts the contents of 'raw_text.txt' using a shift-based cipher
def encrypt_file(shift1: int, shift2: int):
    # Read the raw input text
    with open("raw_text.txt", "r") as file:
        raw_text = file.read()
    # Stores encrypted characters
    encrypted_chars = []  
    # Stores metadata tags for decryption
    meta_chars = []       

    for ch in raw_text:
        # Encrypts lowercase letters
        if ch.islower():
            # Determines if the character is in the first have of the alphabet
            if ch <= 'm':
                # Applies positive shift based on product of shifts
                new_ch = chr(((ord(ch) - ord('a') + (shift1 * shift2)) % 26) + ord('a'))
                tag = '0'  # Tag for this encryption rule
            else:
                # Applies negative shift based on sum of shifts
                new_ch = chr(((ord(ch) - ord('a') - (shift1 + shift2)) % 26) + ord('a'))
                tag = '1'
        # Encrypts uppercase letters
        elif ch.isupper():
            # Determines if the character is in the first have of the alphabet
            if ch <= 'M':
                # Apply negative shift using shift1
                new_ch = chr(((ord(ch) - ord('A') - shift1) % 26) + ord('A'))
                tag = '2'
            else:
                # Apply positive shift using square of shift2
                new_ch = chr(((ord(ch) - ord('A') + (shift2 ** 2)) % 26) + ord('A'))
                tag = '3'
        else:
            # Non-alphabetic characters are unchanged
            new_ch = ch
            tag = '.'

        encrypted_chars.append(new_ch)
        meta_chars.append(tag)

    # Saves encrypted text and metadata to separate files
    with open("encrypted_text.txt", "w") as f:
        f.write("".join(encrypted_chars))

    with open("encrypted_meta.txt", "w") as f:
        f.write("".join(meta_chars))


# Decrypts the encrypted text using the metadata and shift values
def decrypt_file(shift1: int, shift2: int):
    # Reads encrypted text and metadata
    with open("encrypted_text.txt", "r") as f:
        encrypted_text = f.read()
    with open("encrypted_meta.txt", "r") as f:
        meta = f.read()

    # Checks if metadata length matches encrypted text
    if len(encrypted_text) != len(meta):
        raise ValueError("Meta file length does not match encrypted text length.")

    decrypted_chars = []

    # Reverses the encryption based on the metadata tags
    for ch, tag in zip(encrypted_text, meta):
        if tag == '0':
            new_ch = chr(((ord(ch) - ord('a') - (shift1 * shift2)) % 26) + ord('a'))
        elif tag == '1':
            new_ch = chr(((ord(ch) - ord('a') + (shift1 + shift2)) % 26) + ord('a'))
        elif tag == '2':
            new_ch = chr(((ord(ch) - ord('A') + shift1) % 26) + ord('A'))
        elif tag == '3':
            new_ch = chr(((ord(ch) - ord('A') - (shift2 ** 2)) % 26) + ord('A'))
        elif tag == '.':
            new_ch = ch
        else:
            raise ValueError(f"Unknown meta tag '{tag}' encountered during decryption.")

        decrypted_chars.append(new_ch)

    # Saves the decrypted text to a file
    with open("decrypted_text.txt", "w") as f:
        f.write("".join(decrypted_chars))


# Verifies that the decrypted text matches the original raw text
def verify_decryption():
    with open("raw_text.txt", "r") as raw_file, open("decrypted_text.txt", "r") as dec_file:
        raw_content = raw_file.read()
        dec_content = dec_file.read()

    if raw_content == dec_content:
        print("Decryption successful. Decrypted text matches the original.")
    else:
        print("Decryption failed. Decrypted text does not match the original.")


def main():
    # Gets the shift values from user input
    shift1 = int(input("Enter shift1 (integer): "))
    shift2 = int(input("Enter shift2 (integer): "))

    # Runs the encryption, decryption, and verification
    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify_decryption()


if __name__ == "__main__":
    main()