#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''{{cookiecutter.project_slug}}

{{cookiecutter.project_description}}

'''

import sys
import os
import platform

sys.dont_write_bytecode = True  # Avoid writing .pyc files

# ----------------------------------------------------------------------
# Environment detection
# ----------------------------------------------------------------------

try:
    import maya.cmds as cmds
    MAYA = True
except ImportError:
    MAYA = False

try:
    import nuke
    import nukescripts
    NUKE = True
except ImportError:
    NUKE = False

STANDALONE = False
if not MAYA and not NUKE:
    STANDALONE = True

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# Window title and object names
WINDOW_TITLE = '{{cookiecutter.project_slug}}'
WINDOW_OBJECT = '{{cookiecutter.project_slug|lower}}'

# Docking
DOCK_WITH_MAYA_UI = {{cookiecutter.dock_in_maya}}
DOCK_WITH_NUKE_UI = {{cookiecutter.dock_in_nuke}}

# Repository path
REPO_PATH = os.path.realpath(os.path.dirname(__file__))

# Full path to where .ui files are stored
UI_PATH = os.path.join(REPO_PATH, 'data')

# Palette filepath
PALETTE_FILEPATH = os.path.join(UI_PATH, 'qpalette_maya2016.json')

# Qt.py option: Set up preffered binding
# os.environ['QT_PREFERRED_BINDING'] = 'PyQt4'
# os.environ['QT_PREFERRED_BINDING'] = 'PySide'
# os.environ['QT_PREFERRED_BINDING'] = 'PyQt5'
# os.environ['QT_PREFERRED_BINDING'] = 'PySide2'


# ----------------------------------------------------------------------
# Main script
# ----------------------------------------------------------------------

from .extern.Qt import QtWidgets  # pylint: disable=E0611
from .extern.Qt import QtCore     # pylint: disable=E0611
from .extern.Qt import QtCompat

from .lib import mayapalette
from .lib.dcc import *


class {{cookiecutter.project_slug}}(QtWidgets.QMainWindow):
    """
    {{cookiecutter.project_description}}
    """

    def __init__(self, parent=None):

        super({{cookiecutter.project_slug}}, self).__init__(parent)

        # Set object name and window title
        self.setObjectName(WINDOW_OBJECT)
        self.setWindowTitle(WINDOW_TITLE)

        # Window type
        self.setWindowFlags(QtCore.Qt.Window)

        if MAYA:
            # Makes Maya perform magic which makes the window stay
            # on top in OS X and Linux. As an added bonus, it'll
            # make Maya remember the window position
            self.setProperty("saveWindowPref", True)

        # Filepaths
        main_window_file = os.path.join(UI_PATH, 'main_window.ui')
        module_file = os.path.join(UI_PATH, 'module.ui')

        # Load UIs
        self.main_widget = QtCompat.load_ui(main_window_file)  # Main window UI
        self.module_widget = QtCompat.load_ui(module_file)  # Module UI

        # Attach module to main window UI's boilerVerticalLayout layout
        self.main_widget.boilerVerticalLayout.addWidget(self.module_widget)

        # Set the main widget
        self.setCentralWidget(self.main_widget)

        # Define minimum size of UI
        self.setMinimumSize(200, 200)


    def event(self, event):

        if event.type() == QtCore.QEvent.Type.Show:
            try:
                _nuke_set_zero_margins(self)
            except:
                pass

        return QtWidgets.QMainWindow.event(self, event)

# ----------------------------------------------------------------------
# Run functions
# ----------------------------------------------------------------------

def run_maya():
    """Run in Maya"""
    _maya_delete_ui(WINDOW_OBJECT, WINDOW_TITLE)  # Delete any existing existing UI
    boil = {{cookiecutter.project_slug}}(parent=_maya_main_window())

    # Makes Maya perform magic which makes the window stay
    # on top in OS X and Linux. As an added bonus, it'll
    # make Maya remember the window position
    boil.setProperty("saveWindowPref", True)

    if not DOCK_WITH_MAYA_UI:
        boil.show()  # Show the UI
    elif DOCK_WITH_MAYA_UI:
        allowed_areas = ['right', 'left']
        cmds.dockControl(WINDOW_TITLE, label=WINDOW_TITLE, area='left',
                         content=WINDOW_OBJECT, allowedArea=allowed_areas)


def run_nuke():
    """Run in Nuke

    Note:
        If you want the UI to always stay on top, replace:
        `boil.ui.setWindowFlags(QtCore.Qt.Tool)`
        with:
        `boil.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)`

        If you want the UI to be modal:
        `boil.ui.setWindowModality(QtCore.Qt.WindowModal)`
    """
    _nuke_delete_ui(WINDOW_OBJECT)  # Delete any alrady existing UI
    if not DOCK_WITH_NUKE_UI:
        boil = {{cookiecutter.project_slug}}(parent=_nuke_main_window())
        boil.setWindowFlags(QtCore.Qt.Tool)
        boil.show()  # Show the UI
    elif DOCK_WITH_NUKE_UI:
        panel = nukescripts.panels.registerWidgetAsPanel(
            widget='{{cookiecutter.project_slug|lower}}.{{cookiecutter.project_slug}}',  # module_name.Class_name
            name=WINDOW_TITLE,
            id='uk.co.thefoundry.' + WINDOW_TITLE,
            create=True)



def run_standalone():
    """Run standalone
    """
    app = QtWidgets.QApplication(sys.argv)
    boil = {{cookiecutter.project_slug}}()
    if not (platform.system() == 'Darwin' and
            (QtCompat.__binding__ == 'PySide' or QtCompat.__binding__ == 'PyQt4')):
        mayapalette.set_maya_palette_with_tweaks(PALETTE_FILEPATH)
    boil.show()  # Show the UI
    sys.exit(app.exec_())


def main():
    """Run based on env
    """
    if MAYA:
        run_maya()
    elif NUKE:
        run_nuke()
    else:
        run_standalone()

if __name__ == "__main__":
    main()
