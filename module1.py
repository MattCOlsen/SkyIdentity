import ChaCha20
import RSA
import random
from time import process_time as time
import Communication_Module
import numpy as np


def test_ChaCha20(size, interval, transmission_delay=None, processing_delay=None):
    times = [[0, 0]]
    for i in range(interval, size + interval, interval):
        test = Communication_Module.RadioModule(transmission_delay, processing_delay)
        test.create_ChaCha20_Packages_and_keys(i)

        tic = time()
        test.decrypt_ChaCha20_packages()
        toc = time()
    
    
        times.append([i, (toc-tic)/i])

    with open('ChaCha20.txt', 'w') as filehandle:
        for listitem in times:
            filehandle.write('%s\n' % listitem)



    return times
    
def test_RSA(size, interval, transmission_delay=None, processing_delay=None):
    times = [[0, 0]]
    for i in range(interval, size + interval, interval):

        Drone_Keys = RSA.create_keypairs(i)

        Base_Keys = RSA.create_keypairs(1)

        Drone_Public_Keys = [i[1] for i in Drone_Keys]
        Base_Public_Keys = [i[1] for i in Base_Keys]

        #Create the Base Module
        chosen_base = Base_Keys[0]

        Base_Module = Communication_Module.RadioModule(id=0, publickeylist=Drone_Public_Keys, private_key=chosen_base[0])

        Drone_List = []
        for j in range(i):
            keys = Drone_Keys[j]
            Drone = Communication_Module.RadioModule(id=j, publickeylist=Base_Public_Keys, private_key=keys[0])
            Drone_List.append(Drone)


        random.shuffle(Drone_List)


        tic = time()

        for j in Drone_List:
            Base_Module.RSA_challenge(j)

        toc = time()
    
    
        times.append([i, (toc-tic)/i])

    with open('RSA.txt', 'w') as filehandle:
        for listitem in times:
            filehandle.write('%s\n' % listitem)

    return times