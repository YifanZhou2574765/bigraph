from distutils.command.upload import upload
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
    line0 = line0.replace(",", "") #去掉字符串中所有空格
    line0 = line0.split(")") #按照)分割字符串
    
    nodeNum = len(line0)
    nodeSet = [([0] * 3) for i in range(nodeNum)] # [index, name, linkNum]
    
    for i in range(len(line0)):
        line0[i] = line0[i].replace("(", "") #去掉(
        line0[i] = line0[i].lstrip() #去掉字符串左边的空格
        line0[i] = line0[i].split()[1] #用空格分割字符串，取空格后的字符串
        line0[i] = line0[i].replace(" ", "") #去掉所有空格

        nodeSet[i][0] = i #index
        nodeSet[i][1] = line0[i].split(":")[0] #name
        nodeSet[i][2] = int(line0[i].split(":")[1]) #LinkNum

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




    

        
# upload按钮
uploadButton = Button(win, text='Upload', command=upload_file_process)
uploadButton.place(x=170, y=180)

# 主循环
win.mainloop()



