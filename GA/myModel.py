import math
import numpy as np


def object():
    def general(x, y):
        return pow(x - 1, 2) + pow(y - 1, 2)

    def rosenbroke(x, y):
        return (x - 1) * (x - 1) + 100 * pow((y - pow(x, 2)), 2)

    def csdn(x, y):
        return 3 * (1 - x) ** 2 * np.exp(-(x ** 2) - (y + 1) ** 2) - 10 * (x / 5 - x ** 3 - y ** 5) * np.exp(
            -x ** 2 - y ** 2) - 1 / 3 ** np.exp(-(x + 1) ** 2 - y ** 2)

    return csdn


class myModel:
    def __init__(self, gene):
        trainNum = 1
        self.num = len(gene)
        self.gene = gene
        self.steps = [(i + 1) * trainNum for i in range(100)]
        self.step = 0
        self.fitness = 0
        for i in range(trainNum):
            self.fitness = -object()(*gene)

    def compute_score(self, hurdles):
        while self.step < len(hurdles):
            for j in range(self.steps[self.step]):
                self.fitness = -object()(*self.gene)
            if self.fitness < hurdles[self.step]:
                self.step += 1
            else:
                return False
        return True
