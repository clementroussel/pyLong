from PyQt5.QtWidgets import QAction, QComboBox, QMenu
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import QSize, Qt

def createActions(self):
    self.projectToolBar = self.addToolBar("Project")
    self.projectToolBar.setMovable(False)
    self.projectToolBar.setIconSize(QSize(20, 20))

    self.newProjectAction = QAction(QIcon(self.appctxt.get_resource('icons/newProject.png')), "New project", self)
    self.newProjectAction.setShortcut(QKeySequence("Ctrl+N"))
    #self.newProjectAction.triggered.connect(self.newProject)
    self.projectToolBar.addAction(self.newProjectAction)

    self.openProjectAction = QAction(QIcon(self.appctxt.get_resource('icons/openProject.png')), "Open a project", self)
    self.openProjectAction.setShortcut(QKeySequence("Ctrl+O"))
    #self.openProjectAction.triggered.connect(self.openProject)
    self.projectToolBar.addAction(self.openProjectAction)

    self.saveProjectAction = QAction(QIcon(self.appctxt.get_resource('icons/saveProject.png')), "Save project", self)
    self.saveProjectAction.setShortcut(QKeySequence("Ctrl+S"))
    #self.saveProjectAction.triggered.connect(self.saveProject)
    self.projectToolBar.addAction(self.saveProjectAction)

    self.saveProjectAsAction = QAction(QIcon(self.appctxt.get_resource('icons/saveProjectAs.png')), "Save project as... ", self)
    self.saveProjectAsAction.setShortcut(QKeySequence("Shift+Ctrl+S"))
    #self.saveProjectAsAction.triggered.connect(self.saveProjectAs)
    self.projectToolBar.addAction(self.saveProjectAsAction)

    self.settingsAction = QAction(QIcon(self.appctxt.get_resource('icons/settings.png')), "Settings", self)
    self.settingsAction.triggered.connect(self.settings)
    self.projectToolBar.addAction(self.settingsAction)

    self.projectToolBar.addSeparator() 

    self.interfaceToolBar = self.addToolBar("Interface")
    self.interfaceToolBar.setMovable(False)
    self.interfaceToolBar.setIconSize(QSize(20, 20))

    self.fullScreenAction = QAction(QIcon(self.appctxt.get_resource('icons/fullScreen.png')), "Full screen", self)
    self.fullScreenAction.setCheckable(True)
    self.fullScreenAction.setShortcut(QKeySequence("F11"))
    self.fullScreenAction.triggered.connect(self.fullScreen)
    self.interfaceToolBar.addAction(self.fullScreenAction)

    self.zoomInAction = QAction(QIcon(self.appctxt.get_resource('icons/zoomIn.png')), "Zoom in", self)
    self.zoomInAction.setShortcut(QKeySequence("Ctrl++"))
    self.zoomInAction.triggered.connect(self.zoomIn)
    self.interfaceToolBar.addAction(self.zoomInAction)

    self.zoomOutAction = QAction(QIcon(self.appctxt.get_resource('icons/zoomOut.png')), "Zoom out", self)
    self.zoomOutAction.setShortcut(QKeySequence("Ctrl+-"))
    self.zoomOutAction.triggered.connect(self.zoomOut)
    self.interfaceToolBar.addAction(self.zoomOutAction)

    self.adjustWidthAction = QAction(QIcon(self.appctxt.get_resource('icons/adjustWidth.png')), "Adjust width", self)
    self.adjustWidthAction.triggered.connect(self.adjustWidth)
    self.interfaceToolBar.addAction(self.adjustWidthAction)

    self.adjustHeightAction = QAction(QIcon(self.appctxt.get_resource('icons/adjustHeight.png')), "Adjust height", self)
    self.adjustHeightAction.triggered.connect(self.adjustHeight)
    self.interfaceToolBar.addAction(self.adjustHeightAction)

    self.interfaceToolBar.addSeparator()

    self.figureToolBar = self.addToolBar("Figure")
    self.figureToolBar.setMovable(False)
    self.figureToolBar.setIconSize(QSize(20, 20))

    ##################################################
    # liste des mises en pages + son menu contextuel #
    ##################################################
    self.layoutsList = QComboBox()
    self.layoutsList.setMinimumWidth(100)
    for layout in self.project.layouts:
        self.layoutsList.addItem(layout.title)

    self.layoutsList.currentIndexChanged.connect(self.canvas.updateFigure)

    self.layoutsList.setContextMenuPolicy(Qt.CustomContextMenu)
    self.layoutsList.customContextMenuRequested.connect(self.contextMenuLayouts)

    self.popMenuLayouts = QMenu(self)
    self.addLayoutAction = QAction('Add a new layout', self)
    self.renameLayoutAction = QAction('Rename current layout', self)
    self.deleteLayoutsAction = QAction('Delete layouts', self)
    self.addLayoutAction.triggered.connect(self.addLayout)
    self.renameLayoutAction.triggered.connect(self.renameLayout)
    self.deleteLayoutsAction.triggered.connect(self.deleteLayouts)
    self.popMenuLayouts.addAction(self.addLayoutAction)
    self.popMenuLayouts.addSeparator()
    self.popMenuLayouts.addAction(self.renameLayoutAction)
    self.popMenuLayouts.addSeparator()
    self.popMenuLayouts.addAction(self.deleteLayoutsAction)

    self.figureToolBar.addWidget(self.layoutsList)
    ##################################################

    self.layoutAction = QAction(QIcon(self.appctxt.get_resource('icons/layout.png')), "Layout properties", self)
    self.layoutAction.triggered.connect(self.layout)
    self.figureToolBar.addAction(self.layoutAction)

    self.advancedLayoutAction = QAction(QIcon(self.appctxt.get_resource('icons/advancedLayout.png')), "Advanced layout properties", self)
    self.advancedLayoutAction.triggered.connect(self.advancedLayout)
    self.figureToolBar.addAction(self.advancedLayoutAction)

    self.refreshAction = QAction(QIcon(self.appctxt.get_resource('icons/refresh.png')), "Refresh", self)
    self.refreshAction.setShortcut(QKeySequence("Ctrl+R"))
    self.refreshAction.triggered.connect(self.refresh)
    self.figureToolBar.addAction(self.refreshAction)

    self.printAction = QAction(QIcon(self.appctxt.get_resource('icons/print.png')), "Print", self)
    self.printAction.setShortcut(QKeySequence("Ctrl+P"))
    #self.printAction.triggered.connect(self.print)
    self.figureToolBar.addAction(self.printAction)

    self.copyFigureAction = QAction(QIcon(self.appctxt.get_resource('icons/copyFigure.png')), "Copy", self)
    self.copyFigureAction.setShortcut(QKeySequence("Ctrl+C"))
    self.copyFigureAction.triggered.connect(self.copyFigure)
    self.figureToolBar.addAction(self.copyFigureAction)

    self.figureToolBar.addSeparator()

    self.subplotToolBar = self.addToolBar("Subplot")
    self.subplotToolBar.setMovable(False)
    self.subplotToolBar.setIconSize(QSize(20, 20))

    self.subplotsManagerAction = QAction(QIcon(self.appctxt.get_resource('icons/subplotsManager.png')), "Subplots manager", self)
    self.subplotsManagerAction.triggered.connect(self.subplotsManager)
    self.subplotToolBar.addAction(self.subplotsManagerAction)

    self.subplotToolBar.addSeparator()

    self.profileToolBar = self.addToolBar("Profile")
    self.profileToolBar.setMovable(False)
    self.profileToolBar.setIconSize(QSize(20, 20))

    self.addProfileAction = QAction(QIcon(self.appctxt.get_resource('icons/addProfile.png')), "Add a new profile", self)
    self.addProfileAction.triggered.connect(self.addProfile)
    self.profileToolBar.addAction(self.addProfileAction)

    self.tableAction = QAction(QIcon(self.appctxt.get_resource('icons/table.png')), "Profile Values ​​Table", self)
    #self.tableAction.triggered.connect(self.table)
    self.profileToolBar.addAction(self.tableAction)

    self.profileStyleAction = QAction(QIcon(self.appctxt.get_resource('icons/style.png')), "Profile style", self)
    self.profileStyleAction.triggered.connect(self.profileStyle)
    self.profileToolBar.addAction(self.profileStyleAction)

    self.sortAction = QAction(QIcon(self.appctxt.get_resource('icons/sort.png')), "Sort", self)
    self.sortAction.triggered.connect(self.sort)
    self.profileToolBar.addAction(self.sortAction)

    self.filterAction = QAction(QIcon(self.appctxt.get_resource('icons/filter.png')), "Filter", self)
    self.filterAction.triggered.connect(self.filter)
    self.profileToolBar.addAction(self.filterAction)

    self.simplifyAction = QAction(QIcon(self.appctxt.get_resource('icons/simplify.png')), "Simplify", self)
    self.simplifyAction.triggered.connect(self.simplify)
    self.profileToolBar.addAction(self.simplifyAction)

    self.exportAction = QAction(QIcon(self.appctxt.get_resource('icons/export.png')), "Export", self)
    self.exportAction.triggered.connect(self.export)
    self.profileToolBar.addAction(self.exportAction)

    self.profileDeleteAction = QAction(QIcon(self.appctxt.get_resource('icons/delete.png')), "Delete", self)
    self.profileDeleteAction.triggered.connect(self.profileDelete)
    self.profileDeleteAction.setShortcut(QKeySequence("Alt+P"))
    self.profileToolBar.addAction(self.profileDeleteAction)

    self.profileToolBar.addSeparator()

    self.editingToolBar = self.addToolBar("Interactive editing")
    self.editingToolBar.setMovable(False)
    self.editingToolBar.setIconSize(QSize(20, 20))

    self.editingAction = QAction(QIcon(self.appctxt.get_resource('icons/editing.png')), "Interactive editing", self)
    self.editingAction.setCheckable(True)
    self.editingAction.triggered.connect(self.edit)
    self.editingToolBar.addAction(self.editingAction)

    self.addPointAction = QAction(QIcon(self.appctxt.get_resource('icons/addPoint.png')), "Add a vertice", self)
    self.addPointAction.setCheckable(True)
    self.addPointAction.triggered.connect(self.addPoint)
    self.addPointAction.setShortcut(QKeySequence("Shift+A"))
    self.editingToolBar.addAction(self.addPointAction)
    self.addPointAction.setVisible(False)

    self.deletePointAction = QAction(QIcon(self.appctxt.get_resource('icons/deletePoint.png')), "Delete a vertice", self)
    self.deletePointAction.setCheckable(True)
    self.deletePointAction.triggered.connect(self.removePoint)
    self.deletePointAction.setShortcut(QKeySequence("Shift+S"))
    self.editingToolBar.addAction(self.deletePointAction)
    self.deletePointAction.setVisible(False)

    self.magnetismAction = QAction(QIcon(self.appctxt.get_resource('icons/magnetism.png')), "Magnetism", self)
    self.magnetismAction.setCheckable(True)
    self.magnetismAction.triggered.connect(self.updateProfilesList)
    self.magnetismAction.triggered.connect(self.activateMagnetism)
    self.editingToolBar.addAction(self.magnetismAction)
    self.magnetismAction.setVisible(False)

    self.profilesComboBox = QComboBox()
    for profile in self.project.profiles:
        self.profilesComboBox.addItem(profile.title)
    self.profilesListAction = self.editingToolBar.addWidget(self.profilesComboBox)
    self.profilesListAction.setVisible(False)

    self.editingToolBar.addSeparator()

    self.annotationToolBar = self.addToolBar("Annotation")
    self.annotationToolBar.setMovable(False)
    self.annotationToolBar.setIconSize(QSize(20, 20))

    self.addTextAction = QAction(QIcon(self.appctxt.get_resource('icons/text.png')), "Add a text", self)
    self.addTextAction.triggered.connect(self.addText)
    self.annotationToolBar.addAction(self.addTextAction)

    self.addVerticalAnnotationAction = QAction(QIcon(self.appctxt.get_resource('icons/verticalAnnotation.png')), "Add a vertical annotation", self)
    self.addVerticalAnnotationAction.triggered.connect(self.addVerticalAnnotation)
    self.annotationToolBar.addAction(self.addVerticalAnnotationAction)

    self.addLinearAnnotationAction = QAction(QIcon(self.appctxt.get_resource('icons/linearAnnotation.png')), "Add a linear annotation", self)
    self.addLinearAnnotationAction.triggered.connect(self.addLinearAnnotation)
    self.annotationToolBar.addAction(self.addLinearAnnotationAction)

    self.addIntervalAction = QAction(QIcon(self.appctxt.get_resource('icons/interval.png')), "Add an interval", self)
    self.addIntervalAction.triggered.connect(self.addInterval)
    self.annotationToolBar.addAction(self.addIntervalAction)

    self.addRectangleAction = QAction(QIcon(self.appctxt.get_resource('icons/rectangle.png')), "Add a rectangle", self)
    self.addRectangleAction.triggered.connect(self.addRectangle)
    self.annotationToolBar.addAction(self.addRectangleAction)

    self.annotationStyleAction = QAction(QIcon(self.appctxt.get_resource('icons/style.png')), "Annotation style", self)
    self.annotationStyleAction.triggered.connect(self.annotationStyle)
    self.annotationToolBar.addAction(self.annotationStyleAction)

    self.copyStyleAction = QAction(QIcon(self.appctxt.get_resource('icons/copyStyle.png')), "Copy style", self)
    self.copyStyleAction.triggered.connect(self.copyStyle)
    self.copyStyleAction.setShortcut(QKeySequence("Ctrl+Alt+C"))
    self.annotationToolBar.addAction(self.copyStyleAction)

    self.pasteStyleAction = QAction(QIcon(self.appctxt.get_resource('icons/pasteStyle.png')), "Paste style", self)
    self.pasteStyleAction.triggered.connect(self.pasteStyle)
    self.pasteStyleAction.setShortcut(QKeySequence("Ctrl+Alt+V"))
    self.annotationToolBar.addAction(self.pasteStyleAction)

    self.adjustVerticalAnnotationAction = QAction(QIcon(self.appctxt.get_resource('icons/adjustVerticalAnnotation.png')), "Adjust vertical annotations", self)
    self.adjustVerticalAnnotationAction.setShortcut(QKeySequence("Ctrl+Alt+Z"))
    self.adjustVerticalAnnotationAction.triggered.connect(self.adjustVerticalAnnotation)
    self.annotationToolBar.addAction(self.adjustVerticalAnnotationAction)

    self.duplicateAction = QAction(QIcon(self.appctxt.get_resource('icons/duplicate.png')), "Duplicate", self)
    self.duplicateAction.setShortcut(QKeySequence("Ctrl+Alt+D"))
    self.duplicateAction.triggered.connect(self.duplicate)
    self.annotationToolBar.addAction(self.duplicateAction)

    self.groupsManagerAction = QAction(QIcon(self.appctxt.get_resource('icons/groupsManager.png')), "Groups manager", self)
    #self.groupsManagerAction.triggered.connect(self.groupsManager)
    self.annotationToolBar.addAction(self.groupsManagerAction)

    self.annotationDeleteAction = QAction(QIcon(self.appctxt.get_resource('icons/delete.png')), "Delete", self)
    self.annotationDeleteAction.triggered.connect(self.annotationDelete)
    self.annotationDeleteAction.setShortcut(QKeySequence("Alt+A"))
    self.annotationToolBar.addAction(self.annotationDeleteAction)

    self.annotationToolBar.addSeparator()

    self.reminderLineToolBar = self.addToolBar("Reminder line")
    self.reminderLineToolBar.setMovable(False)
    self.reminderLineToolBar.setIconSize(QSize(20, 20))

    self.annotation2reminderLineAction = QAction(QIcon(self.appctxt.get_resource('icons/annotation2reminderLine.png')), "Annotation >>> Reminder line", self)
    #self.annotation2reminderLineAction.triggered.connect(self.annotation2reminderLine)
    self.reminderLineToolBar.addAction(self.annotation2reminderLineAction)

    self.reminderLinesManagerAction = QAction(QIcon(self.appctxt.get_resource('icons/reminderLinesManager.png')), "Reminder lines manager", self)
    #self.reminderLinesManagerAction.triggered.connect(self.reminderLinesManager)
    self.reminderLineToolBar.addAction(self.reminderLinesManagerAction)

    self.reminderLineToolBar.addSeparator()

    self.toolboxToolBar = self.addToolBar("Toolbox")
    self.toolboxToolBar.setMovable(False)
    self.toolboxToolBar.setIconSize(QSize(20, 20))

    self.toolboxAction = QAction(QIcon(self.appctxt.get_resource('icons/toolbox.png')), "Toolbox", self)
    self.toolboxAction.triggered.connect(self.toolBox)
    self.toolboxToolBar.addAction(self.toolboxAction)

    self.calculationAction = QAction(QIcon(self.appctxt.get_resource('icons/calculation.png')), "Calculation properties", self)
    self.calculationAction.triggered.connect(self.calculation)
    self.toolboxToolBar.addAction(self.calculationAction)

    self.calculationDeleteAction = QAction(QIcon(self.appctxt.get_resource('icons/delete.png')), "Delete", self)
    self.calculationDeleteAction.triggered.connect(self.calculationDelete)
    self.calculationDeleteAction.setShortcut(QKeySequence("Alt+C"))
    self.toolboxToolBar.addAction(self.calculationDeleteAction)

    self.toolboxToolBar.addSeparator()

    self.otherDataToolBar = self.addToolBar("Other data")
    self.otherDataToolBar.setMovable(False)
    self.otherDataToolBar.setIconSize(QSize(20, 20))

    self.addDataAction = QAction(QIcon(self.appctxt.get_resource('icons/addData.png')), "Add new data", self)
    #self.addDataAction.triggered.connect(self.addData)
    self.otherDataToolBar.addAction(self.addDataAction)

    self.dataStyleAction = QAction(QIcon(self.appctxt.get_resource('icons/style.png')), "Data style", self)
    # self.action_styleDonnees.triggered.connect(self.dataStyle)
    self.otherDataToolBar.addAction(self.dataStyleAction)

    self.dataDeleteAction = QAction(QIcon(self.appctxt.get_resource('icons/delete.png')), "Delete", self)
    #self.action_supprimerDonnees.triggered.connect(self.dataDelete)
    self.dataDeleteAction.setShortcut(QKeySequence("Alt+D"))
    self.otherDataToolBar.addAction(self.dataDeleteAction)

    self.otherDataToolBar.addSeparator()

    self.resourceToolBar = self.addToolBar("Resources")
    self.resourceToolBar.setMovable(False)
    self.resourceToolBar.setIconSize(QSize(20, 20))

    self.documentationAction = QAction(QIcon(self.appctxt.get_resource('icons/documentation.png')), "Documentation", self)
    self.documentationAction.triggered.connect(self.documentation)
    self.resourceToolBar.addAction(self.documentationAction)

    self.aboutAction = QAction(QIcon(self.appctxt.get_resource('icons/about.png')), "About pyLong", self)
    self.aboutAction.triggered.connect(self.about)
    self.resourceToolBar.addAction(self.aboutAction)

    self.onfToolBar = self.addToolBar("ONF")
    self.onfToolBar.setMovable(False)
    self.onfToolBar.setIconSize(QSize(52, 20))

    self.onfAction = QAction(QIcon(self.appctxt.get_resource('icons/onf.png')), "www.onf.fr ", self)
    self.onfAction.triggered.connect(self.onf)
    self.onfToolBar.addAction(self.onfAction)

    menu = self.menuBar()

    self.projectMenu = menu.addMenu("Project")

    self.projectMenu.addAction(self.newProjectAction)
    self.projectMenu.addSeparator()
    self.projectMenu.addAction(self.openProjectAction)
    self.recentFilesMenu = self.projectMenu.addMenu("Open a recent project")
    # for path in self.recentFiles:
    #     self.menuRecent.addAction(f"{chemin}", lambda path=chemin: self.ouvrirProjetRecent(chemin=path))
    self.projectMenu.addSeparator()
    self.projectMenu.addAction(self.saveProjectAction)
    self.projectMenu.addAction(self.saveProjectAsAction)
    self.projectMenu.addSeparator()
    self.projectMenu.addAction(self.settingsAction)
    self.projectMenu.addSeparator()
    
    self.quitPyLongAction = QAction("Quit pyLong", self)
    self.quitPyLongAction.setShortcut(QKeySequence("Ctrl+Q"))
    #self.quitPyLongAction.triggered.connect(self.quitPylong)
    self.projectMenu.addAction(self.quitPyLongAction)

    self.interfaceMenu = menu.addMenu("Interface")
    self.interfaceMenu.addAction(self.fullScreenAction)
    self.interfaceMenu.addSeparator()
    self.interfaceMenu.addAction(self.zoomInAction)
    self.interfaceMenu.addAction(self.zoomOutAction)
    self.interfaceMenu.addAction(self.adjustWidthAction)
    self.interfaceMenu.addAction(self.adjustHeightAction)


    self.figureMenu = menu.addMenu("Figure")

    self.figureMenu.addAction(self.addLayoutAction)
    self.figureMenu.addAction(self.renameLayoutAction)
    self.figureMenu.addAction(self.deleteLayoutsAction)
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.layoutAction)
    self.figureMenu.addAction(self.advancedLayoutAction)
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.refreshAction)
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.navigationBar._actions['back'])
    self.figureMenu.addAction(self.navigationBar._actions['forward'])
    self.figureMenu.addAction(self.navigationBar._actions['pan'])
    self.figureMenu.addAction(self.navigationBar._actions['zoom'])
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.printAction)
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.copyFigureAction)

    self.subplotMenu = menu.addMenu("Subplot")

    self.subplotMenu.addAction(self.subplotsManagerAction)

    self.profileMenu = menu.addMenu("Profile")

    self.profileMenu.addAction(self.addProfileAction)
    self.profileMenu.addSeparator()
    self.profileMenu.addAction(self.tableAction)
    self.profileMenu.addSeparator()
    self.profileMenu.addAction(self.profileStyleAction)
    self.profileMenu.addSeparator()
    self.profileMenu.addAction(self.sortAction)
    self.profileMenu.addAction(self.filterAction)
    self.profileMenu.addAction(self.simplifyAction)
    self.profileMenu.addAction(self.exportAction)
    self.profileMenu.addSeparator()
    self.profileMenu.addAction(self.profileDeleteAction)

    menuEdition = menu.addMenu("Interactive editing")

    menuEdition.addAction(self.editingAction)
    menuEdition.addSeparator()
    menuEdition.addAction(self.addPointAction)
    menuEdition.addAction(self.deletePointAction)
    menuEdition.addAction(self.magnetismAction)

    self.annotationMenu = menu.addMenu("Annotation")
    self.annotationMenu.addAction(self.addTextAction)
    self.annotationMenu.addAction(self.addVerticalAnnotationAction)
    self.annotationMenu.addAction(self.addLinearAnnotationAction)
    self.annotationMenu.addAction(self.addIntervalAction)
    self.annotationMenu.addAction(self.addRectangleAction)
    self.annotationMenu.addSeparator()
    self.annotationMenu.addAction(self.annotationStyleAction)
    self.annotationMenu.addSeparator()
    self.annotationMenu.addAction(self.copyStyleAction)
    self.annotationMenu.addAction(self.pasteStyleAction)
    self.annotationMenu.addSeparator()
    self.annotationMenu.addAction(self.adjustVerticalAnnotationAction)
    self.annotationMenu.addSeparator()
    self.annotationMenu.addAction(self.duplicateAction)
    self.annotationMenu.addSeparator()

    self.addGroupAction = QAction('Add a new group', self)
    self.addGroupAction.triggered.connect(self.addGroup)
    self.annotationMenu.addAction(self.addGroupAction)
    self.renameGroupAction = QAction('Rename current group', self)
    self.renameGroupAction.triggered.connect(self.renameGroup)
    self.annotationMenu.addAction(self.renameGroupAction)
    self.deleteGroupsAction = QAction('Delete groups', self)
    self.deleteGroupsAction.triggered.connect(self.deleteGroups)
    self.annotationMenu.addAction(self.deleteGroupsAction)

    self.annotationMenu.addAction(self.groupsManagerAction)
    self.annotationMenu.addSeparator()
    self.annotationMenu.addAction(self.annotationDeleteAction)

    self.reminderLineMenu = menu.addMenu("Reminder line")
    self.reminderLineMenu.addAction(self.annotation2reminderLineAction)
    self.reminderLineMenu.addSeparator()
    self.reminderLineMenu.addAction(self.reminderLinesManagerAction)

    self.toolboxMenu = menu.addMenu("Toolbox")
    self.toolboxMenu.addAction(self.toolboxAction)
    self.toolboxMenu.addSeparator()
    self.toolboxMenu.addAction(self.calculationAction)
    self.toolboxMenu.addSeparator()
    self.toolboxMenu.addAction(self.calculationDeleteAction)

    self.otherDataMenu = menu.addMenu("Other data")
    self.otherDataMenu.addAction(self.addDataAction)
    self.otherDataMenu.addSeparator()
    self.otherDataMenu.addAction(self.dataStyleAction)
    self.otherDataMenu.addSeparator()
    self.otherDataMenu.addAction(self.dataDeleteAction)

    self.resourceMenu = menu.addMenu("Resources")
    self.resourceMenu.addAction(self.documentationAction)
    self.resourceMenu.addSeparator()
    self.resourceMenu.addAction(self.aboutAction)
    self.resourceMenu.addSeparator()
    self.resourceMenu.addAction(self.onfAction)
