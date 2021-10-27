import copy
import itertools
from scipy.special import comb

def AlltruTable(varsNum):
    TableList = []
    pos = pow(2, varsNum)
    for i in range(0, pos):
        tmp = str(bin(i)).split("0b")
        for elem in tmp:
            if elem == '':
                continue
            tmpList = []
            for element in elem:
                tmpList.append(int(element))
            if len(tmpList) != varsNum:
                len1 = varsNum - len(tmpList)
                for i in range(len1):
                    tmpList.insert(0, 0)
            TableList.append(copy.deepcopy(tmpList))
    return TableList

def computeTerm(varsNum, term, table):
    ret = 1
    for i in range(varsNum):
        if term['x_' + str(i + 1)][0] == True:
            term['x_' + str(i + 1)][1] = table[varsNum - i - 1]
    for i in range(varsNum):
        ret *= term['x_' + str(i + 1)][1]
    return ret



def ANF2TruthTable(varsNum, allTable):
    oneTerm = {}
    for i in range(varsNum):
        oneTerm['x_' + str(i + 1)] = [False, 1]
    # print(oneTerm) # {'x_1': [False, 1], 'x_2': [False, 1], 'x_3': [False, 1]}
    multiptyTermList = []
    while 1:
        termList = input("the term index(split by a space, -1 to finish)[+]:").split(' ')
        if '-1' in termList:
            break
        oneTermList = []
        for ele in termList:
            oneTermList.append(int(ele))
        multiptyTermList.append(copy.deepcopy(oneTermList))
    # print(multiptyTermList) # [[1, 2], [2, 3], [1, 3]]

    multiptyTerm = []
    for one in multiptyTermList:
        tmpTerm = copy.deepcopy(oneTerm)
        for ele in one:
            tmpTerm['x_'+str(ele)] = [True, 1]
        multiptyTerm.append(copy.deepcopy(tmpTerm))
    # print(multiptyTerm) # [{'x_1': [True, 1], 'x_2': [True, 1], 'x_3': [False, 1]}, {'x_1': [False, 1], 'x_2': [True, 1], 'x_3': [True, 1]}, {'x_1': [True, 1], 'x_2': [False, 1], 'x_3': [False, 1]}, {'x_1': [True, 1], 'x_2': [True, 1], 'x_3': [True, 1]}]

    truthTable = []
    for table in allTable:
        oneTermRes = 0
        for term in multiptyTerm:
            oneTermRes += computeTerm(varsNum, term, table)
        truthTable.append(oneTermRes % 2)
    return truthTable


def combines(varsNum):
    lst = []
    ret = []
    for i in range(varsNum):
        lst.append(i + 1)
    for j in range(varsNum + 1):
        for ele in itertools.combinations(lst, j):
            ret.append(list(ele))
    return ret


def sortByEle(lst):
    length = len(lst)
    tmp = []
    for i in range(length - 1):
        for j in range(i + 1, length):
            if len(lst[j]) < len(lst[i]):
                tmp = lst[j]
                lst[j] = lst[i]
                lst[i] = tmp
    return lst


def truTable2ANF(varsNum, binTruthTable, allTable):
    tLst = []
    uLst = []
    for i in range(varsNum):
        for j in range(1, pow(2, varsNum - 1) + 1):
            tLst.append(binTruthTable[2 * (j) - 1 - 1])
            uLst.append((binTruthTable[2 * (j) - 1 - 1] + binTruthTable[2 * (j) - 1]) % 2)
        for ele in uLst:
            tLst.append(ele)
        binTruthTable.clear()
        for ele in tLst:
            binTruthTable.append(ele)
        tLst.clear()
        uLst.clear()

    ANFTable = []
    for i in range(pow(2, varsNum)):
        if binTruthTable[i] == 1:
            tmp = allTable[i]
            tmpLst = []
            for j in range(varsNum):
                if tmp[j] == 1:
                    tmpLst.append(varsNum - j)
            ANFTable.append(copy.deepcopy(sorted(tmpLst)))

    ANFTable = sortByEle(ANFTable)
    ANF = ""
    for ele in ANFTable:
        for elem in ele:
            ANF += "x" + str(elem)
        ANF += " + "
    return ANF[:len(ANF) - 3]


def checkKBalanced(varsNum, truthTable, allTable):
    if truthTable.count(1) != pow(2, varsNum - 1):
        return False
    checkDic = {}
    for i in range(pow(2, varsNum)):
        if allTable[i].count(1) in checkDic.keys():
            checkDic[allTable[i].count(1)].append({str(allTable[i]) : truthTable[i]})
        else:
            checkDic[allTable[i].count(1)] = [{str(allTable[i]) : truthTable[i]}]
    for ele in list(checkDic.values())[1 : len(checkDic.values()) - 1]:
        tmpTable = []
        for elem in ele:
            tmpTable.append(list(elem.values())[0])
        if tmpTable.count(1) != int(comb(varsNum, list(ele[0].keys())[0].count('1')) * 0.5):
            return False
    return True

def strsToSBOXTable(tableStr):
    tmpStr = ""
    for ele in tableStr:
        if ele == "\n":
            continue
        tmpStr += ele

    lst = tmpStr.split(", ")
    retLst = []
    for ele in lst:
        retLst.append(int(ele))
    return (retLst)

if __name__ == '__main__':
    varsNum = int(input("input your function variable[+]: "))
    allTable = AlltruTable(varsNum)
    '''
        代数正规型转二进制真值表
    '''
    table = ANF2TruthTable(varsNum, allTable)
    '''
        二进制真值表转代数正规型
    '''
    print(truTable2ANF(varsNum, table, allTable))
#
#




