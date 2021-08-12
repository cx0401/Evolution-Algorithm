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
        self.newPop = []
        self.hurdles = []
        self.hurdles.append(sum([i.fitness for i in self.pop]) / self.popNum)
        self.best = self.pop[np.argsort([self.pop[i].fitness for i in range(self.popNum)])[0]]

    # produce the child pop
    def generate_tasks(self):
        newPop = []
        for i in range(self.popNum):
            indiviual = []

            # mutate
            for k in range(self.variableNum):
                m = self.pop[i].gene[k]
                if random.random() < self.mutateFactor:
                    m += self.factor1 * (self.pop[random.randint(0, self.popNum - 1)].gene[k] -
                                         self.pop[random.randint(0, self.popNum - 1)].gene[k])
                    # m += self.factor2 * (self.best.gene[k] - m)
                    m = self.upper if m > self.upper else m
                    m = self.lower if m < self.lower else m
                indiviual.append(m)

            model = myModel.myModel(indiviual)
            newPop.append(model)
        self.newPop = newPop
        return newPop

    # compute the score and use hurdle to pass the bad child
    def method_hurdle(self):
        for i in self.newPop:
            if not i.compute_score(self.hurdles):
                del i
        score = [i.fitness for i in self.newPop]
        return score

    # par and child together to select and add the hurdle
    def handle_rewards(self, score: List[float]) -> None:
        score = [i.fitness for i in self.pop] + score
        pop = self.pop + self.newPop

        # tournament algorithm
        n = 2
        randPop = np.random.choice(len(score), len(score), replace=False)
        red = randPop[:len(score) // 2]
        blue = randPop[len(score) // 2:]
        index = [red[i] if score[red[i]] < score[blue[i]] else blue[i] for i in range(len(score) // 2)]

        self.pop = [pop[i] for i in index]
        self.popNum = len(self.pop)
        self.hurdles.append(sum([i.fitness for i in self.pop]) / self.popNum)
        self.best = self.pop[np.argsort([i.fitness for i in self.pop])[0]]
        return None


if __name__ == '__main__':
    Pop = SearchStrategy()
    epochs = 50
    # initial the picture
    p = plot.plot(myModel.object(), Pop.lower, Pop.upper, 200)
    random.seed(time.time())
    for i in range(epochs):
        # mutate
        Pop.generate_tasks()

        # select
        Pop.handle_rewards(Pop.method_hurdle())

        # draw the 3D picture
        p.point(np.array([j.gene[0] for j in Pop.pop]), np.array([j.gene[1] for j in Pop.pop]))

        print(Pop.best.gene, Pop.best.fitness)
