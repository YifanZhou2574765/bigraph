from contextlib import nullcontext
from distutils.command.upload import upload
from distutils.errors import LinkError
from io import FileIO
from re import I
from tkinter import *    # filedialog函数用于上传文件 #filedialog function for uploading files
from tkinter import filedialog
from turtle import shape
from xml.etree.ElementTree import Comment
from importlib_metadata import NullFinder
import numpy as np
from graphviz import *
import string

######## 创建交互窗口 -> 用户在窗口选择需要读取的文件  ########
######## Create an interactive window -> the user selects the file to be read in the window ########
win = Tk()
win.title('Upload Your Bigraph File')
win.geometry('400x400')

######## 上传文件 ########
######## upload file ########
# 点击上传按钮的时候调用此函数 #This function is called when the upload button is clicked
def upload_file_process():
    # 默认打开路径（MacOS系统与Window系统路径不同） # Default open path (MacOS systems have a different path than Window systems)
    #file_path = filedialog.askopenfilename(initialdir='/Users/') #MacOS System
    file_path = filedialog.askopenfilename(initialdir='C:/') #Windows System
    
    selectedFile = open(file_path, 'r')
    
    # 将文件按行读取，然后存贮到lines数组中 #Read the file by line and store it in the lines array
    line = selectedFile.readline().strip() #strip() to remove space before and after the string
    lines = []
    lines.append(line)
    while line:
        line = selectedFile.readline().strip()
        lines.append(line)
    selectedFile.close() #关闭文件 #close file
    
    ######## 第一行：点的集合 ########
    ######## 1st line: set of nodes ########
    line0 = lines[0]
    line0 = line0.strip("{(").strip(")}") #去掉首尾字符 #Removal of first and last characters
    line0 = line0.replace(",", "") #去掉字符串中所有, #Remove all ,
    line0 = line0.split(")") #按照)分割字符串 #split the string with)
    
    nodeNum = len(line0)
    nodeSet = [([0] * 4) for i in range(nodeNum)] # [index, name, linkNum, parentNodes, childrenNodes]
    
    for i in range(len(line0)):
        line0[i] = line0[i].replace("(", "") #去掉( #remove (
        line0[i] = line0[i].lstrip() #去掉字符串左边的空格 #Remove spaces to the left of the string
        line0[i] = line0[i].split()[1] #用空格分割字符串，取空格后的字符串 #Split the string with a space and take the string after the space
        line0[i] = line0[i].replace(" ", "") #去掉所有空格 #remove all space

        nodeSet[i][0] = i #index
        nodeSet[i][1] = line0[i].split(":")[0] + str(i) #name
        nodeSet[i][2] = int(line0[i].split(":")[1]) #LinkNum
        nodeSet[i][3] = "" #parentNodes

    print(nodeSet)
    ######## 第二行：region数目，node数目，site数目 ########
    ######## 2nd line：region number，node number，site number ########
    # 按照空格分开 #split with space
    line2 = lines[1]
    regionNum = int(line2.split()[0])
    nodeNum = int(line2.split()[1])
    siteNum = int(line2.split()[2])


    ######## 邻接矩阵 -- place graph ########
    ######## adjacent Matrix -- place graph ########
    # range：2 ～ 2+regionNum+nodeNum-1
    # shape：[regionNum+nodeNum, nodeNum+siteNum]
    lineAM = lines[2:2+regionNum+nodeNum]
    adjacentMatrix = [([0] * (nodeNum+siteNum)) for i in range(regionNum+nodeNum)]

    # 将元素存储到adjacentMatrix中 #Storing elements in an adjacentMatrix
    for i in range(regionNum+nodeNum):
        for j in range(nodeNum+siteNum):
            adjacentMatrix[i][j] = lineAM[i][j]
   
    rowIndex = [] #邻接矩阵行名称 #row name of adjacentMatrix
    columnIndex = [] #邻接矩阵列名称 #column name of adjacentMatrix
    siteSet = [([0] * 3) for i in range(siteNum)] #store sites (site index, site name, parent node)
    regionSet = [([0] * 3) for i in range(regionNum)] #store regions (region index, region name, parentNodes, childrenNodes)

    #将region名称插入rowIndex[] #insert region name into rowIndex[]
    if(regionNum != 0):
        for region in range(regionNum):
            rowIndex.append("region"+str(region))

    #将node名称插入rowIndex[] & columnIndex[] #insert node name into rowIndex[]
    if(nodeNum != 0):
        for node in range(nodeNum):
            rowIndex.append(nodeSet[node][1])
            columnIndex.append(nodeSet[node][1])
    
    #将site名称插入columnIndex[] #insert site name into columnIndex[]
    if(siteNum != 0):
        for site in range(siteNum):
            columnIndex.append("site"+str(site))

    #### 遍历邻接矩阵 ####
    #### Traversing the adjacency matrix ####
    #Traversing region rows, regionSet - [region index, region name, parent node, children node]
    for r in range(regionNum): #row -- parent node
        for c in range(len(columnIndex)): #column -- children node
            if(adjacentMatrix[r][c] == '1'): #邻接矩阵元素为1 -> place graph有连接 #adjacency matrix with element 1 -> place graph is connected
                regionSet[r][0] = r #region index
                regionSet[r][1] = "region" + str(r) #region name
                regionSet[r][2] = "" #region没有parent node #region have no parent node
                regionSet[r].append(columnIndex[c]) #columnIndex[c] -> children node
            if(adjacentMatrix[r][c] == '0'): #邻接矩阵元素为0 -> place graph无连接 #adjacency matrix with 0 elements -> place graph unconnected
                regionSet[r][0] = r # region index
                regionSet[r][1] = "region" + str(r) #region name
                regionSet[r][2] = "" #region没有parent node #region have no parent node
    
    #nodeSet - [index, name, linkNum, parentNodes, childrenNodes]
    #Traversing node -- add children node
    for r in range(regionNum, len(rowIndex)):
        for c in range(len(columnIndex)):
            if(adjacentMatrix[r][c] == '1'): #邻接矩阵元素为1 -> place graph有连接 #adjacency matrix with element 1 -> place graph is connected
                nodeSet[(r-regionNum)].append(columnIndex[c]) #columnIndex[c] -> children node
    #遍历node -- 添加parent node
    #Traversing node -- add parent node
    for r in range(len(rowIndex)):
        for c in range(nodeNum):
            if(adjacentMatrix[r][c] == '1'): #邻接矩阵元素为1 -> place graph有连接 #adjacency matrix with element 1 -> place graph is connected
                nodeSet[c][3] = rowIndex[r] #rowIndex[r] -> parent node
   
    # siteSet - [site index, site name, parent node]
    #遍历site -- 添加parent node
    #Traversing site -- add parent node
    for r in range(len(rowIndex)):
        for c in range(nodeNum, len(columnIndex)):
            if(adjacentMatrix[r][c] == '1'): #邻接矩阵元素为1 -> place graph有连接 #adjacency matrix with element 1 -> place graph is connected
                siteSet[c-nodeNum][0] = c-nodeNum
                siteSet[c-nodeNum][1] = "site"+ str(c-nodeNum)
                siteSet[c-nodeNum][2] = rowIndex[r] #rowIndex[r] -> parent node
            if(adjacentMatrix[r][c] == '0'): #邻接矩阵元素为0 -> place graph无连接 #adjacency matrix with 0 elements -> place graph unconnected
                siteSet[c-nodeNum][0] = c-nodeNum
                siteSet[c-nodeNum][1] = "site"+ str(c-nodeNum)
                siteSet[c-nodeNum][2] = "" #parent node为空 #parent node is empty


    ######## link graph ########
    # range: 2+regionNum+nodeNum, len(lines)
    lineLG = lines[(2+regionNum+nodeNum):(len(lines)-1)]
    linkSet = [([0] * 4) for i in range(len(lineLG))] #存储所有边信息[innerName, outerName, linkEdge, linkIndex] #Store all side information
    anchorNode = []
    nodePort = [] #输出的边所连接的点 [edge index, node index, port index, anchor node index] #The nodes to which the output edge is connected


    for i in range(len(lineLG)):
        lineLG[i] = lineLG[i] .strip("(").strip(")") #去掉首尾字符  #Remove of first and last characters
        lineLG[i] = lineLG[i].replace(",", " ") #去掉字符串所有逗号 #remove all , in the string
        lineLG[i] = lineLG[i].split("}") #按照}分割字符串 #split the string with}

        # link -- [innerName, outerName, linkEdge, linkIndex]
        # 用link存储每个边的信息 #Store information about each edge with link
        linkSet[i][0] = lineLG[i][0].replace("{", " ").strip() #去掉{和空格 #remove { and space
        linkSet[i][1] = lineLG[i][1].replace("{", " ").strip() #去掉{和空格 #remove { and space
        linkSet[i][2] = lineLG[i][2].replace("{", " ").strip() #去掉{和空格 #remove { and space
        linkSet[i][3] = i
        anchorNode.append("anchorNode"+str(i))

        #处理link.edge 不止一个node #Handling link.edge More than one node
        nodesOfEdges = linkSet[i][2].split(")") #用)分割字符串

        for j in range(len(nodesOfEdges)-1):
            nodesOfEdges[j] = nodesOfEdges[j].replace("(", "").lstrip() #去掉(和左边的空格 Remove (and the space to the left
            nodesOfEdges[j] = nodesOfEdges[j].split(" ")

            for k in range(len(nodesOfEdges[j])-1):
                anchorNodeIndex = "anchorNode" + str(i)
                
            # [edge index, node index, port index, anchor node index]
            nodePort.append([i, nodesOfEdges[j][0], nodesOfEdges[j][1], anchorNodeIndex])
            print(nodePort)
        

    ######## drawing bigraph ########
    g = Graph(name="Bigraph", format="png")
    g.compound=True #cluster的必要声明 #Required declaration for cluster

    #nodeSetWithoutLinknum [nodeIndex, nodeName, parentNodes, childrenNodes]
    nodeSetWithoutLinknum = nodeSet
    for n in range(len(nodeSetWithoutLinknum)):
        del nodeSetWithoutLinknum[n][2]

    allNode = regionSet + nodeSetWithoutLinknum + siteSet #regionSet + nodeSet
    nodeIndex = [node[:2] for node in allNode] #node index
    drawnNode = [] #存储所有已经被添加的node&region #Store all nodes&regions that have been added

    
    def addBigraphNode(currentNode, c):
        currentNodeIndex_X = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0] #当前节点在二维数组allNode中的index_X #Index_X of the current node in the two-dimensional array allNode
        #currentNodeIndex_Y = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][1] #当前节点在二维数组allNode中的index_Y #Index_Y of the current node in the two-dimensional array allNode
        childrenNodeNum = len(allNode[currentNodeIndex_X]) - 3 #当前节点的childrenNode个数    #Number of childrenNode of the current node   

        if(currentNode not in drawnNode): #该节点没有被添加    #This node has not been added 
            ##当前节点有childrenNode #current node have childrenNode
            #当前节点只有一个childrenNode #current node have only one childrenNode
            if(childrenNodeNum == 1):
                name = 'cluster' + currentNode
                with c.subgraph(name=name) as c:
                    c.attr(label=currentNode, color='black')
                    drawnNode.append(currentNode)
                    print("CurrentNode: " + currentNode + " has 1 childrenNode. Its index is " + str(currentNodeIndex_X))
                    currentNode = allNode[currentNodeIndex_X][3] #currentNode更新为其子节点 #currentNode is updated to its child node
                    print("CurrentNode has changed to: " + allNode[currentNodeIndex_X][3] + "; its index is: ", [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0])
                    addBigraphNode(currentNode, c)
                                        

            #当前节点有多个childrenNode #current node have more than one childrenNode
            if(childrenNodeNum > 1):
                name = 'cluster' + currentNode
                with c.subgraph(name=name) as c:
                    c.attr(label=currentNode, color='black')
                    drawnNode.append(currentNode)
                    print("CurrentNode: " + currentNode + " has " + str(childrenNodeNum) + " childrenNode. Its index is " + str(currentNodeIndex_X))
                    parentNode = currentNode #父节点
                    print("now parent node is: " + parentNode)
                    for i in range(childrenNodeNum):
                        currentNode = allNode[currentNodeIndex_X][3+i] #currentNode更新为第i个childrenNode #currentNode is updated to the i-th childNode
                        print("CurrentNode: " + currentNode + "is the " + str(i) + "th childrenNode")
                        addBigraphNode(currentNode, c)
                        drawnNode.append(currentNode)
                        currentNode = parentNode
                        print("Current node return to " + currentNode)
                        
            #当前节点没有childrenNode #current node have no childrenNode
            if(childrenNodeNum == 0):    
                c.node(currentNode)
                drawnNode.append(currentNode)
        return g
    '''
    #不判断是否画过
    def addBigraphNode(currentNode, c):
        currentNodeIndex_X = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0] #当前节点在二维数组allNode中的index_X
        #currentNodeIndex_Y = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][1] #当前节点在二维数组allNode中的index_Y
        childrenNodeNum = len(allNode[currentNodeIndex_X]) - 3 #当前节点的childrenNode个数   

        #if(currentNode not in drawnNode): #该节点没有被添加    
        ##当前节点有childrenNode
        #当前节点只有一个childrenNode
        if(childrenNodeNum == 1):
            name = 'cluster' + currentNode
            with c.subgraph(name=name) as c:
                c.attr(label=currentNode, color='black')
                #drawnNode.append(currentNode)
                print("CurrentNode: " + currentNode + " has 1 childrenNode. Its index is " + str(currentNodeIndex_X))
                currentNode = allNode[currentNodeIndex_X][3] #currentNode更新为其子节点
                print("CurrentNode has changed to: " + allNode[currentNodeIndex_X][3] + "; its index is: ", [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0])
                addBigraphNode(currentNode, c)
                                        

        #当前节点有多个childrenNode
        if(childrenNodeNum > 1):
            name = 'cluster' + currentNode
            with c.subgraph(name=name) as c:
                c.attr(label=currentNode, color='black')
                #drawnNode.append(currentNode)
                print("CurrentNode: " + currentNode + " has " + str(childrenNodeNum) + " childrenNode. Its index is " + str(currentNodeIndex_X))
                parentNode = currentNode #父节点
                print("now parent node is: " + parentNode)
                for i in range(childrenNodeNum):
                    currentNode = allNode[currentNodeIndex_X][3+i] #currentNode更新为第i个childrenNode
                    print("CurrentNode: " + currentNode + "is the " + str(i) + "th childrenNode")
                    addBigraphNode(currentNode, c)
                    #drawnNode.append(currentNode)
                    currentNode = parentNode
                    print("Current node return to " + currentNode)
                        
        #当前节点没有childrenNode
        if(childrenNodeNum == 0):    
            c.node(currentNode)
            drawnNode.append(currentNode)
        return g
    '''

    def addBigraphAnchorNode(g):
        for i in range(len(anchorNode)):
            g.node(name=anchorNode[i], label=anchorNode[i], shape='point')
        return g

    def addBigraphEdge(g):
        for i in range(len(nodePort)):
            # nodePort[i][1] -- node index
            # nodePort[i][3] -- anchor node
            indexOfNode = int(nodePort[i][1])
            edgeNode1 = nodeSet[indexOfNode][1] #该边连接的第一个点 #The first node joined by this side
            
            #如果该边连接的点有children node -> node name变为cluster # If the point connected by this edge has children node -> node name becomes cluster
            edgeNode1Index = [(i, sub_list.index(edgeNode1)) for i, sub_list in enumerate(nodeIndex) if edgeNode1 in sub_list][0][0] #edgeNode2在二维数组nodeIndex中的index_X #index_X of edgeNode2 in the two-dimensional array nodeIndex
            
            if(len(allNode[edgeNode1Index]) > 3): #如果有子节点 #If there are child nodes
                edgeNode1 = "cluster" + edgeNode1

            edgeNode2 = nodePort[i][3] #该边连接的第二个点 #The second point joined by this side

            g.edge(edgeNode1, edgeNode2, label=linkSet[nodePort[i][0]][1])
            print("edgeNode1: " + edgeNode1 + " edgeNode2: " + edgeNode2)

        return g

            
    with g.subgraph(name='cluster') as c:
        c.attr(color="white")
        addBigraphNode(allNode[0][1], c)
    addBigraphAnchorNode(g)
    addBigraphEdge(g)

    g.engine = "fdp" # fdp layout支持cluster连接 #fdp layout supports cluster connections
    g.view()

# upload button
uploadButton = Button(win, text='Upload', command=upload_file_process)
uploadButton.place(x=170, y=180)

# main loop
win.mainloop()