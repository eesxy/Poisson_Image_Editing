# Poisson_Image_Editing

泊松图像编辑

## 使用说明

### 预处理类

`Preprocessing`类: 选择泊松编辑所需的编辑区域与编辑位置

`select`方法: 同时选择编辑区域与编辑位置，对应`seamlessClone`中的`mask`和`point`参数

第一次弹出窗口为源图像复制区域的选择，通过按住鼠标左键拖动选择复制区域的边界(请确保选择一个封闭区域)，然后按下鼠标右键指定区域的内部。如果对所选区域不满意可用按下鼠标中键撤销选择。按下键盘任意键确定选择区域。

第二次弹出窗口为目标图像复制位置的选择，通过按住鼠标左键拖动来拖动源图像已选择区域到想要的位置。按下键盘任意键确定选择位置。

返回值为`mask, point`，也可通过访问成员变量来获取之前选出的参数

`selectArea`方法：仅选择编辑区域`mask`，适用于原地编辑方法

与`select`类似，只有第一次弹出窗口，只返回`mask`

### 核心类

`Poisson`类：实现泊松编辑的各种方法

`seamlessClone`方法：泊松编辑的基础方法

使用方法与opencv的`seamlessClone`大致相同，但`point`参数的顺序是相反的(opencv采用宽高坐标，这里实现时采用numpy的行列坐标)

`flag`参数可以指定为`NORMAL_CLONE`或`MIXED_CLONE`，效果与opencv对应的模式相同。`NORMAL_CLONE`为标准的泊松编辑，引导向量场采用源图像梯度场；`MIXED_CLONE`为混合模式，引导向量场采用源图像梯度场与目标图像梯度场各点对应方向较大值

`textureFlattening`方法：材质扁平化

参数形式与opencv相同，但参数的效果可能与opencv有所不同。采用canny边缘检测器作为判断依据，因此`low_thresh`和`high_thresh`参数分别对应canny边缘检测器的低阈值和高阈值

`illuminationChange`方法：亮度调整

参数形式与opencv相同，但参数的效果可能与opencv有所不同。对目标区域梯度场的作用如公式所示：

$$
\mathbf{v} = \alpha^\beta *\log(|\nabla f^*|^{-\beta})*\nabla f^*
$$

`colorChange`方法：色彩调整

参数形式与作用效果均与opencv相同。`red_mul`,`green_mul`,`blue_mul`参数代表三通道分别乘的比例

`deColor`方法：去色

此方法未在opencv中实现。效果为去除选中区域以外的区域的颜色，即保留ROI的色彩并使背景变为黑白

参数：

- `src`: 待编辑的图像，必须是三通道uint8存储
- `mask`: 指定的颜色保留区域

### 样例程序

各种编辑方法对应的样例程序均在examples中，运行对应的main.py即可

## 免责声明

本项目仅为教学使用，样例程序中使用的图片来自于原论文和互联网，如有侵权请联系作者删除。作者对项目使用者使用项目所造成的后果不承担任何责任。
