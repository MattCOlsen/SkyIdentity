import json
from base64 import b64encode
from base64 import b64decode
from Cryptodome.Cipher import ChaCha20_Poly1305
from Cryptodome.Random import get_random_bytes
import random
import string

def random_string(length = 32):
    alphabet = string.ascii_letters
    buffer = ''.join(random.choice(alphabet) for i in range(length))
    return buffer


def can_decrypt(key, package):
    try:        
        jv = decode_package(package)

        cipher = ChaCha20_Poly1305.new(key=key, nonce=jv['nonce'])
        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        #print("The message was: " + str(plaintext))
        return True, plaintext
    except ValueError:
        #print("Incorrect decryption")
        return False, None

def decode_package(package):
    b64 = json.loads(package)
    jk = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    return {k:b64decode(b64[k]) for k in jk}


def create_chacha20_cipher_package(header, plaintext=None, key=None):
    #header = header.encode('utf-8')

    if plaintext is None:
        plaintext = random_string().encode('utf-8')

    if key is None:
        key = get_random_bytes(32)

    cipher = ChaCha20_Poly1305.new(key=key)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    #encoded_header = b64encode(header).decode('utf-8')
    #decoded_haeder = b64decode(encoded_header) #so we just need to decode the header using b64encode

    encoded_nonce = b64encode(cipher.nonce).decode('utf-8')
    decoded_nonce = b64decode(encoded_nonce) #so we just need to decode the header using b64encode

    jk = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    jv = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, header, ciphertext, tag) ]
    package = json.dumps(dict(zip(jk, jv)))
    return package, key #key is unencrypted key
