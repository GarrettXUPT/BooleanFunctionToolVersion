import sys
import copy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from interface import BooleanFunction
from S_Box_nonlinearity import translateHex
from truthTable import ANF2TruthTable, AlltruTable, strsToSBOXTable


class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


mutl = 2

class Form(QWidget):
    ANF2Table = []
    checkBoxLst = []

    def __init__(self):
        super(QWidget, self).__init__()
        self.setStyleSheet("sources/a.jpg")
        self.setAutoFillBackground(True)

        self.setWindowIcon(QIcon('sources/b.jpg'))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Background, QBrush(QPixmap("sources/a.jpg")))
        self.setPalette(palette1)
        # 将窗口的大小固定
        self.setWindowTitle("boolean function@shiyu")
        self.setFixedSize(400 * mutl, 300* mutl)

        self.btn1 = QPushButton("nonlinearity", self)
        self.btnSet(self.btn1, 5, 30* mutl)
        self.btn1.setFixedWidth(self.btn1.width() - 10)

        self.btn2 = QPushButton('transparency', self)
        self.btnSet(self.btn2, 100* mutl + 10, 30* mutl)
        self.btn2.setFixedWidth(self.btn1.width() - 10)

        self.btn3 = QPushButton('degree', self)
        self.btnSet(self.btn3, 200* mutl + 5, 30* mutl)
        self.btn3.setFixedWidth(self.btn1.width() - 10)


        self.btn4 = QPushButton('absolute indicator', self)
        self.btnSet(self.btn4, 300* mutl + 5, 30* mutl)
        self.btn4.setFixedWidth(self.btn1.width() - 10)


        self.btn5 = QPushButton('isBalanced',self)
        self.btnSet(self.btn5, (50 + 110)* mutl, 55* mutl)

        self.btn7 = QPushButton('differential uniformity', self)
        self.btnSet(self.btn7, (50) * mutl, 55 * mutl)

        self.btn6 = QPushButton('relisent',self)
        self.btnSet(self.btn6, (250 + 20)* mutl, 55* mutl)

        self.btn1.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.btn2.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.btn3.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.btn4.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.btn5.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.btn6.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.btn7.setFont(QFont("微软雅黑", 13, QFont.Bold))

        self.btn1.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')
        self.btn2.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')
        self.btn3.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')
        self.btn4.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')
        self.btn5.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')
        self.btn6.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')
        self.btn7.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')




        self.edit = QLineEdit("boolean Function table space", self)
        self.setEdit(self.edit, 0* mutl, 80* mutl + 20)
        self.edit.resize(200* mutl, 85* mutl)
        self.edit.setMaxLength(pow(2, 30))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Base, QBrush(QPixmap("./a.jpg")))
        self.edit.setPalette(palette2)
        self.edit.setStyleSheet("color:white")
        self.edit.setFont(QFont("微软雅黑", 10, QFont.Bold))

        self.edit1 = QLineEdit("S BOX table space", self)
        self.edit.move(0, 160 * mutl + 20)
        self.setEdit(self.edit1, 0 * mutl, 80 * mutl)
        self.edit1.resize(200 * mutl, 85 * mutl)
        self.edit1.setMaxLength(pow(2, 30))
        palette3 = QPalette()
        palette3.setBrush(QPalette.Base, QBrush(QPixmap("./a.jpg")))
        self.edit1.setPalette(palette3)
        self.edit1.setStyleSheet("color:white")
        self.edit1.setFont(QFont("微软雅黑", 10, QFont.Bold))



        self.variable = QLineEdit(self)
        self.variable.setText("n")
        self.variable.setTextMargins(5* mutl,0,5* mutl,0)
        self.setEdit(self.variable, 60* mutl, 10* mutl)
        self.variable.resize(30* mutl, 15* mutl)
        self.variable.move(160, 20)
        self.variable.setFont(QFont("微软雅黑", 13, QFont.Bold))


        self.process = QTextEdit(self, readOnly = True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(150* mutl)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setFixedWidth(200* mutl)
        self.process.setFixedHeight(175* mutl)
        self.process.move(200* mutl, 80* mutl)
        self.process.setFont(QFont("微软雅黑", 10, QFont.Bold))
        self.process.setStyleSheet("color:white")
        palette3 = QPalette()
        palette3.setBrush(QPalette.Base, QBrush(QPixmap("./a.jpg")))
        self.process.setPalette(palette3)


        sys.stdout = Stream(newText=self.onUpdateText)

        self.checkBox2 = QCheckBox("binary", self)
        self.checkBox2.move(135* mutl, 10* mutl)
        self.checkBox2.stateChanged.connect(self.fixTypeButton)
        self.checkBoxLst.append(self.checkBox2)

        self.checkBox3 = QCheckBox("Hex", self)
        self.checkBox3.move(200* mutl, 10* mutl)
        self.checkBox3.stateChanged.connect(self.fixTypeButton)
        self.checkBoxLst.append(self.checkBox3)

        self.checkBox4 = QCheckBox("ANF", self)
        self.checkBox4.move(255* mutl, 10* mutl)
        self.checkBox4.stateChanged.connect(self.fixTypeButton)
        self.checkBoxLst.append(self.checkBox4)

        self.checkBox5 = QCheckBox("S BOX", self)
        self.checkBox5.move(25 * mutl, 10 * mutl)
        self.checkBox5.stateChanged.connect(self.fixTypeButton)
        self.checkBoxLst.append(self.checkBox5)

        self.checkBox2.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.checkBox2.setStyleSheet("color:white")

        self.checkBox3.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.checkBox3.setStyleSheet("color:white")

        self.checkBox4.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.checkBox4.setStyleSheet("color:white")

        self.checkBox5.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.checkBox5.setStyleSheet("color:white")



        self.reset = QPushButton("reset", self)
        self.reset.resize(50* mutl, 20* mutl)
        self.reset.move(320* mutl, 5* mutl)
        self.reset.toggle()
        self.reset.clicked.connect(self.resetButton)
        self.reset.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.reset.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')

        self.clearbtn = QPushButton("Clear All", self)
        self.clearbtn.setDefault(True)
        self.clearbtn.resize(100* mutl, 20* mutl)
        self.clearbtn.move(50* mutl, 260* mutl)
        self.clearbtn.clicked.connect(self.clearTable)
        self.clearbtn.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.clearbtn.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')



        self.clearbtn = QPushButton("Clear Terminal", self)
        self.clearbtn.setDefault(True)
        self.clearbtn.resize(100* mutl, 20* mutl)
        self.clearbtn.move(250* mutl, 260* mutl)
        self.clearbtn.clicked.connect(self.clearTerminal)
        self.clearbtn.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.clearbtn.setStyleSheet('color: white; border-radius: 10px; border: 2px groove white;')





    # def printTermial(self):
    #     print(self.edit.text())

    def fixTypeButton(self):
        pos = -1
        for i in range(len(self.checkBoxLst)):
            if self.checkBoxLst[i].isChecked():
                pos = i

        if pos != -1:
            for i in range(len(self.checkBoxLst)):
                if i != pos:
                    self.checkBoxLst[i].setCheckable(False)
        print("check")
        # if pos == len(self.checkBoxLst) - 1:
        #     self.ANF2Table = ANF2TruthTable(self.variable, AlltruTable(self.variable))

    def clearTable(self):
        self.edit.setText("")
        self.variable.setText("n")
        self.edit1.setText("")

    def clearTerminal(self):
        self.process.setText("")

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()


    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()


    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)


    def resetButton(self):
        for ele in self.checkBoxLst:
            ele.setChecked(False)
            ele.setCheckable(True)
        print("Truth table type reseted")



    def tableTypeSet(self):
        pass


    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)


    def setEdit(self, edit, x, y):
        edit.setGeometry(x, y, 200* mutl, 200* mutl)

    def btnSet(self, btn, x, y):
        # 创建按钮1
        # setCheckable()：设置按钮是否已经被选中，如果为True，则表示按钮将保持已点击和释放状态
        btn.setDefault(True)
        # toggle()：在按钮状态之间进行切换
        btn.toggle()
        # 点击信号与槽函数进行连接，这一步实现：在控制台输出被点击的按钮
        # btn.clicked.connect(lambda: self.whichBoxBtn(btn))
        btn.clicked.connect(lambda: self.switchBtn(btn))

        # btn.clicked.connect(self.printTermial)
        # 点击信号与槽函数进行连接，实现的目的：输入安妞的当前状态，按下还是释放
        # btn.clicked.connect(self.btnstate)
        # 设置按钮的大小
        btn.setFixedSize(100* mutl, 20* mutl)
        btn.setGeometry(x, y, btn.width(), btn.height())


    def btnstate(self):
        #isChecked()：判断按钮的状态，返回值为True或False
        if self.btn1.isChecked():
            print('button pressed')
        else:
            print('button released')

    def binStrToHexLst(self, strList):
        resLst = []
        tmpLst = []
        count = 0
        for ele in self.edit.text():
            if ele.isdigit():
                tmpLst.append(int(ele))
                count += 1
            if count == 4:
                resLst.append(copy.deepcopy(tmpLst))
                tmpLst.clear()
                count = 0
        hex = ""
        for ele in resLst:
            hex += translateHex(ele)
        return hex

    def switchBtn(self, btn):
        if self.checkBoxLst[-1].isChecked():
            self.whichBoxBtn(btn)
        else:
            self.whichbtn(btn)

    def whichbtn(self, btn):
        #输出被点击的按钮
        if self.variable.text() == 'n' or not self.variable.text().isdigit():
            print("please enter n-variable")
            return
        var = int(self.variable.text())
        for ele in self.checkBoxLst:
            if ele.isChecked():
                table = self.edit.text()
                if ele.text() == "Hex":
                    if len(table) * 4 != pow(2, var):
                        print("the table or variable is wrong")
                        return
                elif ele.text() == "binary":
                    table = self.binStrToHexLst(table)
                    if len(table) * 4 != pow(2, var):
                        print("the table or variable is wrong")
                        return
                elif ele.text() == "ANF":
                    table = self.ANF2Table
                print('the boolean function ' + btn.text() + " is ")
                bf = BooleanFunction(varsNum=var, longTable=table)
                if btn.text() == "nonlinearity":
                    print(bf.nonliearity())
                    return
                elif btn.text() == "transparency":
                    print(bf.transparency())
                    return
                elif btn.text() == "absolute indicator":
                    print(bf.nonAbsoluteIndictor())
                    return
                elif btn.text() == "degree":
                    print(bf.degree())
                    return
                elif btn.text() == "isBalanced":
                    print(str(bf.isBalanced()))
                    return
                elif btn.text() == "relisent":
                    print(bf.relisentCompute())
                    return
                elif btn.text() == "differential uniformity":
                    print("not found the function")
                    return

        print("please check the properity or table type")

    def whichBoxBtn(self, btn):
        # 输出被点击的按钮
        if self.variable.text() == 'n' or not self.variable.text().isdigit():
            print("please enter n-variable")
            return
        var = int(self.variable.text())
        table =  strsToSBOXTable(self.edit1.text().strip())
        print('the S BOX ' + btn.text() + " is ")
        bf = BooleanFunction(varsNum=var, S_BOX_Table = table)
        if btn.text() == "nonlinearity":
            print(bf.S_Box_Nonlinearity())
            return
        elif btn.text() == "transparency":
            print("It takes a long time. Drink first")
            print(bf.S_BOX_RTO())
            return
        elif btn.text() == "absolute indicator":
            print(bf.autoCorrelationMaxAbsolute())
            return
        elif btn.text() == "degree":
            print(bf.sBoxDegree())
            return
        elif btn.text() == "isBalanced":
            print(str(bf.S_BOX_isBalance()))
            return
        elif btn.text() == "differential uniformity":
            print(bf.differentialUniformValue())
            return
        elif btn.text() == "relisent":
            print("not found the function")
            return


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    btnDemo = Form()
    btnDemo.setStyleSheet("#MainWindow{border-image:url(./back.JPG);}")
    btnDemo.show()
    sys.exit(app.exec_())
