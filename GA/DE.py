import copy
import math
import time
from typing import List
import random
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


class SearchStrategy(object):
    def __init__(self):
        self.mutateFactor = 0.8
        self.tournament = 0.5
        self.popNum = 200
        self.variableNum = 2
        self.pop = []
        self.newPop = []
        self.fitness = []
        self.lower = -10
        self.upper = 10
        self.select = 0.8
        self.factor = 0.8
        self.pop = [[random.random() * (self.upper - self.lower) + self.lower
                     for i in range(self.variableNum)] for j in range(self.popNum)]

    def generate_tasks(self):
        self.newPop = []
        for i in range(self.popNum):
            self.newPop.append([])
            for k in range(self.variableNum):
                m = self.pop[i][k]
                if random.random() < self.mutateFactor:
                    m += self.factor * (self.pop[random.randint(0, self.popNum - 1)][k] -
                                        self.pop[random.randint(0, self.popNum - 1)][k])
                    m = self.upper if m > self.upper else m
                    m = self.lower if m < self.lower else m
                self.newPop[i].append(m)
        return self.newPop

    def compute_score(self, array) -> List[float]:
        return [general(i) for i in array]

    def handle_rewards(self, score: List[float]) -> None:
        # roulette&tournament algorithm
        newPop = self.pop + self.newPop
        score = self.compute_score(newPop)
        index = []

        # roulette algorithm
        def roulette():
            pro = [max(score) - i + 1e-3 for i in score]
            pro = [i / sum(pro) for i in pro]
            index = np.random.choice(len(pro), size=self.popNum, replace=True, p=pro)
            return index

        # roulette & tournament algorithm
        def rou_tour():
            score_sort = np.argsort(score)
            for i in range(self.popNum):
                j = 0
                while random.random() > self.select and j < len(newPop):
                    j += 1
                index.append(score_sort[j])
            return index

        # tournament algorithm
        def tournament():
            n = 2
            index = []
            for i in range(self.popNum):
                players = [random.randint(0, len(score) - 1) for j in range(n)]
                player_score = [score[j] for j in players]
                index.append(players[np.argsort(player_score)[0]])
            return index

        # select the n max
        def kMax():
            return np.argsort(score)[:self.popNum]

        self.pop = [newPop[i] for i in tournament()]
        return None


if __name__ == '__main__':
    a = SearchStrategy()
    epochs = 1000
    for i in range(epochs):
        random.seed(time.time())
        a.generate_tasks()
        a.handle_rewards([])
        if i % 10 == 0:
            print(a.pop, a.compute_score(a.pop), "\n")
