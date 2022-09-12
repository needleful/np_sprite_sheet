from krita import DockWidgetFactory, DockWidgetFactoryBase
from .plugin import DockerTemplate

DOCKER_ID = 'np_sprite_sheet'
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        DockerTemplate)

instance.addDockWidgetFactory(dock_widget_factory)