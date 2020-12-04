import RSA
import ChaCha20
import time
import random
from time import process_time as timer
import json
from base64 import b64encode
from base64 import b64decode


usleep = lambda x: time.sleep(x/1000000000.0)


#a lot could have been done here, but I wanted to reduce delay as much as possible in order to get closer to the "true" time for the process.  
#the original idea was to write it as a class with state machines to talk between two instances of the class, but that would have introduced
#the issue pushing and popping from the stack as the 
class RadioModule:
    def __init__(self, transmission_delay=None, processing_delay=None, id=None, publickeylist=None, private_key=None):
        #propogation delay is assumed to be almost non-existant 
        #Queuing Delay is inheritly introduced by needing to solve all packets
        if transmission_delay is None:
            self.transmission_delay = 500 #in nanoseconds
        else:
            self.transmission_delay = transmission_delay
        if processing_delay is None:
            self.processing_delay = 500
        else:
            self.processing_delay = processing_delay
        self.id = id
        self.publickeylist = publickeylist
        self.private_key = private_key
        self.sentNonce = None
        self.pointB_id = None # used in part three of the second handshake to further verify the sender's ID, ensure packet sent from orginal challenger

    def create_ChaCha20_Packages_and_keys(self, number):
        self.package_list = []
        self.key_list = []
        for i in range(number):
            header = ("drone" + str(i)).encode('utf-8')
            package, key = ChaCha20.create_chacha20_cipher_package(header)

            self.key_list.append(key)
            self.package_list.append(package)

        random.shuffle(self.package_list)


    def decrypt_ChaCha20_packages(self):        
        for p_number, package in enumerate(self.package_list):
            usleep(self.transmission_delay) # wait in getting the package
            for k_number, key in enumerate(self.key_list):
                successful_decrypt, plaintext = ChaCha20.can_decrypt(key, package)
                if successful_decrypt:
                    print("Successfull decrytion of package " + str(p_number) + " after " + str(k_number) + " attempts.")
                    break    

    def RSA_challenge(self, other):
        usleep(self.transmission_delay) # wait in getting the package
        first_response = other.respond_to_id(self.id)

        success, data = RSA.RSA_Decrypt(self.private_key, first_response)
        usleep(self.processing_delay)


        if success is False:
            print("Something went Wrong in decyrpting response")

        data = data.decode('utf-8')

        temp = data.split(',')
        # other's id, other's nonce, other's timestamp
        other_pkey = self.publickeylist[int(temp[0])]

        nonce = random.randint(0, 1000)
        self.sentNonce = nonce
        data = temp[1] + ", " + str(nonce) + ", " + str(self.id) + ", " + str(time.gmtime())
        data = data.encode('utf-8')

        self.pointB_id = int(temp[0])
        challenger_pkey = self.publickeylist[self.pointB_id]
        usleep(self.transmission_delay)
        package = RSA.RSA_Encrypt(challenger_pkey, data)
        usleep(self.processing_delay)


        nonce, timestamp = other.verify_nonce(package)

        usleep(self.transmission_delay)
        if self.sentNonce == nonce:
            return True
        return False



    def respond_to_id(self, challenger_id):
        usleep(self.transmission_delay) # wait in getting the package

        self.pointB_id = challenger_id
        challenger_pkey = self.publickeylist[challenger_id]
        nonce = random.randint(0, 1000)
        self.sentNonce = nonce
        data = str(self.id) + ", " + str(nonce) + ", " + str(time.gmtime())
        data = data.encode('utf-8')
        package = RSA.RSA_Encrypt(challenger_pkey, data)
        usleep(self.processing_delay)

        return package

    def verify_nonce(self, package):  
        usleep(self.transmission_delay) # wait in getting the package

        challenger_pkey = self.publickeylist[self.pointB_id]

        success, data = RSA.RSA_Decrypt(self.private_key, package)

        if success is False:
            print("Something went Wrong in decyrpting nonce")

        data = data.decode('utf-8')

        temp = data.split(',')
        # self's nonce, others's nonce, other's id, other's timestamp
        if int(temp[0]) != self.sentNonce:
            print("Returned Nonce was in error")

        if int(temp[2]) != self.pointB_id:
            print("Wasn't sent from the same ID")
        usleep(self.processing_delay)


        return int(temp[1]), temp[3]











            #plaintext = random_string().encode('utf-8')


