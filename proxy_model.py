
from PyQt5.QtCore import QAbstractProxyModel, QIdentityProxyModel, QSortFilterProxyModel, \
                         QModelIndex, QVariant, Qt

class ReverseProxyModel(QAbstractProxyModel):
    def __init__(self, parent=None):
        super(ReverseProxyModel, self).__init__(parent)
        pass
    
    def mapToSource(self, proxyIndex):
        if( self.sourceModel() ):
            return self.sourceModel().index(proxyIndex.column(), proxyIndex.row() )
        pass
    def mapFromSource(self, sourceIndex):
        return self.index(sourceIndex.column(), sourceIndex.row() )
        pass
    def index(self, row, column, parent= QModelIndex()):
        return self.createIndex(column, row, 0)
        pass
    def parent(self, child):
        return QModelIndex()
        pass
    
    def rowCount(self, parent = QModelIndex() ):
        if( self.sourceModel() ):
            return self.sourceModel().columnCount()
        else:
            return 0
        pass
    def columnCount(self, parent = QModelIndex() ):
        if( self.sourceModel() ):
            return self.sourceModel().rowCount()
        else:
            return 0 
        pass

    def headerData(self, section, orientation, role):
        if( self.sourceModel() == None):
            return QVariant()
        new_orientation = None
        if( orientation == Qt.Horizontal ):
            new_orientation = Qt.Vertical
        else:
            new_orientation = Qt.Horizontal
        return self.sourceModel().headerData(section, new_orientation, role)
            
class ColumnProxyModel(QAbstractProxyModel):
    # model 의 한 column 만 보여주는 모델 
    def __init__(self, parent=None):
        super(ColumnProxyModel, self).__init__(parent)
        self.key_column = 0
        pass

    def setKeyColumn(self, col_num = 0):
        self.key_column = col_num;
        pass
    
    def mapToSource(self, proxyIndex):
        if( self.sourceModel() ):
            return self.sourceModel().index(proxyIndex.row(), self.key_column )
        else:
            return QModelIndex()
        pass
    def mapFromSource(self, sourceIndex):
        return self.index(sourceIndex.row(), self.key_column)
        pass

    def index(self, row, column, parent= QModelIndex()):
        return self.createIndex(row, self.key_column, 0)
        pass
    
    def rowCount(self, parent = QModelIndex() ):
        if( self.sourceModel() ):
            return self.sourceModel().rowCount()
        else:
            return 0
        pass

    def columnCount(self, parent = QModelIndex() ):
        if( self.sourceModel() ):
            return self.sourceModel().columnCount()
        else:
            return 0 
        pass

    def headerData(self, section, orientation, role):
        if( self.sourceModel() == None):
            return QVariant()
        return self.sourceModel().headerData(section, orientation, role)
            