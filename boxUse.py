from interface import BooleanFunction
from flieToLst import fileToList1

def boxUse(varsNum, boxTable):
    bf = BooleanFunction(varsNum, S_BOX_Table=boxTable)
    nonlinearity = (bf.S_Box_Nonlinearity())
    autoAbsolute = (bf.autoCorrelationMaxAbsolute())
    diff = (bf.differentialUniformValue())
    degree = (bf.sBoxDegree())
    mto = (bf.S_BOX_MTO())
    rto = (bf.S_BOX_RTO())
    with open("correct.txt", mode = "a+", encoding="utf-8") as f:
        f.write(str(boxTable) + "   " + str(nonlinearity) + "   " + autoAbsolute + "    " + str(diff) + "   " + str(degree) + "   " + str(mto) + "    " + str(rto) + "\n")

def makeSence(address):
    tableVec = fileToList1(address)
    len1 = len(tableVec)
    for i in range(len1):
        boxUse(8, tableVec[i][0])

if __name__ == '__main__':
    makeSence("matrix.txt")
