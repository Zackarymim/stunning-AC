from matplotlib.image import imread
import numpy as np
from decimal import Decimal,getcontext

getcontext().prec=100

class ArithmeticCoder():
    def __init__(self,block):
        self.block = block
        self.occurs = {}

    def get_freqs(self):
        return self.occurs
    
    def make_proba_table(self):

        total = self.block.size

        for i in range(256):
            self.occurs[i] = Decimal(int((self.block == i).sum()))
        
        for key,value in self.occurs.items():
            self.occurs[key] = Decimal(int(value)) / Decimal(total)

        res = [Decimal(0)]
        L = list(self.occurs.values())
        for i in range(len(L)):
            som = 0
            for j in range(i+1):
                som = som + L[j]
            
            res.append(som)
    
        return res

    def encode(self):
        sequence = self.block.flatten()
        probs = self.make_proba_table()

        Dictionary = self.occurs
        Probas = list(self.occurs.values())
        for i in range(len(sequence)):
            ind = list(Dictionary.keys()).index(sequence[i])
            probs = probs[ind:ind+2]

            for j in range(len(Dictionary)-1):
                upper = probs[-1]
                lower = probs[0]
                lower2 = probs[j]
                resultat = (upper - lower) * Probas[j] + lower2
                probs.insert(j+1,resultat)
        return (probs[0] + probs[-1]) / 2
    

class ArithmeticDecoder():
    def __init__(self):
        pass
    
    def make_proba_table(self,L):
        res = [0]
        for i in range(len(L)):
            som = 0
            for j in range(i+1):
                som = som + L[j]
            
            res.append(som)
    
        return res

    def decode(self,fraction,size,freqs):
        block = []
        Dictionary = freqs
        probs = self.make_proba_table(list(freqs.values()))
        Probas = list(freqs.values())
        for _ in range(size*size):
            ind = 0
            for k in range(len(probs)-1):
                if fraction >= probs[k] and fraction <= probs[k+1]: 
                    ind = k
            block.append(list(Dictionary.keys())[ind])
            probs = probs[ind:ind+2]

            for j in range(len(list(Dictionary.keys()))-1):
                upper = probs[-1]
                lower = probs[0]
                lower2 = probs[j]
                resultat = (upper - lower) * Probas[j] + lower2
                probs.insert(j+1,resultat)
        return block


        