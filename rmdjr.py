# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 23:38:33 2017

@author: Administrator
"""

import os
def removeDir(dirPath,redir=0):#list type
    if not os.path.isdir(dirPath) or not os.path.exists(dirPath) :#如果既不是文件、也不是文件and not os.path.isfile(dirPath)
        return
    try:
        if os.path.isfile(dirPath):#若是已存在的文件，先删除，自生成新的之前直接覆盖
            os.remove(dirPath)
        else:#若是目录，递归删除目录内的文件，在删除空目录 删除
            files = os.listdir(dirPath)
            for file in files:
                filePath = os.path.join(dirPath, file)
                if os.path.isfile(filePath):
                    os.remove(filePath)
                elif os.path.isdir(filePath):
                    removeDir(filePath)
        if redir:#连空文件夹也删除，若为0 ，则只清空文件夹内的文件
            os.rmdir(dirPath)
    except Exception, e:
        return e
def rmdAndmkd(dirPath,rempdir=0,mksd=1):
    removeDir(dirPath,redir=rempdir)
    if os.path.exists(dirPath):
        mksd=0
    if mksd:
        os.makedirs(dirPath)

if __name__ == "__main__":
	removeDir(r'C:\Users\z81022868\Desktop\EA5800-X17(N63E-22) 快速安装指南 01\XML_799'.decode('utf-8'))
