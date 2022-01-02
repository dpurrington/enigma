#!/usr/bin/env python
import random
import pickle
import logging

CHARSET_SIZE = 26

def index_as_chr(i):
    return chr(i + 65)
def chr_as_index(c):
    return ord(c - 65)

class Rotor:
    def __init__(self, position = 0, ring_position = 0):
        assert position >= 0, "Position must be greater than or equal to 0"
        assert position <= CHARSET_SIZE - 1, f"Position must be  less than or equal to {CHARSET_SIZE}"
        assert ring_position >= 0, "Ring position must be greater than or equal to 0"
        assert ring_position <= CHARSET_SIZE - 1, f"Ring position must be  less than or equal to {CHARSET_SIZE}"
        # forward pathway
        self.forward_data = [*range(0,CHARSET_SIZE)]
        self.position = position
        self.ring_position = ring_position
        random.shuffle(self.forward_data)

        #ensure every position maps to another
        for i in range(0, CHARSET_SIZE):
            val = self.forward_data[i]
            if val == i:
                # is this the last position?
                if i == CHARSET_SIZE - 1:
                    #swap current value with the prior one
                    self.forward_data[i] = self.forward_data[i-1]
                    self.forward_data[i-1] = val
                else:
                    #swap current value with the next one
                    self.forward_data[i] = self.forward_data[i+1]
                    self.forward_data[i+1] = val
                    

        # the reverse pathway
        self.backward_data = [None] * CHARSET_SIZE 
        for index, data in enumerate(self.forward_data):
            self.backward_data[data] = index
        
    def set_ring(self, r):
        assert 0 <= r < CHARSET_SIZE, "Ring setting out of range"
        self.ring_position = r

    def set_position(self, p):
        assert 0 <= p < CHARSET_SIZE, "Position setting out of range"
        self.position = p

    def rotate(self):
        retval = self.position == self.ring_position
        if self.position >= CHARSET_SIZE - 1:
            self.position = 0
        else:
            self.position = self.position + 1
        return retval

    def __repr__(self):
        return self.__str__()
    
    def __str__(self) -> str:
        return self.forward_data.__str__()
    
    def forward(self, ordinal):
        assert 0 <= ordinal < CHARSET_SIZE, "ordinal value not in range"
        return self.forward_data[ordinal]

    def backward(self, ordinal):
        assert 0 <= ordinal < CHARSET_SIZE, "ordinal value not in range"
        return self.backward_data[ordinal] 

class Reflector:
    def __init__(self):
        right = [*range(0,CHARSET_SIZE//2)]
        left = [None] * (CHARSET_SIZE//2)
        random.shuffle(right)
        for i, val in enumerate(right):
            left[val] = i + CHARSET_SIZE//2
        self.data = left + right

    def get_key(self, k):
        return(self.data[k])

class RotorHouse:
    def __init__(self, reflector, rotors):
        self.reflector = reflector
        self.rotors = rotors

    def turn_rotors(self):
        if (self.rotors[0].rotate()):
            if(self.rotors[1].rotate()):
                self.rotors[2].rotate()
        
    def translate(self, key):
        self.turn_rotors()
        retval = key
        transforms = []
        transforms.append(f"{index_as_chr(retval)}")
        for r in self.rotors:
            retval = r.forward(retval)
            transforms.append(f"-> {index_as_chr(retval)}")

        retval = self.reflector.get_key(retval)
        transforms.append(f"-> {index_as_chr(retval)}")
        for r in self.rotors[::-1]:
            retval = r.backward(retval)
            transforms.append(f"-> {index_as_chr(retval)}")
        logging.debug(' '.join(transforms))
        return retval

class PlugBoard:
    def __init__(self):
        self.pairs = [None] * 26
    
    def add_pair(self, pair):
        (a, b) = pair
        assert a != b, "Pairs must be of different values"
        assert self.pairs[a] is None, "Duplicate pair"
        assert self.pairs[b] is None, "Duplicate pair"

        self.pairs[a] = b
        self.pairs[b] = a

    def get_key(self, k):
        if self.pairs[k] is None:
            return k
        return self.pairs[k]

class EnigmaMachine:
    def __init__(self, reflector, rotors, pairs):
        self.rotor_house = RotorHouse(reflector, rotors)
        self.plug_board = PlugBoard()
        map(self.plug_board, pairs)
    
    def get_key(self, k):
        index = ord(k.upper()) - 65
        newindex = self.plug_board.get_key(self.rotor_house.translate(index))
        return chr(newindex + 65)

def generate_rotors():
    with open("rotors/reflector.bin", 'wb') as f:
        pickle.dump(Reflector(), f)
    for i in range(5):
        with open(f"rotors/rotor{i}.bin", 'wb') as f:
            pickle.dump(Rotor(), f)

def load_rotors():
    with open("rotors/reflector.bin", 'rb') as f:
        reflector = pickle.load(f)
    
    rotors = []
    for i in range(3):
        with open(f"rotors/rotor{i}.bin", 'rb') as f:
            rotors.append(pickle.load(f))

    return reflector, rotors
  
def do_run(message): 
    (reflector, rotors) = load_rotors()
    for r in rotors:
        r.set_ring(0)
        r.set_position(0)
    pairs = () 
    m = EnigmaMachine(reflector, rotors, pairs)
    new_message = []
    for c in message:
        new_message.append(m.get_key(c))
    return new_message

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    message = do_run("ABCDE")
    do_run(message)

if __name__ == '__main__':
    main()