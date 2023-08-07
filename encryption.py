from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext, cipher.iv

def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_data, AES.block_size)
    return plaintext


if __name__ == "__main__":
    # Example usage
    key = get_random_bytes(16)
    plaintext = b"Hello, world! This is a secret message."

    ciphertext, iv = encrypt(plaintext, key)
    decrypted_text = decrypt(ciphertext, key, iv)

    print("Original message:", plaintext.decode())
    print("Decrypted message:", decrypted_text.decode())
