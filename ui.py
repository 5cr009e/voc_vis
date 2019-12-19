import sys
from PyQt5.QtWidgets import QApplication, QSizePolicy, QFileSystemModel,\
    QTreeView, QWidget, QVBoxLayout
from PyQt5.QtCore import QDir
import re
import json

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.figure import Figure

from vis import plot_rect

with open("config.json", "r") as config_file:
    config = json.loads(config_file.read())


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file system view'
        self.left = 100
        self.top = 100
        self.width = 1140
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(config['rgb_img_path']))
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setWindowTitle("Dir View")
        self.tree.resize(640, 480)
        self.tree.doubleClicked.connect(self.plot)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)
        self.m = PlotCanvas(self, width=5, height=4)
        self.m.move(640, 0)
        self.show()

    def plot(self, signal):
        file_path = self.tree.model().filePath(signal)
        sample_id = re.search(r'\d+', file_path.split('/')[-1]).group()
        self.m.plot(str(sample_id))


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(211)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(config['img_id'])

    def plot(self, img_id):
        self.figure.clf()
        ax0 = self.figure.add_subplot(211)
        ax1 = self.figure.add_subplot(212)
        plot_rect([ax0, ax1],
                  img_id,
                  config['ir_img_path']+'/',
                  config['ir_anno_path']+'/',
                  config['rgb_img_path']+'/',
                  config['rgb_anno_path']+'/')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
