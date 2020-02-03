# encoding: utf-8
#-----------------------------------------------------------
# Copyright (C) 2020 Raymond Nijssen
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from functools import partial

from PyQt5.QtWidgets import QAction

from qgis.core import QgsMessageLog, Qgis
from qgis.gui import QgsPreviewEffect

def classFactory(iface):
    return PreviewModePlugin(iface)


class PreviewModePlugin:
    def __init__(self, iface):
        self.iface = iface
        self.do_log = True
        self.actions = []


    def initGui(self):
        modes = [
            {'name': 'Normal', 'effect': -1},
            {'name': 'Grayscale', 'effect': QgsPreviewEffect.PreviewGrayscale},
            {'name': 'Mono', 'effect': QgsPreviewEffect.PreviewMono},
            {'name': 'Protanope', 'effect': QgsPreviewEffect.PreviewProtanope},
            {'name': 'Deuteranope', 'effect': QgsPreviewEffect.PreviewDeuteranope}
        ]
        for mode in modes:
            action = QAction(mode['name'], self.iface.mainWindow())
            action.preview_effect = mode['effect']
            action.triggered.connect(partial(self.setPreviewMode, action))
            self.iface.addToolBarIcon(action)
            self.actions.append(action)


    def unload(self):
        for action in self.actions:
            self.iface.removeToolBarIcon(action)
            del action
        self.actions = []


    def log(self, message, tab='preview mode plugin'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def setPreviewMode(self, button):
        #self.log(button.preview_effect)
        self.iface.mapCanvas().setPreviewModeEnabled(button.preview_effect >= 0)
        if button.preview_effect >= 0:
            self.iface.mapCanvas().setPreviewMode(button.preview_effect)
