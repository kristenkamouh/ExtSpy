"""
@author Kristen Kamouh
@date 18/2/2025
@description This module contains utility functions for file operations


"""

import os
import magic
from PyQt5.QtCore import QThread, pyqtSignal

class FileScanner(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    error_occurred = pyqtSignal(str)

    def __init__(self, target_path, output_file, scan_type='folder'):
        super().__init__()
        self.target_path = target_path
        self.output_file = output_file
        self.scan_type = scan_type
        self._is_running = True

    def run(self):
        try:
            if self.scan_type == 'folder':
                self.scan_folder()
            else:
                self.scan_file()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def scan_folder(self):
        total_files = sum([len(files) for _, _, files in os.walk(self.target_path)])
        self.update_progress.emit(0)
        
        with open(self.output_file, "w") as f:
            count = 0
            for root, dirs, files in os.walk(self.target_path):
                if not self._is_running:
                    break
                for file in files:
                    if not self._is_running:
                        break
                    self.process_file(os.path.join(root, file), f)
                    count += 1
                    self.update_progress.emit(int((count/total_files)*100))
            
            self.finalize_scan()

    def scan_file(self):
        self.update_progress.emit(0)
        with open(self.output_file, "w") as f:
            self.process_file(self.target_path, f)
            self.update_progress.emit(100)
            self.finalize_scan()

    def process_file(self, file_path, file_handler):
        try:
            mime_type = magic.from_file(file_path, mime=True)
            file_extension = mime_type.split('/')[-1] if mime_type else "Unknown"
        except Exception as e:
            file_extension = f"Error: {str(e)}"
        
        absolute_path = os.path.abspath(file_path)
        file_handler.write(f"{absolute_path}, {file_extension}\n")

    def finalize_scan(self):
        if self._is_running:
            self.finished.emit(True, self.output_file)
        else:
            self.finished.emit(False, "Scanning aborted by user")

    def stop(self):
        self._is_running = False