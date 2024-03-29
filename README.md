## FT_marblue

用傅里叶变换画老大(x

渲染出来的gif比较大，不一定能直接加载出来，可以直接点击`marblue.gif`查看

![](./assets/marblue.gif)



### 参考资料

1. [_手把手教你用傅立叶变换画可达鸭_](https://zhuanlan.zhihu.com/p/72632360)
2. [_matplotlib：先搞明白plt. /ax./ fig再画_](https://zhuanlan.zhihu.com/p/93423829)
3. [_Matplotlib_](https://www.matplotlib.org.cn/)
4. [_Python+Matplotlib制作动画_](https://www.cnblogs.com/endlesscoding/p/10308111.html)
5. [_Delaunay剖分_](http://www.geom.uiuc.edu/~samuelp/del_project.html)
6. [_Ramer–Douglas–Peucker_](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm)



### 正文

~~知乎的那篇看得我头皮发麻~~

虽然大部分内容都有提到，但实现的细节讲的不完全

另外，代码是Jupyter的风格，看着不是很习惯，于是重构了一下代码，写了几个类

画图时间比较长（10710U-16G），800+点傅里叶变换画图需要10min左右，200+大概2min

| Class            | 功能                            |
| ---------------- | ------------------------------- |
| ContourExtract   | 根据阈值提取转化成灰度后的图像  |
| MSTGenerator     | 在Delaunay剖分的基础上生成MST   |
| PathGenerator    | 在MST的基础上生成并优化遍历路径 |
| FourierTransPlot | 将路径傅里叶变换后画图          |

| Other    |                                     |
| -------- | ----------------------------------- |
| contour2 | 使用matplotlib的contour进行轮廓提取 |
| main     | 主函数                              |



#### 1.轮廓提取

- [ ] CNN

~~使用了naive的方法~~

先把图片转化为灰度，然后根据给定阈值来判断黑色轮廓，并在收集完轮廓后进行采样

![](./assets/stage1.png)



#### 2.MST生成

Delaunay剖分：[Link](http://www.geom.uiuc.edu/~samuelp/del_project.html)

​	所有在Delaunay剖分里的三角形外接圆不含其它点，存在且唯一

MST性质：每个环上的最长边必定不在MST上

MST是Delaunay剖分的子图：

​	如果(u,v)不在Delaunay剖分，则(u,v)外接圆内含有其它点，不妨w，从而(u,v)为u-v-w里的最长边

在Delaunay剖分的基础上使用$Kruskal$即可

![](./assets/stage2.png)



#### 3.生成遍历路径

dfs一遍最小生成树，生成的dfs序即为遍历路径，注意叶子节点只需进一次

考虑到最后一次回溯其实没有必要，因此选择树的直径来dfs以减少最后一次最长的回溯

树的直径直接dp即可，求得直径后，根据连通性重新排序邻接表使得末端最后被访问



#### 4.优化遍历路径

应用Ramer–Douglas–Peucker算法

The following is By Mysid from wikipedia.

![](./assets/Douglas-Peucker_animated.gif)

首先给定精度$\varepsilon$，选取首尾点做直线$\ell$，在此基础上寻找Hausdorff距离最远的点

- 若点到$\ell$距离小于$\varepsilon$，则其余点也满足，不继续处理
- 若点到$\ell$距离大于$\varepsilon$，则该点必须选取，分治递归处理

![](./assets/stage4.png)



#### 5.Fourier变换画图

- [ ] 去掉模长较小的分量

离散Fourier变换
$$
X_k = \sum_{n=0}^{N-1} x_n\cdot e^{-\frac {i 2\pi}{N}kn} = \sum_{n=0}^{N-1} x_n\cdot [\cos(2 \pi k n / N) - i\cdot \sin(2 \pi k n / N)]
$$

$$
x_n = \frac{1}{N} \sum_{k=0}^{N-1} X_k\cdot e^{i 2 \pi k n / N}
$$

以$n=8$为例
$$
x_1 = \frac{1}{8}(X_0\cdot e^{0} + X_1\cdot e^{i2\pi/8} + X_2\cdot e^{{i4\pi/8}} + X_3\cdot e^{{i6\pi/8}} + X_4\cdot e^{{i8\pi/8}} + X_5\cdot e^{i10\pi/8} + X_6\cdot e^{i12\pi/8} + X_7\cdot e^{i14\pi/8})
$$
相当于让 $X_0$ 不动，在此基础上$X_1$逆时针转45度，以此类推。另外，圆的半径就是$\frac{|X_i|}{N}$

这些圆如果首尾相接，第二个圆心定在第一个圆的向量末端……，那么最后一个圆的向量指向的位置就是所有向量的和，即为$x_i$

使用`matplotlib`里的`FuncAnimation`，进行绘制。先预处理出每个圆心在每一帧的位置，然后在帧之间重新渲染圆心和圆之间的连线并加入新的点。
