# generate MST of selected points
#   usually after contour.extractImage()
#   using Delaunay triangulation and Kruskal
# input: nx2 np.array of points
# output: an adjacency list of MST

from scipy.spatial import Delaunay
import numpy as np
import math
import matplotlib.pyplot as plt


class MSTGenerator():
    def __init__(self, points: np.array):
        self.points = points
        # triangles
        self.tris = Delaunay(self.points).simplices

    # points[x] and points[y]
    def __dist2(self, x: int, y: int):
        return math.sqrt((self.points[x, 0] - self.points[y, 0])**2 +
                         (self.points[x, 1] - self.points[y, 1])**2)

    def show(self):
        self.__plotTris()
        self.__plotMST()
        plt.show()

    # show triangulation
    def __plotTris(self):
        plt.subplot(1, 2, 1)
        plt.triplot(self.points[:, 0], self.points[:, 1], self.tris)

    def __plotMST(self):
        plt.subplot(1, 2, 2)
        for u in range(len(self.g)):
            for v in self.g[u]:
                plt.plot((self.points[u, 0], self.points[v, 0]),
                         (self.points[u, 1], self.points[v, 1]))

    # return an adjacency list of MST
    def generateMST(self):
        n = len(self.points)
        self.g = [[] for i in range(n)]
        edges = set()
        for tri in self.tris:
            for i in range(3):
                u, v = tri[i - 1], tri[i]
                edges |= {(u, v) if u < v else (v, u)}
        edges = list(edges)
        edges.sort(key=lambda e: self.__dist2(e[0], e[1]))
        # union and find sets
        fa = list(range(n))

        def find(x: int) -> int:
            if fa[x] == x:
                return x
            fa[x] = find(fa[x])
            return fa[x]

        def union(x: int, y: int):
            fa[find(x)] = find(y)

        for edge in edges:
            u, v = edge
            if find(u) == find(v): continue
            self.g[u].append(v)
            self.g[v].append(u)
            union(u, v)

        print("finish generate MST")
