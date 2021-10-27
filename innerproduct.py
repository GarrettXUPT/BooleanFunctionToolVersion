from truthTable import AlltruTable
import numpy as np
import time

'''
    将由文件读取的字符串转化为原来的列表形式
'''
def strToList(str):
    resList = []
    len1 = len(str) - 1
    for i in range(len1):
        if  (not str[i - 1].isdigit()) and str[i].isdigit() and str[i + 1] == "," and str[i + 2] == " ":
            resList.append(int(str[i]))
        elif str[i].isdigit() and str[i + 1].isdigit() and (str[i + 2] == "," or str[i + 2] == "]"):
            resList.append(int(str[i] + str[i + 1]))
        elif (not str[i - 1].isdigit()) and str[i].isdigit() and str[i + 1] == "]":
            resList.append(int(str[i]))
    return resList


'''
    向量间相乘
'''
def lstMultiply(lst1, lst2):
    return np.multiply(np.array(lst1), np.array(lst2))


'''
    单纯的乘积
'''
def multiply(x, w):
    return x * w

'''
    选择根据元数选择使用的点积运算
'''
def innerProductSelect(AlltruthTable):
    resList1 = []
    for ele in AlltruthTable:
        for elem in AlltruthTable:
            resList1.append(sum(lstMultiply(ele, elem)))
    return resList1

if __name__ == '__main__':
    pass
