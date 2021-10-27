import time
import copy
from truthTable import AlltruTable
from flieToLst import fileToList1
from walsh_and_nonlinearity import walshCompute, nonlinearityCompute
from innerproduct import innerProductSelect
from transparency import  autocorrelation, transparencyCompute
import random
from innerproduct import strToList
import numpy as np


"================================创建轨道(四、六、八元)======================================"
'''
    真值表输入循环移位
    input: lst 当前需要移位的列表
'''
def moveBit(lst, num):
    tmpList = copy.deepcopy(lst)
    for i in range(num):
        tmpList.insert(0, tmpList.pop())
    return tmpList

'''
    轨道输入移位
    input: oribit 当前需要移位的轨道
    output: 移位结果
'''
def oribitMoveBit(varsNum, oribit):
    oribitRes = []
    for i in range(varsNum):
        oribitRes.append(moveBit(oribit, i))
    return oribitRes


'''
    去掉各轨道中重复的输入项
'''
def removedepriate(elementList, List):
    FlagList = []
    for ele in List:
        for elem in elementList:
            if elem in ele:
                FlagList.append(False)
            else:
                FlagList.append(True)
    if False in FlagList:
        return False
    else:
        return True

'''
    创建轨道输入项
'''
def generateOribit(varsNum, truthTable):
    tmpList = [[]]
    depriateFlag = True
    len1 = len(truthTable)
    for i in range(len1):
        oribitTmp = oribitMoveBit(varsNum, truthTable[i])
        depriateFlag = removedepriate(oribitTmp, tmpList)
        if depriateFlag is True:
            tmpList.append(oribitTmp)
    # print(tmpList[1 : ])
    # for ele in tmpList[1 : ]:
    #     print(ele)
    # print(len(tmpList[1 : ]))
    resList = []
    for ele in tmpList[1 : ]:
        tmp = []
        for elem in ele:
            if elem not in tmp:
                tmp.append(elem)
        resList.append(tmp)
    # for ele in resList:
    #     print(ele)
    # print(len(resList))
    return resList
"========================================================================================"
'''
    生成当前轨道数，及各轨道真值表输入
    :return 得到各轨道取值
'''
def finalOribit(varsNum, AlltruthTable):
    resList = generateOribit(varsNum, AlltruthTable)
    # for ele in resList:
    #     print(ele)
    # print(len(resList))
    # print(resList)
    return resList


'''
    根据小项表达式计算多项式该项的值
    :return 返回该项的值
'''
def itemRes(dic_index, dic_value):
    for key in dic_value.keys():
        if dic_value.get(key) != dic_index.get(key):
            return 0
    return 1



'''
    计算九元布尔函数自相关谱
    truthTable: 该布尔函数真值表
    dicIndexList: 该布尔函数的索引值
    :return 返回自相关谱求和结果
'''
def autocorrelationCompute(varsNum, truthTable, dicIndexList, allTable):
    ResList = []
    for ele in allTable:
        ResList.append(abs(autocorrelation(varsNum, ele, truthTable, dicIndexList, allTable)))
    correlationRes = 0
    len1 = len(ResList)
    for i in range(1, len1):
        correlationRes += ResList[i]
    return correlationRes


def autocorrelationSelect(varsNum, truthTable, dicIndexList, allTable):
    return autocorrelationCompute(varsNum, truthTable, dicIndexList, allTable)



'''
    将真值表输入项(真值表2 ** n 长)转化为适合使用的dicIndexList
'''
def truthTableTrans(varsNum, oneNumListEle):
    Dic = {}
    List = []
    num = 0
    for ele in oneNumListEle:
        for elem in ele:
            Dic[num % varsNum] = elem
            num = num + 1
        List.append(copy.deepcopy(Dic))
    return List



'''
    根据输入，求真值表
'''
def midProcess(varsNum, dicIndexList, allTable):
    resList = []
    hang = len(dicIndexList)
    for ele in allTable:
        resTmpList = []
        for i in range(0, hang):
            if list(dicIndexList[i].values())  == ele:
                resTmpList.append(1)
            else:
                resTmpList.append(0)
        resList.append(sum(resTmpList) % 2)
    return resList



'''
    根据当前布尔函数元数求出真值表
'''
def TruthTableSelect(varsNum, dicIndexList, allTable):
   return midProcess(varsNum, dicIndexList, allTable)



'''
    input: 当前布尔函数元数
    oneNumOribitList: 当前输出为1的真值表列表
    OribitList:当前布尔函数的轨道真值表
    
    output: dicIndexList(当前布尔函数对应的索引值)
'''
def initRSBF(varsNum, oneNumOribitList, OribitList):
    # print("该布尔函数轨道总数" ,len(OribitList))
    dicOribit = {}
    len1 = len(OribitList)
    for i in range(len1):
        dicOribit[i + 1] = OribitList[i]

    oneNumList = []
    # print(len(oneNumOribitList))
    # print(oneNumOribitList)
    for ele in oneNumOribitList:
        oneNumList.append(dicOribit[ele])
    # print(oneNumList)

    transList = []
    len2 = len(oneNumList)
    for i in range(len2):
        transList.append(truthTableTrans(varsNum, oneNumList[i]))
    # print(transList)

    indexList = []
    for ele in transList:
        for elem in ele:
            indexList.append(elem)
    return indexList


'''
    获取当前布尔函数的非线性度、透明阶、输出为1索引值的真值表长度
'''
def nonlinearityAndTransparency(varsNum, lst, OribitList, allTable):
    dicIndexList = initRSBF(varsNum, lst, OribitList)

    truthTable = TruthTableSelect(varsNum, dicIndexList, allTable)
    balanceFlag = ""
    if truthTable.count(1) == pow(2, varsNum - 1):
        balanceFlag = "balanced function"
    else:
        balanceFlag = "unbalanced function"
    res1 = nonlinearityCompute(varsNum, truthTable)
    res2 = transparencyCompute(varsNum, truthTable, dicIndexList, allTable)
    # print("nonlinearity = " + str(res1), "  transparency = " + str(res2))
    return res1, res2, balanceFlag


def allin(address):
    count = 0
    tableLst = fileToList1(address)
    minTranparency = 1.0
    for ele in tableLst:
        count += 1
        tmpLst = (nonlinearityAndTransparency(8, ele[0], finalOribit(8, AlltruTable(8)), AlltruTable(8)))
        if tmpLst[1] < minTranparency:
            minTranparency = tmpLst[1]
            print(minTranparency)
        if count == 1000 and count != 0:
            print(count)
    print(address + " " + str(minTranparency))



if __name__ == '__main__':
    # tableLst = fileToList1("116.0_search.txt")
    # minTranparency = 1.0
    # for ele in tableLst:
    #     tmpLst = (nonlinearityAndTransparency(8, ele[0], finalOribit(8, AlltruTable(8)), AlltruTable(8)))
    #     if tmpLst[1] < minTranparency:
    #         minTranparency = tmpLst[1]
    # print(minTranparency)


    # allin("112.0_search.txt")
    # allin("113.0_search.txt")
    allin("114.0_search.txt")
    # allin("115.0_search.txt")



