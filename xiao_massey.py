
from walsh_and_nonlinearity import walshCompute

def oneNumStaticGen(varsNum):
    oneNumStatic = {}
    for i in range(varsNum + 1):
        oneNumStatic[i] = 0
    return oneNumStatic

def xiao_messay(varsNum, TruthTable, allTruthTable):
    oneNumStatic = oneNumStaticGen(varsNum)
    for ele in allTruthTable:
        num = ele.count(1)
        oneNumStatic[num] =  oneNumStatic[num] + 1

    walshVec = walshCompute(varsNum, TruthTable)

    zeroVec = []
    len1 = len(walshVec)
    for i in range(len1):
        if walshVec[i] == 0:
            zeroVec.append(i)

    truthTableVec = []
    for ele in zeroVec:
        truthTableVec.append(allTruthTable[ele].count(1))
    # print(oneNumStatic)
    # print(truthTableVec)
    oneNumStatic.pop(0)
    autoDeg = 0
    item = oneNumStatic.items()
    for k, v in item:
        if truthTableVec.count(k) == v:
            autoDeg = k
        else:
            break
    return autoDeg


if __name__ == '__main__':
    pass

