#!/bin/python3
import numpy as np
import random

class QSystem:
    """
    i_*: Physically impossible operations
    """
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.prob = np.ones(2 ** num_bits)
        self.prob /= self.prob.size
    
    def observe(self, ix_qb):
        value = False if (self.i_prob(ix_qb) <= random.random()) else True

        mask = 1 << ix_qb
        for (st, p) in enumerate(self.prob):
            if ((st & mask) != 0) != value:
                self.prob[st] = 0
        self.prob /= np.sum(self.prob)

        return value
    
    def i_prob(self, ix_qb):
        mask = 1 << ix_qb
        p_1 = 0
        p_0 = 0
        for (st, p) in enumerate(self.prob):
            if st & mask != 0:
                p_1 += p
            else:
                p_0 += p
        # p_0 + p_1 == 1
        return p_1
    
    def reset_nand(self, a, b, result):
        """
        Destroy result state
        and result = !(a & b)
        """
        for (st, p) in enumerate(self.prob):
            va = (st & (1 << a)) != 0
            vb = (st & (1 << b)) != 0
            vres = (st & (1 << result)) != 0
            vres_expected = not (va and vb)
            print(st, vres, vres_expected)
            if vres != vres_expected:
                self.prob[st] = 0
        self.prob /= np.sum(self.prob)
    
    def reset_qbit(self, ix_qb, prob):
        """
        Destroy current ix_qb and
        set new independent superposition
        0 (prob-1) + 1 (prob)
        """
        mask = 1 << ix_qb
        for (st, p) in enumerate(self.prob):
            if st & mask != 0:
                # Un-entangle
                p_marginalized = self.prob[st & ~mask] + self.prob[st]

                self.prob[st] = p_marginalized * prob
                self.prob[st & ~mask] = p_marginalized * (1 - prob)
    
    def i_print_pretty(self):
        for (st, p) in enumerate(self.prob):
            print("%s|%.5f" % (bin(st), p))



def main():
    qs = QSystem(4)
    qs.reset_nand(0, 1, 2)
    qs.reset_nand(0, 2, 3)
    print(qs.observe(2))
    print(qs.i_prob(3))
    

main()