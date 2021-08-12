import time
from typing import List
import random
import numpy as np
import myModel
import plot


class SearchStrategy(object):
    def __init__(self):
        self.mutateFactor = 0.5
        self.tournament = 0.5
        self.popNum = 200
        self.variableNum = 2
        self.lower = -3
        self.upper = 3
        self.select = 0.8
        self.factor1 = 0.8
        self.factor2 = 0.5
        self.pop = [myModel.myModel([random.random() * (self.upper - self.lower) + self.lower
                                     for i in range(self.variableNum)]) for j in range(self.popNum)]
        self.best = self.pop[np.argsort([self.pop[i].fitness for i in range(self.popNum)])[0]]

    def generate_tasks(self):
        for i in range(self.popNum):
            indiviual = []
            for k in range(self.variableNum):
                m = self.pop[i].gene[k]
                if random.random() < self.mutateFactor:
                    m += self.factor1 * (self.pop[random.randint(0, self.popNum - 1)].gene[k] -
                                         self.pop[random.randint(0, self.popNum - 1)].gene[k])
                    # m += self.factor2 * (self.best.gene[k] - m)
                    m = self.upper if m > self.upper else m
                    m = self.lower if m < self.lower else m
                indiviual.append(m)
            self.pop.append(myModel.myModel(indiviual))
        return self.pop

    def handle_rewards(self, score: List[float]) -> None:
        index = []

        # tournament algorithm
        n = 2
        randPop = np.random.choice(len(score), len(score), replace=False)
        red = randPop[:self.popNum]
        bule = randPop[self.popNum:]
        index = [red[i] if score[red[i]] < score[bule[i]] else bule[i] for i in range(self.popNum)]

        self.pop = [self.pop[i] for i in index]
        self.best = self.pop[np.argsort([self.pop[i].fitness for i in range(self.popNum)])[0]]
        return None


if __name__ == '__main__':
    Pop = SearchStrategy()
    epochs = 100
    p = plot.plot(myModel.object(), Pop.lower, Pop.upper, 200)

    for i in range(epochs):
        random.seed(time.time())
        Pop.generate_tasks()
        Pop.handle_rewards([i.fitness for i in Pop.pop])
        p.point(np.array([j.gene[0] for j in Pop.pop]), np.array([j.gene[1] for j in Pop.pop]))
        print(Pop.best.gene, Pop.best.fitness)
