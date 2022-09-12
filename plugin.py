from krita import DockWidget
from PyQt5.QtWidgets import *

from .np_sprite_sheet import *

DOCKER_TITLE = 'NP Sprite Sheet'

class DockerTemplate(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)

        self.main_widget = QWidget(self)
        self.main_widget.setContentsMargins(20, 20, 10, 10)
        self.setWidget(self.main_widget)

        self.preview_button = QPushButton("Preview Sprite Sheet", self.main_widget)
        self.preview_button.clicked.connect(preview_spritesheet)

        self.export_button = QPushButton("Export Sprite Sheet", self.main_widget)
        self.export_button.clicked.connect(self.showExportMenu)

        layout = QVBoxLayout()
        layout.addWidget(self.preview_button)
        layout.addWidget(self.export_button)
        self.main_widget.setLayout(layout)

        self.folder_picker = QFileDialog()
        self.folder_picker.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        self.folder_picker.fileSelected.connect(self.exportSprites)

    # notifies when views are added or removed
    # 'pass' means do not do anything
    def canvasChanged(self, canvas):
        pass

    def showExportMenu(self):
        self.folder_picker.show()

    def exportSprites(self, value):
        export_spritesheet(value)