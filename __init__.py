# encoding: utf-8
#-----------------------------------------------------------
# Copyright (C) 2020 Raymond Nijssen
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 3
#
# <one line to give the program's name and a brief idea of what it does.>
# Copyright (C) <year>  <name of author>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#---------------------------------------------------------------------

import os

from functools import partial

from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from qgis.core import QgsMessageLog, Qgis
from qgis.gui import QgsPreviewEffect

def classFactory(iface):
    return PreviewModePlugin(iface)


class PreviewModePlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.do_log = True
        self.actions = []


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Preview Mode Toolbar")
        modes = [
            {'name': 'Normal', 'effect': -1},
            {'name': 'Grayscale', 'effect': QgsPreviewEffect.PreviewGrayscale},
            {'name': 'Mono', 'effect': QgsPreviewEffect.PreviewMono},
            {'name': 'Protanope', 'effect': QgsPreviewEffect.PreviewProtanope},
            {'name': 'Deuteranope', 'effect': QgsPreviewEffect.PreviewDeuteranope}
        ]
        for mode in modes:
            icon = QIcon(os.path.join(self.plugin_dir, 'icon_{}.svg'.format(mode['name'].lower())))
            action = QAction(icon, mode['name'], self.iface.mainWindow())
            action.preview_effect = mode['effect']
            action.triggered.connect(partial(self.setPreviewMode, action))
            self.toolbar.addAction(action)
            self.actions.append(action)


    def unload(self):
        for action in self.actions:
            self.toolbar.removeAction(action)
            del action
        self.actions = []
        del self.toolbar


    def log(self, message, tab='preview mode plugin'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def setPreviewMode(self, button):
        #self.log(button.preview_effect)
        self.iface.mapCanvas().setPreviewModeEnabled(button.preview_effect >= 0)
        if button.preview_effect >= 0:
            self.iface.mapCanvas().setPreviewMode(button.preview_effect)
