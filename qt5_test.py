import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QPushButton, QTextEdit, QGridLayout,QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def changeText(self):
        print('a')

    def initUI(self):
        title = QLabel("Title")
        author = QLabel("Author")
        review = QLabel("Review")
        self.review2=QPushButton('ok',self)
        #self.review2.clicked.connect(self.changeText())
        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5,1)
        grid.addWidget(self.review2, 4, 0)



        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("Review")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())