
import time, copy
from addDeg import getDegree
from truthTable import AlltruTable

def XOR(ele1, ele2):
    return (ele1 + ele2) % 2


def vectorXOR(vec1, vec2):
    resLst = []
    len1 = len(vec1)
    for i in range(len1):
        resLst.append(XOR(vec1[i], vec2[i]))
    return resLst

def vectorXORes(vec1, vec2):
    res = 0
    len1 = len(vec1)
    for i in range(len1):
        tmp = XOR(vec1[i], vec2[i])
        if tmp == 0:
            res += 1
        elif tmp == 1:
            res -= 1
        else:
            print("value error")
    return res


def firstTerm(truthTable1):
    return truthTable1


def truthTableDicGen(truthTable, alltruthTable):
    truthTableDic = {}
    len1 = len(alltruthTable)
    for i in range(len1):
        truthTableDic[str(alltruthTable[i])] = truthTable[i]
    return truthTableDic


def secondTerm(truthTable2, alltruthTable, truthTableXOR):
    truthTableDic = truthTableDicGen(truthTable2, alltruthTable)
    putLst = []
    len1 = len(alltruthTable)
    for i in range(len1):
        putLst.append(truthTableDic[str(truthTableXOR[i])])
    return putLst


def correlation(truthTable1, truthTable2, alltruthTable, truthTableXOR):
    first = firstTerm(truthTable1)
    second = secondTerm(truthTable2, alltruthTable, truthTableXOR)
    res = vectorXORes(first, second)
    return res


def betaOp(beta):
    resLst = []
    for ele in beta:
        for elem in beta:
            if XOR(ele, elem) == 1:
                resLst.append(-1)
            elif XOR(ele, elem) == 0:
                resLst.append(1)
    return resLst



def sumTermRTO(beta, SMatrix, alltruthTable, truthTableXOR):
    sumRes = 0
    for i in range(len(SMatrix)):
        for j in range(len(SMatrix)):
            sumRes += (correlation(SMatrix[i], SMatrix[j], alltruthTable, truthTableXOR) * beta[i * len(SMatrix) + j])
    return abs(sumRes)


def sumTermMTO(beta, SMatrix, alltruthTable, truthTableXOR):
    sumRes = 0
    for i in range(len(SMatrix)):
        sumTerm = 0
        for j in range(len(SMatrix)):
            sumTerm += (correlation(SMatrix[i], SMatrix[j], alltruthTable, truthTableXOR) * beta[i * len(SMatrix) + j])
        sumRes += abs((sumTerm))
    return sumRes


def revisedTO(varsNum, SMatrix):
    truthTableXOR = []
    allTruthtable = AlltruTable(varsNum)

    for ele in allTruthtable[1:]:
        tmpList = []
        for elem in allTruthtable:
            tmpList.append((vectorXOR(ele, elem)))
        truthTableXOR.append((tmpList))

    betaList = []
    for ele in allTruthtable:
        betaList.append(betaOp(ele))

    maxValue = 0
    for j in (range(len(allTruthtable))):
        sumTerm = 0
        for i in range(len(allTruthtable[1:])):
            sumTerm += (sumTermRTO(betaList[j], SMatrix, allTruthtable, truthTableXOR[i]))
        tmpValue = (varsNum - ((1 / ((pow(2, 2 * varsNum) - pow(2, varsNum)))) * sumTerm))
        if  tmpValue > maxValue:
            maxValue = tmpValue

    return maxValue



def modifyMTO(varsNum, SMatrix):
    truthTableXOR = []
    allTruthtable = AlltruTable(varsNum)

    for ele in allTruthtable[1:]:
        tmpList = []
        for elem in allTruthtable:
            tmpList.append((vectorXOR(ele, elem)))
        truthTableXOR.append((tmpList))

    betaList = []
    for ele in allTruthtable:
        betaList.append(betaOp(ele))

    maxValue = 0
    for j in (range(len(allTruthtable))):
        sumTerm = 0
        for i in range(len(allTruthtable[1:])):
            sumTerm += sumTermMTO(betaList[j], SMatrix, allTruthtable, truthTableXOR[i])
        tmpValue = (varsNum - ((1 / ((pow(2, 2 * varsNum) - pow(2, varsNum)))) * sumTerm))
        if tmpValue > maxValue:
            maxValue = tmpValue

    return maxValue


def shortTableToLong(varsNum, shortTable):
    '''
        数字转字符串
    '''
    shortTableStr = []
    for ele in shortTable:
        shortTableStr.append(str(ele))

    '''
        短表转二进制
    '''
    binLst = []
    for ele in shortTableStr:
        tmp = bin(int(ele))[2 : ]
        if len(tmp) != varsNum:
            for i in range(varsNum - len(tmp)):
                tmp = '0' + tmp
        binLst.append(tmp)

    truthTableLst = []
    for i in range(varsNum):
        tmpLst = []
        for ele in binLst:
            tmpLst.append(int(ele[i]))
        truthTableLst.append(tmpLst)

    return truthTableLst


def boxDegree(varsNum, SMatrix, alltruthTable):
    SMatrix = shortTableToLong(varsNum, SMatrix)
    degMin = varsNum
    for ele in SMatrix:
        deg = getDegree(ele, alltruthTable)
        if deg < degMin:
            degMin = deg
    return degMin

if __name__ == '__main__':
    pass



