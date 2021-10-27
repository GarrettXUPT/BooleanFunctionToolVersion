import time
import copy
from multiprocessing import Process

'''
    按读取的行进行转化
'''
def lineTrans(line):
    brack  = 0  # 中括号计数
    tmpLst = []  # 临时数组
    resList = [] # 结果数组
    tmpnum = "" # 数字拼接时临时数字
    tmpStr = "" # 临时字符串
    for ele in line:

        if ele == "[" or ele == "]":
            brack += 1
            continue
        if ele == " " and brack != 2:
            continue
        if ele.isdigit() or ele == ".":
            tmpnum += ele
            continue
        if ele == ",":
            tmpLst.append(int(tmpnum))
            tmpnum = ""
        # 短表结束
        if brack == 2:
            tmpLst.append(int(tmpnum))
            resList.append(copy.deepcopy(tmpLst))
            tmpLst.clear()
            brack = 0
    # 计算指标
    for ele in line:
        if ele == "[" or ele == "]":
            brack += 1
            continue
        if brack == 2:
            tmpStr += ele
        strList = tmpStr.split(" ")
    for ele in strList[1:]:  # 去除空串元素, 我定义 你也不用 我不定义 你就警告 哎。。。太难了
        resList.append((ele))
    # print(resList)
    return resList

'''
    将文件数据转化为列表形式
'''
def fileToList1(strAddress):
    Lst = []
    with open(strAddress, mode = "r+", encoding = "utf-8") as f:
        line = f.readlines()
        for ele in line:
            transRes = lineTrans(ele)
            if len(transRes) == 0:
                continue
            if "*" in transRes:
                continue
            Lst.append(transRes)
    return Lst

if __name__ == '__main__':
    res = fileToList1("matrix.txt")
    print(res[0][0])
