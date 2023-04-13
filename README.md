# LabelSAM-for-yolo
简易的yolo半自动标注库，目前只支持单目标。如果数据集图片背景复杂，可能工作量不比直接标的小，因为sam是通用的分割模型。但是开源适当通过调整参数修改。

主要源码在LabelSAM文件夹内。

### 环境：
请去[facebookresearch/segment-anything: The repository provides code for running inference with the SegmentAnything Model (SAM), links for downloading the trained model checkpoints, and example notebooks that show how to use the model. (github.com)](https://github.com/facebookresearch/segment-anything)
处下载 

```
segment_anything
```

文件夹，并将其放到项目的LabelSAM/下。

并于

```
https://github.com/facebookresearch/segment-anything#model-checkpoints
```

下载对应模型。

### python环境：

```
python>=3.8, as well as pytorch>=1.7 and torchvision>=0.8,opencv-python>=4.6.0
```


## 注意：SAM的推理对gpu性能要求较高，作者本身是3060，使用vit_l模型推理一张1080p的图像算是快显存极限了。不赶时间的话，gpu又不太好的同学，可以使用cpu训练，然后挂着跑。
###将loadModel中的device参数改为'cpu'.



### 基于SAM的yolo半自动标注后端。请配合labelimg使用，或者将生成的标注文件自己移动到其他软件下使用。

用法很简单，源码也加满了注释。直接使用的话可以将待处理图片放入

```
images/train
```

文件夹内

标注文件的默认路径在

```
labels/train
```

内，其中的temp文件夹都是给用户临时存放文件的。
###然后运行main.py文件

可以选择是否保存检测完的图像，默认存放在

```
result/main
```
中。

最后，作者也是第一次开源这种项目，github也不太会用，课也多，开源细则可能理解的不充分，代码也烂。如果有大佬看不下去了可以直接锐评 qwq

可以的话能给我个小⭐⭐吗....
