# generate path from MST
#   usually after MST.generate()
#   traverse all points on MST
#    and exclude the longest path
# input: list of points and an adjacency list of MST
# output: traverse path of MST
#           nx2 np.array

import numpy as np
import math


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
            # longest and 2nd longest
            for nxt in self.g[x]:
                if nxt in vis: continue
                if dfs(nxt):
                    # visit "end point" later
                    self.g[x].remove(nxt)
                    self.g[x].append(nxt)
                    return True
            return False

        dfs(self.s)

    def generatePath(self) -> np.array:
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
            self.path.append(self.points[self.s])
        # check if all points are passed by
        # print(len(vis))
        assert len(vis) == len(self.g)

        self.path = np.array(self.path)
        print("generate path with {} points".format(len(self.path)))

        return self.path
