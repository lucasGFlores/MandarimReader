from PIL.Image import Image
from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame


class PhotoViewer(QGraphicsView):
    _empty = None
    def __init__(self,parent = None):
        super(PhotoViewer,self).__init__(parent)
        self._scene = QGraphicsScene(self)
        self._page = QGraphicsPixmapItem()
        self._scene.addItem(self._page)
        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QFrame.Shape.NoFrame)

    def set_image(self,pixmap=None):
        if pixmap is None:
            raise ValueError
        if pixmap.isNull:
            self._empty = True
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self._page.setPixmap(QtGui.QPixmap())

        self._page.setPixmap(pixmap)
