import time
from typing import List
import random
import numpy as np
import myModel
import plot


class SearchStrategy(object):
    def __init__(self):
        self.mutateFactor = 0.8
        self.tournament = 0.5
        self.popNum = 200
        self.variableNum = 2
        self.newPop = []
        self.fitness = []
        self.lower = -3
        self.upper = 3
        self.select = 0.8
        self.factor = 0.8
        self.pop = [myModel.myModel([random.random() * (self.upper - self.lower) + self.lower
                                     for i in range(self.variableNum)]) for j in range(self.popNum)]
        self.best = self.pop[np.argsort([self.pop[i].fitness for i in range(self.popNum)])[0]]

    def generate_tasks(self):
        self.newPop = []
        for i in range(self.popNum):
            indiviual = []
            for k in range(self.variableNum):
                m = self.pop[i].gene[k]
                if random.random() < self.mutateFactor:
                    m += self.factor * (self.pop[random.randint(0, self.popNum - 1)].gene[k] -
                                        self.pop[random.randint(0, self.popNum - 1)].gene[k])
                    m = self.upper if m > self.upper else m
                    m = self.lower if m < self.lower else m
                indiviual.append(m)
            self.newPop.append(myModel.myModel(indiviual))
        return self.newPop

    def handle_rewards(self, score: List[float]) -> None:
        # roulette&tournament algorithm
        newPop = self.pop + self.newPop
        score = [i.fitness for i in newPop]
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
        self.best = self.pop[np.argsort([self.pop[i].fitness for i in range(self.popNum)])[0]]
        return None


if __name__ == '__main__':
    a = SearchStrategy()
    epochs = 200
    p = plot.plot(myModel.object(), a.lower, a.upper, 200)

    for i in range(epochs):
        random.seed(time.time())
        a.generate_tasks()
        a.handle_rewards([])
        p.point(np.array([j.gene[0] for j in a.pop]), np.array([j.gene[1] for j in a.pop]))
        print(a.best.gene, a.best.fitness)
