from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QTableView, QApplication


class ParametersTableModel(QAbstractTableModel):

    def __init__(self):
        super(ParametersTableModel, self).__init__()
        self.headerText = ["Parameter 1", "Parameter 2"]
        self.data = [[1, 2], [1, 2]]

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.headerText)

    def headerData(self, col, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headerText[col]

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.data[index.row()][index.column()]

    def flags(self, index):
        if not index.isValid():
            return None
        else:
            if index.column() == 1:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
            else:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable


def main():
    app = QApplication([])
    tableModel = ParametersTableModel()
    tableView = QTableView()
    tableView.setModel(tableModel)
    tableView.show()
    app.exec_()


if __name__ == "__main__":
    main()
