import math
import numpy as np


def object():
    def general(n):
        x, y = n
        return pow(x - 1, 2) + pow(y - 1, 2)


    def rosenbroke(x, y):
        return (x - 1) * (x - 1) + 100 * pow((y - pow(x, 2)), 2)


    def csdn(n):
        x, y = n
        return 3 * (1 - x) ** 2 * np.exp(-(x ** 2) - (y + 1) ** 2) - 10 * (x / 5 - x ** 3 - y ** 5) * np.exp(
            -x ** 2 - y ** 2) - 1 / 3 ** np.exp(-(x + 1) ** 2 - y ** 2)

    return rosenbroke

class myModel:
    def __init__(self, gene):
        self.num = len(gene)
        self.gene = gene
        self.fitness = object()(*gene)
