import math

try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *


# TODO merge GraphicScene and Scene
class GraphicScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        # settings
        self.gridSize = 20
        self.gridSquares = 5

        self._color_background = QColor("#ffffff")
        self._color_light = QColor("#d9d8d7")
        self._color_dark = QColor("#bcbbba")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)

    def set_graphic_scene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def dragMoveEvent(self, event):
        pass

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if x % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if y % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)


class Scene:
    def __init__(self, parent_widget=None, width=64000, height=64000):
        self.nodes = []
        self.edges = []
        self.parent_widget = parent_widget
        self.scene_width = width
        self.scene_height = height

        self._has_been_modified_listeners = []
        self._item_selected_listeners = []
        self._items_deselected_listeners = []

        self.graphic_scene = GraphicScene(self)
        self.graphic_scene.set_graphic_scene(self.scene_width, self.scene_height)

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_node(self, node):
        self.nodes.remove(node)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def add_drag_enter_listener(self, callback):
        self.graphic_scene.views()[0].add_drag_enter_listener(callback)

    def add_drop_listener(self, callback):
        self.graphic_scene.views()[0].add_drop_listener(callback)

    def add_has_been_modified_listener(self, callback):
        self._has_been_modified_listeners.append(callback)
