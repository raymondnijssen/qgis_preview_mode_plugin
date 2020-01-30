# encoding: utf-8
#-----------------------------------------------------------
# Copyright (C) 2020 Raymond Nijssen
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from PyQt5.QtWidgets import QAction

def classFactory(iface):
    return PreviewModePlugin(iface)


class PreviewModePlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction('Toggle preview', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.action.triggered.disconnect(self.run)
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        self.iface.mapCanvas().setPreviewModeEnabled(not self.iface.mapCanvas().previewModeEnabled())
