import sys
from qtpy import QtWidgets, QtGui
from ui.mainwindow import Ui_MainWindow
import csv
import pandas as pd

app = QtWidgets.QApplication(sys.argv)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("CSV View")
        self.read_file()
        self.ui.saveFile.clicked.connect(self.save_changes)
        self.ui.addCell.clicked.connect(self.add_row)


    def read_file(self):
        self.ui.tableWidget.setRowCount(0)
        with open("file.csv", "r", newline='', encoding="utf-8") as file:
            reader = csv.reader(file, delimiter = ',', quotechar = '"')
            for line in reader:
                row = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row)
                for i in range(0, len(line)):
                    self.ui.tableWidget.setItem(row, i, QtWidgets.QTableWidgetItem(line[i]))




    def save_changes(self):
        with open("file.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter = ",", quotechar = '"')
            rows = self.ui.tableWidget.rowCount()
            for i in range(0, rows):
                rowContent = [self.ui.tableWidget.item(i, j).text() for j in range(0, self.ui.tableWidget.columnCount())]
                writer.writerow(rowContent)

    def add_row(self):
        index = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(index)

window = MainWindow()
window.show()
sys.exit(app.exec_())