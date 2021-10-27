
from truthTable import AlltruTable
from S_BOX_Transparency import  vectorXOR, XOR, shortTableToLong


def MatrixXOR(Matrix1, Matrix2):
    resMatrix = []
    len1 = len(Matrix1)
    len2 = len(Matrix1[0])
    for i in range(len1):
        tmpVec = []
        for j in range(len2):
            tmpVec.append(XOR(Matrix1[i][j], Matrix2[i][j]))
        resMatrix.append(tmpVec)
    return resMatrix


def mulMatAndVec(vec, matrix):
    resVec = []
    len1 = len(matrix[0])
    len2 = len(matrix)
    for i in range(len1):
        tmpValue = 0
        for j in range(len2):
            tmpValue += (vec[j] * matrix[j][i])
        resVec.append(tmpValue % 2)
    return  resVec


def boxMatrixGen(SMatrix, alltruthTable):
    resDic = {}
    len1 = len(alltruthTable)
    for i in range(len1):
        resDic[str(alltruthTable[i])] = []

    len2 = len(SMatrix)
    len3 = len(SMatrix[0])
    for i in range(len2):
        for j in range(len3):
            resDic[str(alltruthTable[j])].append(SMatrix[i][j])
    return resDic


def boxMidOp(SMatrix, allTruthtable):
    truthTableXOR = []
    for ele in allTruthtable[1:]:
        tmpList = []
        for elem in allTruthtable:
            tmpList.append((vectorXOR(ele, elem)))
        truthTableXOR.append((tmpList))

    boxDic = boxMatrixGen(SMatrix, allTruthtable)
    SMatrix2 = []
    for ele in truthTableXOR:
        SMatrixtmp = []
        for elem in ele:
            SMatrixtmp.append(boxDic[str(elem)])
        SMatrix2.append(SMatrixtmp)

    Matrix2 = []
    for ele in SMatrix2:
        tmpLst = []
        for i in range(len(ele[0])):
            tmpList = []
            for elem in ele:
                tmpList.append(elem[i])
            tmpLst.append(tmpList)
        Matrix2.append(tmpLst)

    modOpRes = []
    for ele in Matrix2:
        modOpRes.append(MatrixXOR(ele, SMatrix))

    return modOpRes

def autoCorrelation(SMatrix, uVec, allTruthtable):
    modOpRes = boxMidOp(SMatrix, allTruthtable)

    resVec = []
    for ele in modOpRes:
        resVec.append(mulMatAndVec(uVec, ele))

    resValueList = []
    for ele in resVec:
        value = 0
        for elem in ele:
            if elem == 0:
                value += 1
            elif elem == 1:
                value -= 1
            else:
                print("value error")
        resValueList.append(value)
    return resValueList


def maxAbsolute(varsNum, Matrix, allTruthtable):
    Matrix = shortTableToLong(varsNum, Matrix)

    resList = []
    for ele in allTruthtable[1:]:
        resList.append(autoCorrelation(Matrix, ele, allTruthtable))


    maxValue = 0
    for ele in resList:
        value = max(ele)
        if value > maxValue:
            maxValue = value

    return maxValue




if __name__ == '__main__':
    pass

