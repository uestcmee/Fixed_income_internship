import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI_Window import Ui_Dialog
# 失败！！

class MyWindow(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        # self.ex=Ui_Dialog
        self.setupUi(self)

        # 由于UI_window的结构的特殊，参数传不出来，很气
        # 没有__init__函数
        # self.ex.send_value.connect(self.rec_data)


    def rec_data(self,Fac_list):
        print('a====',Fac_list)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())