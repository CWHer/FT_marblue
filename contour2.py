# using pyplot.contour
#%%
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = Image.open('edge.png').convert('L')
img = img.resize((1000, 1000), Image.ANTIALIAS)
img = img.convert('L')
fig, ax = plt.subplots()
fig.set_size_inches(10, 10)
ax.set(xlim=[0, 1000], ylim=[0, 1000])
ax.axis("off")
contours = ax.contour(img, origin='image', levels=[100])
# plt.savefig("edge.jpg")
plt.show()
# %%
