## 绘制物理拓扑结构图脚本使用说明

[TOC]

### 1、目录结构

`/DrawTopoStructure/`

> `cabinet.py` ：表箱类，存储表箱的相关数据
>
> `draw.py` ：绘制物理拓扑结构图
>
> `main.py` ：程序入口，负责解析json数据并调用 `draw.py` 中的函数完成物理拓扑结构图的绘制
>
> `node.py` ：开关节点类，存储开关节点的相关信息

**==四个py文件需在同一目录==**



### 2、运行脚本所需环境

Python版本：`Python 3.6+`

Python库：`matplotlib`

> ==*matplotlib库可能需要手动安装*==
>
> 在命令行输入下列命令安装 `matplotlib` 库
>
>
>  ~~~bash
> python -m pip install -U pip
> python -m pip install -U matplotlib
>  ~~~
>
> 验证 `matplotlib` 库是否安装
>
> ~~~bash
> pip show matplotlib
> ~~~
>
> 未安装
>
> <img src="README.assets/%E6%9C%AA%E5%AE%89%E8%A3%85matplotlib.png" alt="未安装matplotlib" style="zoom: 80%;" />
>
> 已安装
>
> <img src="README.assets/%E5%B7%B2%E5%AE%89%E8%A3%85matplotlib.png" alt="已安装matplotlib" style="zoom: 80%;" />



### 3、运行脚本命令

~~~bash
python main.py所在路径
~~~

例如 `main.py` 的路径为： `D:\Programing\Python\DrawTopoStructure\main.py`

![运行脚本](README.assets/%E8%BF%90%E8%A1%8C%E8%84%9A%E6%9C%AC.png)



### 4、输入

运行程序后按提示输入Json数据文件路径

例如Json文件路径为`D:\Programing\Python\DrawTopoStructure\data\attenuating_result_2021_01_25_01_00_17.json`

![输入-1](README.assets/%E8%BE%93%E5%85%A5-1.png)

![输入-2](README.assets/%E8%BE%93%E5%85%A5-2.png)

若路径输入错误会提示未找到指定文件

![未找到文件](README.assets/%E6%9C%AA%E6%89%BE%E5%88%B0%E6%96%87%E4%BB%B6.png)



### 5、运行界面

<img src="README.assets/%E8%BF%90%E8%A1%8C%E7%95%8C%E9%9D%A2.png" alt="运行界面" style="zoom: 80%;" />

#### 5.1、按钮功能

界面左下角有功能按钮

![按钮功能](README.assets/%E6%8C%89%E9%92%AE%E5%8A%9F%E8%83%BD.png)

`按钮1` ：返回初始视图

`按钮2` ：返回上一视图

`按钮3` ：前往下一视图

`按钮4` ：拖动结构图

`按钮5` ：放大选中区域

`按钮6` ：设置图片与界面的间距

`按钮7` ：保存当前视图到直到位置



#### 5.2、物理拓扑结构图





<img src="README.assets/%E7%89%A9%E7%90%86%E6%8B%93%E6%89%91%E7%BB%93%E6%9E%84%E5%9B%BE.png" alt="物理拓扑结构图" style="zoom:80%;" />

1、蓝色节点表示一个开关节点，鼠标放到节点上方显示该开关节点的详细信息（若信息详细信息显示越出边界，可以将节点向中心位置拖动后再查看详细信息）

2、虚线框表示一个表箱，框内左上角的红色标记为表箱的ID，同一层级的表箱在图中的水平高的相同

3、可以使用鼠标滚轮对结构图进行缩放

4、当结构图放大一定程度图中会显示开关节点的MAC信息（若MAC信息在图中重叠，可以使用滚轮放大结构图）

5、表箱与表箱之间的连线上会标有距离（如`100m`），若数据中的距离为0则不会标记