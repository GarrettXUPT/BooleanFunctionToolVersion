
import copy
from walsh_and_nonlinearity import walshCompute, nonlinearityCompute
from addDeg import getDegree
from judge import trans, longTableToTable
from nonAbsoluteIndicator import autocorrelation
from truthTable import AlltruTable
from innerproduct import innerProductSelect
from RSBF import TruthTableSelect, finalOribit, initRSBF
from flieToLst import fileToList1



def Eightnon_Auto(varsNum, truthTable, dicIndexList):
    ResList = []
    dicOfa = {"a1": 0, "a2": 0, "a3": 0, "a4" : 0, "a5" : 0, "a6" : 0, "a7" : 0, "a8" : 0}
    for i1 in range(0, 2):
        for i2 in range(0, 2):
            for i3 in range(0, 2):
                for i4 in range(0, 2):
                    for i5 in range(0, 2):
                        for i6 in range(0, 2):
                            for i7 in range(0, 2):
                                for i8 in range(0, 2):
                                    dicOfa["a1"] = i1
                                    dicOfa["a2"] = i2
                                    dicOfa["a3"] = i3
                                    dicOfa["a4"] = i4
                                    dicOfa["a5"] = i5
                                    dicOfa["a6"] = i6
                                    dicOfa["a7"] = i7
                                    dicOfa["a8"] = i8
                                    ResList.append((autocorrelation(varsNum, dicOfa, truthTable, dicIndexList)))
    return ResList

def keySort(FreqDic):
    return sorted(FreqDic.items(), key=lambda d: d[0])

def freqMe(inputLst):
    tmpList = []
    for ele in inputLst:
        tmpList.append(abs(ele))
    FreqDic = {}
    for ele in tmpList:
        if ele in list(FreqDic.keys()):
            FreqDic[(ele)] += 1
        else:
            FreqDic[(ele)] = 1
    FreqDic = keySort(FreqDic)
    return FreqDic


def WHTDistrubution(varsNum, truthtable):
    walsh = walshCompute(varsNum, truthtable)
    return freqMe(walsh)


def ACDistrubution(varsNum, truthTable, dicIndexList):
    autocorrelation = Eightnon_Auto(varsNum, truthTable, dicIndexList)
    return freqMe(autocorrelation)

def maxAuto(varsNum, truthTable, dicIndexList):
    autocorrelation = Eightnon_Auto(varsNum, truthTable, dicIndexList)
    return max(autocorrelation[1:])


def basicDis(varsNum, longTable1, longTable2, alltruthTable):
    indexDicList1 = trans(varsNum, longTable1, alltruthTable)
    indexDicList2 = trans(varsNum, longTable2, alltruthTable)
    if WHTDistrubution(varsNum, longTable1) == WHTDistrubution(varsNum, longTable2) \
        and ACDistrubution(varsNum, longTable1, indexDicList1) == ACDistrubution(varsNum, longTable2, indexDicList2) \
            and maxAuto(varsNum, longTable1, indexDicList1) == maxAuto(varsNum, longTable2, indexDicList2) \
            and nonlinearityCompute(varsNum, longTable1, ) == nonlinearityCompute(varsNum, longTable2) \
            and getDegree(longTable1, alltruthTable) == getDegree(longTable2, alltruthTable):
        return True
    return False

def RSBF2TruthTable(varsNum, oneNumList, OribitList, alltruthTable):
    dicIndexList = initRSBF(varsNum, oneNumList, OribitList)
    truthTable = TruthTableSelect(varsNum, dicIndexList, alltruthTable)
    return truthTable

def divClass(varsNum):
    # checkLst = fileToList1("class1.txt")
    # checkPos = checkLst[0][0]
    allLst = fileToList1("divData/116/116_1.txt")
    alltruthTable = AlltruTable(varsNum)
    OribitList = finalOribit(varsNum, alltruthTable)
    innerList = innerProductSelect(alltruthTable)

    with open("class1.txt", mode="a+", encoding="utf-8") as f:
        f.write(str(allLst[0][0]) + str(allLst[0][1]) + "\n")

    len1 = len(allLst)
    for i in range(1, len1):
        truthTable1 = RSBF2TruthTable(varsNum, allLst[0][0], OribitList, alltruthTable)
        truthTable2 = RSBF2TruthTable(varsNum, allLst[i][0], OribitList, alltruthTable)
        if basicDis(varsNum, truthTable1, truthTable2, alltruthTable) == True:
            with open("class1.txt", mode="a+", encoding="utf-8") as f:
                f.write(str(allLst[i][0]) + "  "  + str(allLst[i][1]) + "\n")
        else:
            with open("tmpFile1.txt", mode="a+", encoding="utf-8") as f:
                f.write(str(allLst[i][0]) + "  " + str(allLst[i][1]) + "\n")

def findEqValue(longTable1, longTable2, alltruthTable):
    resLst = []
    for i in range(len(alltruthTable)):
        iconnect = connectFunction(longTable2, alltruthTable[i])
        if basicDis(longTable1, iconnect, alltruthTable) == True:
            resLst.append(i)
    return resLst



def vecToint(lst):
    length = len(lst)
    value = 0
    for i in range(length):
        value += pow(2, length - i - 1) * lst[i]
    return value

def intTovec(varsNum, val):
    strs = str(bin(val))
    tmp = strs.split("b")[1]
    resLst = []
    for ele in tmp:
        resLst.append(int(ele))
    count = varsNum - len(resLst)
    while count > 0:
        resLst.insert(0, 0)
        count -= 1
    return resLst


def connectFunction(longTable, iLst):
    resLst = []
    for ele in longTable:
        resLst.append((ele + 1) % 2)
    resLst[vecToint(iLst)] = (resLst[vecToint(iLst)] + 1) % 2
    return resLst


def getEk(varsNum, k):
    resLst = []
    for i in range(varsNum):
        if varsNum - i== k:
            resLst.append(1)
            continue
        resLst.append(0)
    return resLst

def getPossiableMatrix(varsNum, longTable1, longTable2, alltruthTable):
    resList = []
    for i in range(varsNum):
        g = connectFunction(longTable2, getEk(varsNum, i + 1))
        tmpLst = findEqValue(g, longTable1, alltruthTable)
        print(tmpLst)
        resList.insert(0, tmpLst)


# [1, 25, 152, 161, 199, 207, 208, 211]
# [41, 50, 68, 91, 97, 117, 228, 244]
# [44, 63, 77, 89, 100, 123, 159, 173]
# [26, 29, 74, 127, 144, 182, 200, 246]
# [43, 51, 139, 178, 229, 237, 249, 250]
# [9, 13, 112, 119, 128, 143, 204, 234]
# [26, 29, 74, 127, 144, 182, 200, 246]
# [52, 59, 116, 120, 147, 151, 195, 238]

def matMulVec(matT, vec):
    resLst = []
    for i in range(len(matT[0])):
        value = 0
        for j in range(len(matT)):
            value += (vec[j] * matT[j][i])
        resLst.append(value % 2)
    return resLst


def tryToConfirm(varsNum):
    possiableMatrix = [[1, 25, 152, 161, 199, 207, 208, 211], [41, 50, 68, 91, 97, 117, 228, 244], [44, 63, 77, 89, 100, 123, 159, 173], [26, 29, 74, 127, 144, 182, 200, 246], [43, 51, 139, 178, 229, 237, 249, 250], [9, 13, 112, 119, 128, 143, 204, 234], [26, 29, 74, 127, 144, 182, 200, 246], [52, 59, 116, 120, 147, 151, 195, 238]]
    possiableMatrix.reverse()
    resMatrix =[]
    matrix = []
    for i in range(varsNum):
        for j in range(varsNum):
            for k in range(varsNum):
                for n in range(varsNum):
                    for q in range(varsNum):
                        for w in range(varsNum):
                            for e in range(varsNum):
                                for r in range(varsNum):
                                    matrix.append(possiableMatrix[0][i])
                                    matrix.append(possiableMatrix[1][j])
                                    matrix.append(possiableMatrix[2][k])
                                    matrix.append(possiableMatrix[3][n])
                                    matrix.append(possiableMatrix[4][q])
                                    matrix.append(possiableMatrix[5][w])
                                    matrix.append(possiableMatrix[6][e])
                                    matrix.append(possiableMatrix[7][r])

    tmpLst = []
    for i in range(len(matrix)):
        if i % 8 == 0 and i != 0 or i == len(matrix) - 1:
            resMatrix.append(copy.deepcopy(tmpLst))
            tmpLst.clear()
        tmpLst.append(matrix[i])
    # print(resMatrix[0])
    # print(len(resMatrix))
    # '''
    #     固定该矩阵
    # '''
    # count = 0
    # for mat in resMatrix:
    #     flag = True
    #     tmpMat = []
    #     for ele in mat:
    #         tmpMat.append(intTovec(varsNum, ele))
    #     for i in range(varsNum):
    #         left = matMulVec(tmpMat, intTovec(varsNum, pow(2, varsNum - i - 1)))
    #         right = tmpMat[i]
    #         if left != right:
    #             flag = False
    #             break
    #     if flag == True:
    #         count += 1
    # print(count)
    return resMatrix

def vecMul(vec1, vec2):
    value = 0
    for i in range(len(vec1)):
        value += (vec1[i] * vec2[i])
    return value % 2

def XinnerproductB(alltruthTable):
    resLst = []
    for eleb in alltruthTable:
        tmpLst = []
        for elemx in alltruthTable:
            tmpLst.append(vecMul(eleb, elemx))
        resLst.append(copy.deepcopy(tmpLst))
    return resLst

def vecAdd(vec1, vec2):
    resLst = []
    for i in range(len(vec1)):
        resLst.append((vec1[i] + vec2[i]) % 2)
    return resLst

def vecAddOne(vec):
    resLst = []
    for ele in vec:
        resLst.append((ele + 1) % 2)
    return resLst

def longTableTrans(longTable, alltruthTale, Matrix, xinnerB):
    checkDic = {}
    for i in range(len(alltruthTale)):
        checkDic[str(alltruthTale[i])] = longTable[i]

    newInputLst = []
    for i in range(len(alltruthTale)):
        newInputLst.append(matMulVec(Matrix, alltruthTale[i]))

    newTable = []
    for ele in newInputLst:
        newTable.append(checkDic[str(ele)])

    '''
        c = 0 and c = 1
    '''
    newTableLst = []
    for ele in xinnerB:
        newTableLst.append(vecAdd(ele, newTable))
        newTableLst.append(vecAdd(ele, vecAddOne(newTable)))
    return newTableLst


'''
    在a = 0时 查询是否有矩阵可以造成仿射变换
'''
def test():
    varsNum = 8
    tableStr1 = "B7763690E67B728DC85ED3515FD2D516AD576003084DBD08205E24F69CB578F2"
    tableStr2 = "BE3FCA32BE0075DE5EF681E97A3258672D612CCF74D0A256951B572902E90E13"
    alltruthTable = AlltruTable(varsNum)
    longTable1 = longTableToTable(tableStr1)
    longTable2 = longTableToTable(tableStr2)

    resMatrix = tryToConfirm(varsNum)
    xinnerb = XinnerproductB(alltruthTable)
    print(len(resMatrix))
    for mat in resMatrix:
        tmpMat = []
        for elems in mat:
            tmpMat.append(intTovec(varsNum, elems))
        for ele in longTableTrans(longTable1, alltruthTable, tmpMat, xinnerb):
            if ele == longTable2:
                print(mat)
                return


if __name__ == '__main__':
    # varsNum = 8
    # alltruthTable = AlltruTable(varsNum)
    # innerPro = innerProductSelect(alltruthTable)
    # tableStr1 = "B7763690E67B728DC85ED3515FD2D516AD576003084DBD08205E24F69CB578F2"
    # tableStr2 = "BE3FCA32BE0075DE5EF681E97A3258672D612CCF74D0A256951B572902E90E13"
    # longTable1 = longTableToTable(tableStr1)
    # longTable2 = longTableToTable(tableStr2)
    # print(basicDis(varsNum, longTable1, longTable2, alltruthTable, innerPro))
    #
    divClass(8)


