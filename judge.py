
import copy
import time
from truthTable import AlltruTable
from S_Box_nonlinearity import hexToBinary
from walsh_and_nonlinearity import nonlinearityCompute
from transparency import transparencyCompute
from truthTable import AlltruTable
from RSBF import finalOribit, initRSBF
from innerproduct import innerProductSelect



def trans(varsNum, truthTable, AlltruthTable):
    # print(truthTable)
    oneNumList = []
    len1 = len(truthTable)
    for i in range(len1):
        if truthTable[i] == 1:
            oneNumList.append(i)
    # print(oneNumList)
    # print(len(oneNumList))
    oneNumDic = {}
    for ele in oneNumList:
        oneNumDic[ele] = AlltruthTable[ele]

    resTmpList = []
    for k, ele in oneNumDic.items():
        resTmpList.append(ele)
    # print(resTmpList)

    Dic = {}
    List = []
    num = 0
    for ele in resTmpList:
        for elem in ele:
            Dic[num % varsNum] = elem
            num = num + 1
        List.append(copy.deepcopy(Dic))
    # print(List)
    return List


'''
    十六进制表真值表转换为二进制长表
'''
def longTableToTable(tableStr):
    resStr = ""
    for ele in tableStr:
        resStr = resStr + ele + " "
    # print(resStr)
    tmpList = resStr.split(" ")
    tmpList.pop()
    binaryListTmp = hexToBinary(tmpList)
    binaryList = []
    for ele in binaryListTmp:
        for elem in ele:
            binaryList.append(elem)
    # print(binaryList)
    return binaryList

'''
    由二进制长表判断该函数是否为旋转对称布尔函数
'''
def isRotationSymmetric(varsNum, truthTable, AlltruthTable, oribitList):
    nineTable = AlltruthTable
    shortTableOribitList = []
    len2 = len(nineTable)
    for ele in oribitList:
        tmpList = []
        for i in range(len2):
            if nineTable[i] in ele:
                tmpList.append(i)
        shortTableOribitList.append(copy.deepcopy(tmpList))

    TableOribitList = []
    for ele in shortTableOribitList:
        tmpList = []
        for elem in ele:
            tmpList.append(truthTable[elem])
        TableOribitList.append(copy.deepcopy(tmpList))

    '''
        判断是否为旋转对称布尔函数
    '''
    FlagList = []
    for ele in TableOribitList:
        if ele.count(0) == len(ele) or ele.count(1) == len(ele):
            FlagList.append(True)
        else:
            FlagList.append(False)


    '''
        此处可获得短表
    '''
    shortList = []
    len1 = len(TableOribitList)
    for i in range(len1):
        if TableOribitList[i].count(1) == len(TableOribitList[i]):
            shortList.append(i + 1)
    # print(shortList)


    if FlagList.count(True) == len1:
        return "Rotation Symmetric Prove"
    else:
        return "The function is not Rotation Symmetric"




if __name__ == '__main__':
    pass
