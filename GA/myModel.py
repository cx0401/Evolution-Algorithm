import math
import numpy as np

def general(x):
    return pow(x[0] - 1, 2) + pow(x[1] - 1, 2)


def rosenbroke(n):
    x, y = n
    return float(x - 1) * (x - 1) + 100 * math.pow((y - pow(x, 2)), 2)


def csdn(n):
    x, y = n
    return 3 * (1 - x) ** 2 * np.exp(-(x ** 2) - (y + 1) ** 2) - 10 * (x / 5 - x ** 3 - y ** 5) * np.exp(
        -x ** 2 - y ** 2) - 1 / 3 ** np.exp(-(x + 1) ** 2 - y ** 2)

class myModel:
    def __init__(self, gene):
        self.num = len(gene)
        self.gene = gene
        self.fitness = rosenbroke(gene)