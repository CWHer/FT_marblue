# generate path from MST
#   usually after MST.generate()
#   traverse all points on MST
#    and exclude the longest path
#   optimize path using rdp algorithm
# input: list of points and an adjacency list of MST
# output: traverse path of MST
#           nx2 np.array

import numpy as np
import math
import matplotlib.pyplot as plt


class PathGenerator():
    def __init__(self, points: np.array, g: list):
        self.points = points
        self.g = g
        self.path = []
        import sys
        sys.setrecursionlimit(1024 * 1024)

    def findDiameter(self):
        # f[x][0] max distance from x to leaf
        #   with root = 0
        # f[x][1] leaf node satisfies f[x][0]
        f = [[0, i] for i in range(len(self.g))]
        vis = set()
        self.max_len = 0

        def dfs(x: int):
            vis.add(x)
            # longest and 2nd longest
            max_f, nxt_f = [0, 0], [0, 0]
            for nxt in self.g[x]:
                if nxt in vis: continue
                dfs(nxt)
                if f[nxt][0] + 1 > f[x][0]:
                    f[x][0], f[x][1] = f[nxt][0] + 1, f[nxt][1]
                if f[nxt][0] > max_f[0]:
                    max_f, nxt_f = f[nxt], max_f
                elif f[nxt][0] > nxt_f[0]:
                    nxt_f = f[nxt]
            if max_f[0] + nxt_f[0] > self.max_len:
                self.max_len = max_f[0] + nxt_f[0]
                self.s, self.t = max_f[1], nxt_f[1]

        dfs(0)
        print(
            "diameter starts with {} and ends with {}, with length {}".format(
                self.s, self.t, self.max_len))

    # make dfs access close nodes first
    def reorderGraph(self):
        vis = set()

        def dfs(x: int) -> bool:
            vis.add(x)
            if x == self.t:
                return True
            for nxt in self.g[x]:
                if nxt in vis: continue
                if dfs(nxt):
                    # visit "end point" later
                    self.g[x].remove(nxt)
                    self.g[x].append(nxt)
                    return True
            return False

        dfs(self.s)

    # distance between point and line
    # input: point(x,y), start(x,y) and end(x,y)
    def __pldist(self, point, start, end):
        # start == end
        #  np.all applies function to every element
        if np.all(np.equal(start, end)):
            return np.linalg.norm(point - start)

        return np.divide(
            np.abs(np.linalg.norm(np.cross(end - start, start - point))),
            np.linalg.norm(end - start))

    # Ramer–Douglas–Peucker algorithm
    def rdp_downsample(self, l: int, r: int, epsilon: float):
        max_d, idx = 0, 0
        for i in range(l + 1, r):
            d = self.__pldist(self.path[i, :], self.path[l, :],
                              self.path[r, :])
            if d > max_d:
                max_d = d
                idx = i

        if max_d > epsilon:
            path = []
            path.extend(self.rdp_downsample(l, idx, epsilon))
            path.pop()  # remove redundant index
            path.extend(self.rdp_downsample(idx, r, epsilon))
            return path
        else:
            return [self.path[l], self.path[r]]

    def show(self):
        _, ax = plt.subplots()
        ax.scatter(self.path[:, 0], self.path[:, 1], alpha=0.3)
        for i in range(len(self.path) - 1):
            ax.plot((self.path[i, 0], self.path[i + 1, 0]),
                    (self.path[i, 1], self.path[i + 1, 1]))
        plt.show()

    def generatePath(self) -> np.array:
        # remove diameter in the tree
        self.findDiameter()
        self.reorderGraph()

        vis = set()

        # raise when comes to end
        class FinishTraverse(Exception):
            pass

        def dfs(x):
            vis.add(x)
            self.path.append(self.points[x])

            if x == self.t:
                raise FinishTraverse()

            is_leaf = True
            for nxt in self.g[x]:
                if not nxt in vis:
                    dfs(nxt)
                    is_leaf = False
            if not is_leaf:
                self.path.append(self.points[x])

        try:
            dfs(self.s)
        except FinishTraverse:
            # check if all points are passed by
            # print(len(vis))
            assert len(vis) == len(self.g)

        self.path = np.array(self.path)
        print("generate path with {} points".format(len(self.path)))

        # apply Ramer–Douglas–Peucker algorithm
        self.path = self.rdp_downsample(0, len(self.path) - 1, 8)
        print("{} points after rdp_downsample".format(len(self.path)))

        self.path.append(self.points[self.s])
        self.path = np.array(self.path)
        return self.path
