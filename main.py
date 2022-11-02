import _thread
import ctypes
import sys
import time

from PyQt5.QtWidgets import QApplication

import POS_window as main_window

if __name__ == '__main__':
    def exit_completely():
        time.sleep(2)
        print('Exiting...')
        _thread.interrupt_main()

    app = QApplication(sys.argv)
    app_id = 'CubeIQ.POS_app.A1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    win = main_window.Window()
    win.showMaximized()
    app.aboutToQuit.connect(exit_completely)
    sys.exit(app.exec_())
