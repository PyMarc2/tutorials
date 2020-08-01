
from PyQt5 import QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # selected items
        self.selected = []
        self.no       = []

        self.tableModel = QtGui.QStandardItemModel(self)
        self.tableModel.itemChanged.connect(self.itemChanged)
        #
        item1 = QtGui.QStandardItem("file#1")
        item1.setCheckable(True)
        no1 = QtGui.QStandardItem("5.0")
        self.tableModel.appendRow([item1, no1])
        #
        item2 = QtGui.QStandardItem("file#2")
        item2.setCheckable(True)
        no2 = QtGui.QStandardItem("23.0")
        self.tableModel.appendRow([item2, no2])

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(self.tableModel)
        self.mainLayout.addWidget(self.tableView)

        "First Question"
        """How to make table only editable second column, not firts:
           ex. can edit 23.0 or 5.0, but read only file names?
        """

    def itemChanged(self, item):
        if item.checkState() != 0:
            if not item.text() in self.selected:
                self.selected.append(item.text())
        else:
            if item.text() in self.selected:
                self.selected.remove(item.text())

        print(self.selected)

        "Second Question"
        """How to get item checked index and to get the second column value:
           ex. file#2 has 23.0?
        """

        #self.no.append(second column value) ****?
        print(self.no)


def main():
    app = QtWidgets.QApplication([])

    mytable = MyWidget()
    mytable.show()
    app.exec_()


if __name__ == "__main__":
    main()
