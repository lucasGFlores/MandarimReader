import os
from inspect import getsourcefile
from multiprocessing import Process
from pathlib import Path

from PySide6.QtWidgets import QApplication
from src.HMI.pyside.src.screens.page_screen.page_screen import PageScreen
os.chdir(Path(getsourcefile(lambda: 0)).resolve().parent)

class Interface:
    def __init__(self):
        self._worker = self._run_interface
        self._process = None

    def start(self):
        if self._process is None:
            self._process = Process(target=self._run_interface)
        self._process.start()
    @staticmethod
    def _run_interface():
        app = QApplication()
        main = PageScreen()
        main.show()
        app.exec()

