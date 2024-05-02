import json
import os
from os.path import join as pathjoin
import numpy as np
from PIL import Image






# imgDir = r'../images/train'  # 待标注的图片路径
# labelDir = r'../labels/train'  # 存放标注txt的路径,同labelimg的save dir
# cropDir = r'../result/main'  # 存放裁剪完图片的目录



def saveForce(img,path):#不重复的存储图片
    respath = path
    for i in range(1000):
        if os.path.exists(respath) == True:
            dir,f=os.path.split(path)
            f='.'.join(f.split('.')[:-1])+str(i)+'.'+f.split('.')[-1]
            respath=pathjoin(dir,f)
            # print(path)
        else:
            break
    img.save(respath)


def create_json_cropImg(imagesPath, labelsPath, savePath):

    # imgs=[Image.open(pathjoin(imagesPath,img)) for img in os.listdir(imagesPath) if not len(img.split('.')) ==1 and if 'classes' not in img]#所有图片（原图）

    # 使用列表推導式讀取滿足條件的圖片
    print([img for img in os.listdir(imagesPath) if os.path.splitext(img)[1] and 'classes' not in img])
    imgs = [
        Image.open(os.path.join(imagesPath, img))
        for img in os.listdir(imagesPath)
        if os.path.splitext(img)[1] and 'classes' not in img
    ]
    
    labels=[x for x in os.listdir(labelsPath) if  x.find('classes') == -1]#所有标签
    classes = []
    with open(labelsPath + 'classes.txt', "r") as f:
        for c in f.readlines():
            classes.append(c.replace('\n', ''))
    print(classes)


    for i, txt in enumerate(labels):
        result = {}
        try:
            if not txt.find('class') == -1:
                continue
            posPath=pathjoin(labelsPath,txt)
            img=imgs[i]#当前标签对应的图片
            imgSize=img.size
            Prefabs = {}

            groups = []
            with open(posPath, "r") as f:
                for index, s in enumerate(f.readlines()):#每个框的坐标
                    print(index)
                    group = classes[int(s.split()[0])]
                    groups.append(group)
                    if 'children' not in group:
                        create_group = True
                        Prefabs[group] = {}
                        print(index, group)
                        points=list(map(float,s.split()))[1:]#(center.x,center.y,width,height),中心坐标和宽高
                        # print('points:',points)
                        leftup=(np.array((points[0],points[1]))*np.array([imgSize[0],imgSize[1]])).astype(int)#左上坐标（x,y)    #中心座標G
                        Prefabs[group]["name"] = group + '.prefab'
                        Prefabs[group]["type"] = "prefab"
                        Prefabs[group]["position"] = [int(leftup[0]), int(leftup[1])] #prefab_format
                        # print('leftup:',leftup)
                        wh=((np.array((points[2],points[3]))*np.array([imgSize[0],imgSize[1]])).astype(int))
                        # print('wh:',wh)
                        leftup=leftup-(wh/2).astype(int)#左上角
                        zone=[leftup[0],leftup[1],leftup[0]+wh[0],leftup[1]+wh[1]]#裁剪区域
                        # print('zone', zone)
                        # print('center', (leftup[0] + 0.5 * wh[0]), (leftup[1] + 0.5 * wh[1]))
                        detectedBox=img.crop(zone)
                        # print(pathjoin(savePath,'box'))
                        saveDir=pathjoin(savePath,f"{os.path.splitext(txt)[0]}")
                        if os.path.exists(saveDir) ==False:
                            os.mkdir(saveDir)
                        # saveForce(detectedBox,pathjoin(saveDir,f'{txt.split(".")[0]}_Image.jpg'))#保存检测后的子图到对应labels名称目录里
                        saveForce(detectedBox, saveDir + '/' + txt.split(".")[0] +'_'+ group +'_Image'+ str(index) +'.jpg')#保存检测后的子图到对应labels名称目录里
                        print('save', group, 'success!')
                    elif 'children' in group:
                        children = {}
                        groupName = '_'.join(group.split('_')[0:2])
                        # print(groupName, groups, '----')
                        if groupName in groups and create_group:
                            # print(groupName, groups)
                            Prefabs[groupName]["children"] = []
                            create_group = False
                        points=list(map(float,s.split()))[1:]#(center.x,center.y,width,height),中心坐标和宽高
                        # print('points:',points)
                        leftup=(np.array((points[0],points[1]))*np.array([imgSize[0],imgSize[1]])).astype(int)#左上坐标（x,y)    #中心座標G
                        # print('leftup:',leftup)
                        wh=((np.array((points[2],points[3]))*np.array([imgSize[0],imgSize[1]])).astype(int))
                        # print('wh:',wh)
                        leftup=leftup-(wh/2).astype(int)#左上角
                        zone=[leftup[0],leftup[1],leftup[0]+wh[0],leftup[1]+wh[1]]#裁剪区域
                        # print('zone', zone)
                        # print('center', (leftup[0] + 0.5 * wh[0]), (leftup[1] + 0.5 * wh[1]))
                        detectedBox=img.crop(zone)
                        # print(pathjoin(savePath,'box'))
                        saveDir=pathjoin(savePath,f"{os.path.splitext(txt)[0]}")
                        if os.path.exists(saveDir) == False:
                            os.mkdir(saveDir)
                        # saveForce(detectedBox,pathjoin(saveDir,f'{txt.split(".")[0]}_'+ group +'_Image', str(index) ,'.jpg'))#保存检测后的子图到对应labels名称目录里               
                        saveForce(detectedBox, saveDir + '/' + txt.split(".")[0] +'_'+ groupName +'_Image'+ str(index) +'.jpg')#保存检测后的子图到对应labels名称目录里
                        children["name"] = saveDir + '/' + txt.split(".")[0] +'_'+ groupName +'_Image'+ str(index)+'.jpg'
                        children["type"] = "sprite"
                        children["position"] = [int(leftup[0]), int(leftup[1])]
                        print(Prefabs[groupName]["children"])
                        Prefabs[groupName]["children"].append(children)
                        print('save', group, 'success!')

            
            
            result["name"] = txt.split('.')[0]+ ".node"
            result["type"] = "node"
            result["children"] = []
            result["children"].append(Prefabs)

            print(savePath + txt.split('.')[0] +'.json')
            with open(savePath + txt.split('.')[0] +'.json', 'w', encoding= 'utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False))

                            # saveForce(detectedBox, saveDir + )#保存检测后的子图到对应labels名称目录里
            print('-'*30)
        except Exception as e:
            print(f"保存{txt}时出错\n{e}")

# create_json_cropImg(imagesPath, labelsPath, savePath)