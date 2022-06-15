from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from fbs_runtime.platform import *

from interface.mainWindow import MainWindow
from interface.welcome import *

import sys
import time

if __name__ == '__main__':
    welcome()
    
    # Change sys.stdout and sys.stderr
    stdout = open('stdout.log', 'w')
    sys.stdout = stdout

    stderr = open('stderr.log', 'w')
    sys.stderr = stderr

    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    if is_windows():
        appctxt.app.setStyle("Fusion")

    # Create and display the splash screen
    splashImage = QPixmap(appctxt.get_resource('images/splashImage_600px.png'))
    splashScreen = QSplashScreen(splashImage)
    splashScreen.show()

    appctxt.app.processEvents()

    time.sleep(1)

    # Create and display the main window
    mainWindow = MainWindow(appctxt)
    mainWindow.show()

    # Remove the splash screen
    splashScreen.finish(mainWindow)

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
