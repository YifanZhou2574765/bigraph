from contextlib import nullcontext
from distutils.command.upload import upload
from distutils.errors import LinkError
from io import FileIO
from tkinter import *    # filedialog函数用于上传文件
from tkinter import filedialog
from xml.etree.ElementTree import Comment
from importlib_metadata import NullFinder
import numpy as np
from graphviz import *
import string

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
    nodeSet = [([0] * 4) for i in range(nodeNum)] # [index, name, linkNum, parentNodes, childrenNodes]
    
    for i in range(len(line0)):
        line0[i] = line0[i].replace("(", "") #去掉(
        line0[i] = line0[i].lstrip() #去掉字符串左边的空格
        line0[i] = line0[i].split()[1] #用空格分割字符串，取空格后的字符串
        line0[i] = line0[i].replace(" ", "") #去掉所有空格

        nodeSet[i][0] = i #index
        nodeSet[i][1] = line0[i].split(":")[0] #name
        nodeSet[i][2] = int(line0[i].split(":")[1]) #LinkNum
        nodeSet[i][3] = "" #parentNodes

    ######## 第二行：region数目，node数目，site数目 ########
    # 按照空格分开
    line2 = lines[1]
    regionNum = int(line2.split()[0])
    nodeNum = int(line2.split()[1])
    siteNum = int(line2.split()[2])


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
    regionSet = [([0] * 3) for i in range(regionNum)] #存放regions (region index, region name, parentNodes, childrenNodes)

    #将region名称插入rowIndex[]
    if(regionNum != 0):
        for region in range(regionNum):
            rowIndex.append("region"+str(region))

    #将node名称插入rowIndex[] & columnIndex[]
    if(nodeNum != 0):
        for node in range(nodeNum):
            rowIndex.append(nodeSet[node][1])
            columnIndex.append(nodeSet[node][1])
    
    #将site名称插入columnIndex[]
    if(siteNum != 0):
        for site in range(siteNum):
            columnIndex.append("site"+str(site))

    #### 遍历邻接矩阵 ####
    #遍历region行, regionSet - [region index, region name, parent node, children node]
    for r in range(regionNum): #行 -- parent node
        for c in range(len(columnIndex)): #列 -- children node
            if(adjacentMatrix[r][c] == '1'): #邻接矩阵元素为1 -> place graph有连接
                regionSet[r][0] = r #region index
                regionSet[r][1] = "region" + str(r) #region name
                regionSet[r][2] = "" #region没有parent node
                regionSet[r].append(columnIndex[c]) #columnIndex[c] -> children node
            if(adjacentMatrix[r][c] == '0'): #邻接矩阵元素为0 -> place graph无连接
                regionSet[r][0] = r #region index
                regionSet[r][1] = "region" + str(r) #region name
                regionSet[r][2] = "" #region没有parent node
    
    #nodeSet - [index, name, linkNum, parentNodes, childrenNodes]
    #遍历node -- 添加children node
    for r in range(regionNum, len(rowIndex)):
        for c in range(len(columnIndex)):
            if(adjacentMatrix[r][c] == '1'): #邻接矩阵元素为1 -> place graph有连接
                nodeSet[(r-regionNum)].append(columnIndex[c]) #columnIndex[c] -> children node
    #遍历node -- 添加parent node
    for r in range(len(rowIndex)):
        for c in range(nodeNum):
            if(adjacentMatrix[r][c] == '1'): #邻接矩阵元素为1 -> place graph有连接
                nodeSet[c][3] = rowIndex[r] #rowIndex[r] -> parent node
   
    # siteSet - [site index, site name, parent node]
    #遍历site -- 添加parent node
    for r in range(len(rowIndex)):
        for c in range(nodeNum, len(columnIndex)):
            if(adjacentMatrix[r][c] == '1'): #邻接矩阵元素为1 -> place graph有连接
                siteSet[c-nodeNum][0] = c-nodeNum
                siteSet[c-nodeNum][1] = "site"+ str(c-nodeNum)
                siteSet[c-nodeNum][2] = rowIndex[r] #rowIndex[r] -> parent node
            if(adjacentMatrix[r][c] == '0'): #邻接矩阵元素为0 -> place graph无连接
                siteSet[c-nodeNum][0] = c-nodeNum
                siteSet[c-nodeNum][1] = "site"+ str(c-nodeNum)
                siteSet[c-nodeNum][2] = "" #parent node为空


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

    ######## 画图 ########
    g = Graph(name="Bigraph", format="png")
    g.compound=True #cluster的必要声明

    #nodeSetWithoutLinknum [nodeIndex, nodeName, parentNodes, childrenNodes]
    nodeSetWithoutLinknum = nodeSet
    for n in range(len(nodeSetWithoutLinknum)):
        del nodeSetWithoutLinknum[n][2]

    allNode = regionSet + nodeSetWithoutLinknum + siteSet #regionSet + nodeSet
    nodeIndex = [node[:2] for node in allNode] #node的序列
    drawnNode = [] #存储所有已经被添加的node&region

    '''
    #定义添加节点函数
    def addBigraphNode(currentNode, c):
        currentNodeIndex_X = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0] #当前节点在二维数组allNode中的index_X
        #currentNodeIndex_Y = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][1] #当前节点在二维数组allNode中的index_Y
        childrenNodeNum = len(allNode[currentNodeIndex_X]) - 3 #当前节点的childrenNode个数   

        if(currentNode not in drawnNode): #该节点没有被添加    
            ##当前节点有childrenNode
            #当前节点只有一个childrenNode
            if(childrenNodeNum == 1):
                with c.subgraph(name='cluster') as c:
                    c.attr(label=currentNode, color='black')
                    drawnNode.append(currentNode)
                    print("CurrentNode: " + currentNode + " has 1 childrenNode. Its index is " + str(currentNodeIndex_X))
                    currentNode = allNode[currentNodeIndex_X][3] #currentNode更新为其子节点
                    print("CurrentNode has changed to: " + allNode[currentNodeIndex_X][3] + "; its index is: ", [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0])
                    addBigraphNode(currentNode, c)
                                        

            #当前节点有多个childrenNode
            if(childrenNodeNum > 1):
                with c.subgraph(name='cluster') as c:
                    c.attr(label=currentNode, color='black')
                    drawnNode.append(currentNode)
                    print("CurrentNode: " + currentNode + " has " + str(childrenNodeNum) + " childrenNode. Its index is " + str(currentNodeIndex_X))
                    parentNode = currentNode #父节点
                    print("now parent node is: " + parentNode)
                    for i in range(childrenNodeNum):
                        currentNode = allNode[currentNodeIndex_X][3+i] #currentNode更新为第i个childrenNode
                        print("CurrentNode: " + currentNode + "is the " + str(i) + "th childrenNode")
                        addBigraphNode(currentNode, c)
                        drawnNode.append(currentNode)
                        currentNode = parentNode
                        print("Current node return to " + currentNode)
                        
            #当前节点没有childrenNode
            if(childrenNodeNum == 0):    
                c.node(currentNode)
                drawnNode.append(currentNode)
        return g
    '''

    def addBigraphNode(currentNode, c):
        currentNodeIndex_X = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0] #当前节点在二维数组allNode中的index_X
        #currentNodeIndex_Y = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][1] #当前节点在二维数组allNode中的index_Y
        childrenNodeNum = len(allNode[currentNodeIndex_X]) - 3 #当前节点的childrenNode个数   

        if(currentNode not in drawnNode): #该节点没有被添加    
            ##当前节点有childrenNode
            #当前节点只有一个childrenNode
            if(childrenNodeNum == 1):
                name = 'cluster' + currentNode
                with c.subgraph(name=name) as c:
                    c.attr(color='black')
                    drawnNode.append(currentNode)
                    print("CurrentNode: " + currentNode + " has 1 childrenNode. Its index is " + str(currentNodeIndex_X))
                    currentNode = allNode[currentNodeIndex_X][3] #currentNode更新为其子节点
                    print("CurrentNode has changed to: " + allNode[currentNodeIndex_X][3] + "; its index is: ", [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0])
                    addBigraphNode(currentNode, c)
                                        

            #当前节点有多个childrenNode
            if(childrenNodeNum > 1):
                name = 'cluster' + currentNode
                with c.subgraph(name=name) as c:
                    c.attr(color='black')
                    drawnNode.append(currentNode)
                    print("CurrentNode: " + currentNode + " has " + str(childrenNodeNum) + " childrenNode. Its index is " + str(currentNodeIndex_X))
                    parentNode = currentNode #父节点
                    print("now parent node is: " + parentNode)
                    for i in range(childrenNodeNum):
                        currentNode = allNode[currentNodeIndex_X][3+i] #currentNode更新为第i个childrenNode
                        print("CurrentNode: " + currentNode + "is the " + str(i) + "th childrenNode")
                        addBigraphNode(currentNode, c)
                        drawnNode.append(currentNode)
                        currentNode = parentNode
                        print("Current node return to " + currentNode)
                        
            #当前节点没有childrenNode
            if(childrenNodeNum == 0):    
                c.node(currentNode)
                drawnNode.append(currentNode)
        return g


    def addBigraphAnchorNode(g):
        for i in range(len(anchorNode)):
            g.node(name=anchorNode[i], label=anchorNode[i])
        return g

    def addBigraphEdge(g):
        for i in range(len(nodePort)):
            # nodePort[i][1] -- node index
            # nodePort[i][3] -- anchor node
            indexOfNode = int(nodePort[i][1])
            edgeNode1 = nodeSet[indexOfNode][1] #该边连接的第一个点
            
            #如果该边连接的点有children node -> node name变为cluster
            edgeNode1Index = [(i, sub_list.index(edgeNode1)) for i, sub_list in enumerate(nodeIndex) if edgeNode1 in sub_list][0][0] #edgeNode2在二维数组nodeIndex中的index_X
            if(len(allNode[edgeNode1Index]) > 3): #如果有子节点
                edgeNode1 = "cluster" + edgeNode1

            edgeNode2 = nodePort[i][3] #该边连接的第二个点

            g.edge(edgeNode1, edgeNode2)

        return g

            
    with g.subgraph(name='cluster') as c:
        c.attr(color="white")
        addBigraphNode(allNode[0][1], c)
    addBigraphAnchorNode(g)
    addBigraphEdge(g)

    g.engine = "fdp" # fdp layout支持cluster连接
    g.view()

# upload按钮
uploadButton = Button(win, text='Upload', command=upload_file_process)
uploadButton.place(x=170, y=180)

# 主循环
win.mainloop()