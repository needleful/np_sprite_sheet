from krita import DockWidget

DOCKER_TITLE = 'NP Sprite Sheet'

class DockerTemplate(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)

    # notifies when views are added or removed
    # 'pass' means do not do anything
    def canvasChanged(self, canvas):
        pass

