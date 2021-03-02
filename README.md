## FT_marblue

用傅里叶变换画老大(x



### 参考资料

1. [_手把手教你用傅立叶变换画可达鸭_](https://zhuanlan.zhihu.com/p/72632360)

2. [_matplotlib：先搞明白plt. /ax./ fig再画_](https://zhuanlan.zhihu.com/p/93423829)

3. [_Matplotlib_](https://www.matplotlib.org.cn/)

4. [_Python+Matplotlib制作动画_](https://www.cnblogs.com/endlesscoding/p/10308111.html)

5. [_Delaunay剖分_](http://www.geom.uiuc.edu/~samuelp/del_project.html)



### 正文

~~知乎的那篇看得我头皮发麻~~

于是重构了一下代码

#### 1.轮廓提取

- [ ] CNN

~~使用了naive的方法~~

先把图片转化为灰度，然后根据给定阈值来判断黑色轮廓，并在收集完轮廓后进行采样



#### 2.MST生成

Delaunay剖分：[Link](http://www.geom.uiuc.edu/~samuelp/del_project.html)

​	所有在Delaunay剖分里的三角形外接圆不含其它点，存在且唯一

MST性质：每个环上的最长边必定不在MST上

MST是Delaunay剖分的子图：

​	如果(u,v)不在Delaunay剖分，则(u,v)外接圆内含有其它点，不妨w，从而(u,v)为u-v-w里的最长边

在Delaunay剖分的基础上使用$Kruskal$即可



#### 3.生成遍历路径

dfs一遍最小生成树，生成的dfs序即为遍历路径，注意叶子节点只需进一次

考虑到最后一次回溯其实没有必要，因此选择树的直径来dfs以减少最后一次最长的回溯

树的直径直接dp即可，求得直径后，根据连通性重新排序邻接表使得末端最后被访问



#### 4.优化遍历路径



#### 5.Fourier变换画图

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

