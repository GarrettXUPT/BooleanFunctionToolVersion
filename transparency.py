

'''
    按当前布尔函数元数进行模加选择
'''
def variableAddMol(varsNum, listOfa, allTable):
    resList = []
    for ele in allTable:
        for i in range(varsNum):
            resList.append((listOfa[i] + ele[i]) % 2)
    return resList


'''
    自相关谱的计算
    :return 自相关谱累加计算结果
'''
def autocorrelation(varsNum, dicOfa, truthTable, dicIndexList, allTable):

    valueList = []
    for ele in dicIndexList:
        valueList.append(list(ele.values()))

    addModList = variableAddMol(varsNum, dicOfa, allTable)
    addResListTmp = []
    addResList = []
    pos = pow(2, varsNum)
    for i in range(pos):
        addResListTmp.append(addModList[0 + varsNum * i : varsNum + varsNum * i])

    len1 = len(addResListTmp)
    for i in range(len1):
        for ele in valueList:
            if ele == addResListTmp[i]:
                addResListTmp[i] = "vaild"

    for ele in addResListTmp:
        if ele == "vaild":
            addResList.append(1)
        else:
            addResList.append(0)
    # print(addResList)  # [1, 0, 0, 0, 0, 1, 0, 1]

    indexAddResList = truthAdd(truthTable, addResList)
    ResTmpList = []
    for ele in indexAddResList:
        if ele == 0:
            ResTmpList.append(1)
        else:
            ResTmpList.append(-1)

    Res = 0
    for ele in ResTmpList:
        Res = ele + Res
    return Res

# '''
#     计算真值表及小项表示指数
#     :return 返回计算结果
# '''
# def truthTableAndIndexLixt(varsNum):
#     dicIndexList = []
#     truthTable = truthTableSelect(varsNum, dicIndexList)
#     return truthTable, dicIndexList

'''
    计算自相关谱指数部分 f(x) + f(x + d)
    :return 计算结果
    
'''
def truthAdd(truthTable, addResList):
    ResList = []
    len1 = len(truthTable)
    for i in range(len1):
        ResList.append((truthTable[i] + addResList[i]) % 2)
    return ResList

'''
    三元透明阶的计算
    :return 返回计算结果
'''

def TransparencyComputeProcess(varsNum, truthTable, dicIndexList, allTable):
    ResList = []
    for ele in allTable:
        ResList.append(abs(autocorrelation(varsNum, ele, truthTable, dicIndexList, allTable)))
    correlationRes = 0
    len1 = len(ResList)
    for i in range(1, len1):
        correlationRes = ResList[i] + correlationRes
    # print(correlationRes)
    tmp = 1 /(pow(2, varsNum) * (pow(2, varsNum) - 1))
    res = 1 - tmp * correlationRes
    # print(res)
    return res

'''
    透明阶计算选择
    根据传入当前布尔函数元数，选择透明阶计算函数
'''
def transparencyCompute(varsNum, truthTable, dicIndexList, allTable):
    return TransparencyComputeProcess(varsNum, truthTable, dicIndexList, allTable)


if __name__ == '__main__':
    pass











