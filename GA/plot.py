import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


class plot(object):
    def __init__(self, f, *arg) -> None:
        self.X = numpy.linspace(arg[0], arg[1], arg[2])
        self.Y = numpy.linspace(arg[0], arg[1], arg[2])
        self.F = f
        fig = plt.figure()
        self.ax = Axes3D(fig)
        plt.ion()  # 将画图模式改为交互模式，程序遇到plt.show不会暂停，而是继续执行
        ax = self.ax
        self.X, self.Y = numpy.meshgrid(self.X, self.Y)
        Z = self.F(self.X, self.Y)
        ax.plot_surface(self.X, self.Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm)
        ax.set_zlim(0, Z.max())
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.pause(0.1)
        plt.show()

    def point(self, x, y):
        sca = self.ax.scatter(x, y, self.F(x, y), c='black', marker='o');
        plt.show();
        plt.pause(0.01)
        sca.remove()
