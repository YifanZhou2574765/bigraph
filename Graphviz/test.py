from graphviz import Graph

g = Graph(name='testG', format="png")

with g.subgraph(name='cluster') as c:
    c.attr(color='white')
    with c.subgraph(name='cluster') as c:
        c.attr(label='region0', color='black')
        with c.subgraph(name='cluster') as c:
            c.attr(label='A')
            with c.subgraph(name='cluster') as c:
                c.attr(label='Snd')
                with c.subgraph(name='cluster') as c:
                    c.attr(label='Ready')
                    c.node('Fun')      
                c.node('M')  
            

g.view()

'''
    #定义添加节点函数
    def addGraphNode(currentNode, c):
        currentNodeIndex_X = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0] #当前节点在二维数组allNode中的index_X
        #currentNodeIndex_Y = [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][1] #当前节点在二维数组allNode中的index_Y
        childrenNodeNum = len(allNode[currentNodeIndex_X]) - 3 #当前节点的childrenNode个数   

        #with g.subgraph(name='cluster') as c:
            #c.attr(color='white')
            #c.attr(label='test')

        if(currentNode not in drawnNode): #该节点没有被添加    
            ##当前节点有childrenNode
                    
            #当前节点无父节点
            if(len(allNode[currentNodeIndex_X][2]) == 0): 
                #当前节点只有一个childrenNode
                if(childrenNodeNum == 1):
                    with c.subgraph(name='cluster') as c:
                        c.attr(label=currentNode, color='black')
                        drawnNode.append(currentNode)
                        print("currentNode: " + currentNode + " has 1 childrenNode. Its index is " + str(currentNodeIndex_X))
                        currentNode = allNode[currentNodeIndex_X][3] #currentNode更新为其子节点
                        print("currentNode has changed to: " + allNode[currentNodeIndex_X][3] + "; Its index is: ", [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0])
                        addGraphNode(currentNode, c)
                                    

                #当前节点有多个childrenNode
                if(childrenNodeNum > 1):
                    with c.subgraph(name='cluster') as c:
                        c.attr(label=currentNode, color='black')
                        drawnNode.append(currentNode)
                        print(currentNode + " has " + str(childrenNodeNum) + " childrenNode. Its index is " + str(currentNodeIndex_X))
                        parentNode = currentNode #父节点
                        print("now parent node is: " + parentNode)
                        for i in range(childrenNodeNum):
                            currentNode = allNode[currentNodeIndex_X][3+i] #currenNode更新为第i个子节点
                            print("currentNode: " + currentNode + " is the " + str(i) + "th childrenNode")
                            addGraphNode(currentNode, c)
                            drawnNode.append(currentNode)
                            currentNode = parentNode
                            print("current node return to " + currentNode)
                    
                #当前节点没有childrenNode
                if(childrenNodeNum == 0):      
                    c.node(currentNode)
                    drawnNode.append(currentNode)
                    

            #当前节点有父节点
            if(len(allNode[currentNodeIndex_X][2]) > 0):
                #当前节点只有一个childrenNode
                if(childrenNodeNum == 1):
                    with c.subgraph(name='cluster') as c:
                        c.attr(label=currentNode, color='black')
                        drawnNode.append(currentNode)
                        print("CurrentNode: " + currentNode + " has 1 childrenNode. Its index is " + str(currentNodeIndex_X))
                        currentNode = allNode[currentNodeIndex_X][3] #currentNode更新为其子节点
                        print("CurrentNode has changed to: " + allNode[currentNodeIndex_X][3] + "; its index is: ", [(i, sub_list.index(currentNode)) for i, sub_list in enumerate(nodeIndex) if currentNode in sub_list][0][0])
                        addGraphNode(currentNode, c)
                                        

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
                            addGraphNode(currentNode, c)
                            drawnNode.append(currentNode)
                            currentNode = parentNode
                            print("Current node return to " + currentNode)
                        
                #当前节点没有childrenNode
                if(childrenNodeNum == 0):    
                    c.node(currentNode)
                    drawnNode.append(currentNode)

            return g 
'''