
import copy
import numpy as np
'''
    此为验证程序
'''

def correctTruthTable(address):
    lstTmp1 = []
    lstTmp2 = []
    lstTmp3 = []
    lstTmp4 = []
    with open(address, mode="r+", encoding="utf-8") as f:
        lstTmp1.append(f.read())
    for ele in lstTmp1:
        # print(ele)
        lstTmp2 = ele.split(" \n")
        for elem in lstTmp2:
            lstTmp3 = elem.split("\n")
    for element in lstTmp3:
        if len(element) == 1:
            lstTmp4.append(int(element))
    # print(lstTmp4)
    return lstTmp4

def itemTransToList(baseNumStrList):
    itemDic = {}
    for ele in baseNumStrList:
        if ele == "1":
            itemDic['x1'] = 1
        elif ele == "2":
            itemDic['x2'] = 1
        elif ele == "3":
            itemDic['x3'] = 1
        elif ele == "4":
            itemDic['x4'] = 1
        elif ele == "5":
            itemDic['x5'] = 1
        elif ele == "6":
            itemDic['x6'] = 1
        elif ele == "7":
            itemDic['x7'] = 1
        elif ele == "8":
            itemDic['x8'] = 1
    return itemDic

def itemRes(itemDic):
    valueList = list(itemDic.values())
    if 0 in valueList:
        return 0
    else:
        return 1

def itemAllRes(itemDic):
    itemDicTmp = copy.deepcopy(itemDic)
    resList = []
    for i1 in range(2):
        for i2 in range(2):
            for i3 in range(2):
                for i4 in range(2):
                    for i5 in range(2):
                        for i6 in range(2):
                            for i7 in range(2):
                                for i8 in range(2):
                                    itemDicRes = {}
                                    itemDicTmp['x8'] = i1
                                    itemDicTmp['x7'] = i2
                                    itemDicTmp['x6'] = i3
                                    itemDicTmp['x5'] = i4
                                    itemDicTmp['x4'] = i5
                                    itemDicTmp['x3'] = i6
                                    itemDicTmp['x2'] = i7
                                    itemDicTmp['x1'] = i8
                                    for k in itemDic.keys():
                                        if k in itemDicTmp.keys():
                                            itemDicRes[k] = copy.deepcopy(itemDicTmp[k])
                                    res = itemRes(itemDicRes)
                                    resList.append(copy.deepcopy(itemRes(itemDicRes)))
    return resList

def itemInput(varsNum, address1, address2):
    # itemNum = int(input("请输入多项式项数："))
    itemsList = []
    itemAllResList = []
    truthTableResTmpList = []
    truthTableResList = []
    for i in range(pow(2, varsNum)):
        truthTableResTmpList.append(0)


    # for i in range(itemNum):
    #     baseNumStr = input("请输入该项底数：")
    #     baseNumStrList = baseNumStr.split(" ")
    #     itemsList.append(itemTransToList(baseNumStrList))
    # print(itemsList)

    tmp1 = address1.split("_")
    tmp2 = tmp1[1].split(".")

    plus = int(tmp2[0])
    tmpList = []

    with open(address1, mode="r+", encoding="utf-8") as f:
        tmpList.append(f.read())

    lst1 = []
    for ele in tmpList:
        lst1 = ele.split(",\n")

    lst2 = []
    for ele in lst1:
        lst2.append(ele.split(" "))

    for ele in lst2:
        itemsList.append(itemTransToList(ele))
    # print(len(lst2))
    # # print(itemsList)
    for ele in itemsList:
        itemAllResList.append(itemAllRes(ele))

    for ele in itemAllResList:
        truthTableResTmpList = np.array(ele) + np.array(truthTableResTmpList)

    for ele in truthTableResTmpList:
        truthTableResList.append((ele + plus) % 2)

    correctList = correctTruthTable(address2)
    # print(correctList)
    correct = ""
    if correctList == truthTableResList:
        correct = "poly correct"
        print(correct)
    else:
        correct = "poly fail"
        print(correct)

    # print(truthTableResList)
    with open("check.txt", mode = "a+", encoding = "utf-8") as f1:
        f1.write("\n\n" + tmp1[0] + " compute res = " + str(truthTableResList))
        f1.write("\n" + tmp1[0] + " correct res = " + str(correctList))
        f1.write("\n" + correct)





if __name__ == '__main__':
    '''修改处，修改地址即可，无需改变其他代码'''
    address1 = "y0_1.txt"  # 多项式文件地址
    address2 = "res0_correct.txt"  # 由excel得到的正确正值表地址
    itemInput(8, address1, address2)

















