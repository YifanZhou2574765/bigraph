from distutils.command.upload import upload
from distutils.errors import LinkError
from io import FileIO
from tkinter import *    # filedialog函数用于上传文件
from tkinter import filedialog
from importlib_metadata import NullFinder
import numpy as np

######## 创建交互窗口 -> 用户在窗口选择需要读取的文件  ########
win = Tk()
win.title('Upload Your Bigraph File')
win.geometry('400x400')

######## 上传文件 ########
# 点击上传按钮的时候调用此函数
def upload_file_process():
    # 默认打开路径（MacOS系统与Window系统路径不同）
    file_path = filedialog.askopenfilename(initialdir='/Users/') #MacOS System
    #file_path = filedialog.askopenfilename(initialdir='C:/') #Windows System
    
    selectedFile = open(file_path, 'r')
    
    # 将文件按行读取，然后存贮到lines数组中
    line = selectedFile.readline().strip() #strip() 去除前后空格
    lines = []
    lines.append(line)
    while line:
        line = selectedFile.readline().strip()
        lines.append(line)
    selectedFile.close() #关闭文件
    
    ######## 第一行：点的集合 ########
    line0 = lines[0]
    line0 = line0.strip("{(").strip(")}") #去掉首尾字符
    line0 = line0.replace(",", "") #去掉字符串中所有都好
    line0 = line0.split(")") #按照)分割字符串
    
    nodeNum = len(line0)
    nodeSet = [([0] * 4) for i in range(nodeNum)] # [index, name, linkNum, parentNode]
    
    for i in range(len(line0)):
        line0[i] = line0[i].replace("(", "") #去掉(
        line0[i] = line0[i].lstrip() #去掉字符串左边的空格
        line0[i] = line0[i].split()[1] #用空格分割字符串，取空格后的字符串
        line0[i] = line0[i].replace(" ", "") #去掉所有空格

        nodeSet[i][0] = i #index
        nodeSet[i][1] = line0[i].split(":")[0] #name
        nodeSet[i][2] = int(line0[i].split(":")[1]) #LinkNum
        nodeSet[i][3] = " "

    ######## 第二行：region数目，node数目，site数目 ########
    # 按照空格分开
    line2 = lines[1]
    regionNum = int(line2.split()[0])
    nodeNum = int(line2.split()[1])
    siteNum = int(line2.split()[2])

    #print(regionNum, nodeNum, siteNum)

    ######## 邻接矩阵 -- place graph ########
    # 邻接矩阵范围：2 ～ 2+regionNum+nodeNum-1
    # 邻接矩阵形状：[regionNum+nodeNum, nodeNum+siteNum]
    lineAM = lines[2:2+regionNum+nodeNum]
    adjacentMatrix = [([0] * (nodeNum+siteNum)) for i in range(regionNum+nodeNum)]
    # 将元素存储到adjacentMatrix中
    for i in range(regionNum+nodeNum):
        for j in range(nodeNum+siteNum):
            adjacentMatrix[i][j] = lineAM[i].split(" ")[j]
   
    rowIndex = [] #邻接矩阵行名称
    columnIndex = [] #邻接矩阵列名称
    siteSet = [([0] * 3) for i in range(siteNum)] #存放sites (site index, site name, parent node)

    #将region名称插入rowIndex[]
    if(regionNum != 0):
        for region in range(regionNum):
            rowIndex.append(region)
    
    #将node名称插入rowIndex[] & columnIndex[]
    if(nodeNum != 0):
        for node in range(nodeNum):
            rowIndex.append(nodeSet[node][1])
            columnIndex.append(nodeSet[node][1])
    
    #将site名称插入columnIndex[]
    if(siteNum != 0):
        for site in range(siteNum):
            columnIndex.append(site)

    #### 遍历邻接矩阵 ####
    # 遍历node
    for r in range(len(rowIndex)): #行 -- parent node
        for c in range(len(columnIndex)): #列 -- children node
            if (adjacentMatrix[r][c] == 1): #邻接矩阵元素为1 -> place graph有连接
                nodeSet[c][3] = rowIndex[r] #rowIndex[r] -> node name -> parent node


        for c in range(siteNum): #遍历site列
            if(adjacentMatrix[r][c] == 1): #邻接矩阵元素为1 -> place graph有连接 ->bigraph有嵌套
                siteSet[c][0] = c #site index
                siteSet[c][1] = c #site name
                siteSet[c][2] = rowIndex[r] #site parent; rowIndex[r] -> node name
            if(adjacentMatrix[r][c] == 0):
                siteSet[c][0] = c # site index
                siteSet[c][1] = c # site name

    ######## link graph ########
    # 范围: 2+regionNum+nodeNum, len(lines)
    lineLG = lines[(2+regionNum+nodeNum):(len(lines)-1)]
    linkSet = [([0] * 4) for i in range(len(lineLG))] #存储所有边信息[innerName, outerName, linkEdge, linkIndex]
    anchorNode = []
    nodePort = [] #输出的边所连接的点 [edge index, node index, port index, anchor node index]

    for i in range(len(lineLG)):
        lineLG[i] = lineLG[i] .strip("(").strip(")") #去掉首尾字符
        lineLG[i] = lineLG[i].replace(",", " ") #去掉字符串所有逗号
        lineLG[i] = lineLG[i].split("}") #按照}分割字符串

        # link -- [innerName, outerName, linkEdge, linkIndex]
        # 用link存储每个边的信息
        linkSet[i][0] = lineLG[i][0].replace("{", " ").strip() #去掉{和空格
        linkSet[i][1] = lineLG[i][1].replace("{", " ").strip() #去掉{和空格
        linkSet[i][2] = lineLG[i][2].replace("{", " ").strip() #去掉{和空格
        linkSet[i][3] = i
        anchorNode.append("anchorNode"+str(i))

        #处理link.edge 不止一个node
        nodesOfEdges = linkSet[i][2].split(")") #用)分割字符串

        for j in range(len(nodesOfEdges)-1):
            nodesOfEdges[j] = nodesOfEdges[j].replace("(", "").lstrip() #去掉(和左边的空格
            nodesOfEdges[j] = nodesOfEdges[j].split(" ")
            

            for k in range(len(nodesOfEdges[j])-1):
                anchorNodeIndex = "anchorNode" + str(i)
                # [edge index, node index, port index, anchor node index]
                nodePort.append([i, nodesOfEdges[j][0], nodesOfEdges[j][1], anchorNodeIndex])
        
    print(nodePort)

    ######## 画图 ########



# upload按钮
uploadButton = Button(win, text='Upload', command=upload_file_process)
uploadButton.place(x=170, y=180)

# 主循环
win.mainloop()



