from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Random import get_random_bytes
import ChaCha20


def RSA_Generate_Keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def Create_Session_Key(public_key):
    recipient_key = RSA.import_key(public_key)
    session_key = get_random_bytes(32)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    return session_key, enc_session_key

def RSA_Encrypt(public_key, data):
    session_key, enc_session_key = Create_Session_Key(public_key)

    package, x = ChaCha20.create_chacha20_cipher_package(header=enc_session_key, plaintext=data, key=session_key)

    return package

def RSA_Decrypt(private_key, package):
    try:
        stuff = RSA.import_key(private_key)

        dec_package = ChaCha20.decode_package(package)

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(stuff)
        session_key = cipher_rsa.decrypt(dec_package['header'])

        return ChaCha20.can_decrypt(session_key, package)
    except ValueError:
        print("Incorrect decryption")
        return False, None
    
def create_keypairs(number):
    key_list = [] 
    for i in range(number):
        private_key, public_key = RSA_Generate_Keys()
        t =  [private_key, public_key]
        print("Created keypair " + str(i))
        key_list.append(t)
    return key_list

