
from truthTable import AlltruTable
from autocorrelation import boxMidOp
from S_BOX_Transparency import shortTableToLong

def uniform(varsNum, SMatix, alltruthTable):
    SMatix = shortTableToLong(varsNum, SMatix)
    midOpRes = boxMidOp(SMatix, alltruthTable)
    countList = []

    for element in alltruthTable:
        for ele in midOpRes:
            count = 0
            for i in range(len(ele[0])):
                tmpList = []
                for j in range(len(ele)):
                    tmpList.append(ele[j][i])
                if tmpList == element:
                        count += 1
            countList.append(count)
    return max(countList)


if __name__ == '__main__':
    pass