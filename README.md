## FT_marblue

用傅里叶变换画老大(x



### 参考资料

[_手把手教你用傅立叶变换画可达鸭_](https://zhuanlan.zhihu.com/p/72632360)



### 正文

~~知乎的那篇看得我头皮发麻~~

于是重构了一下代码

#### 1.轮廓提取

- [ ] todo

#### 2.MST生成

Delaunay剖分：[Link](http://www.geom.uiuc.edu/~samuelp/del_project.html)

​	所有在Delaunay剖分里的三角形外接圆不含其它点，存在且唯一

MST性质：每个环上的最长边必定不在MST上

MST是Delaunay剖分的子图：

​	如果(u,v)不在Delaunay剖分，则(u,v)外接圆内含有其它点，不妨w，从而(u,v)为u-v-w里的最长边





#### 5.Fourier变换画图