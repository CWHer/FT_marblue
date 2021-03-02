#%%
import numpy as np

from contour import ContourExtract
from ftplot import FourierTransPlot
from mst import MSTGenerator
from path import PathGenerator

extractor = ContourExtract("edge.png")
points = extractor.extractImage()
extractor.show()

mst = MSTGenerator(points)
g = mst.generateMST()
# show triangles
# mst.show(show_tri=False)

path = PathGenerator(points, g)
x = path.generatePath()
path.show()

Ploter = FourierTransPlot(x)
# show or save_gif
Ploter.plot(save_gif=True)
# %%
