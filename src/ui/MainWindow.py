"""
@author Kristen Kamouh
@date 18/2/2025
@description This module contains utility functions for file operations

"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QFileDialog, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

from src.utils.FileOperation import FileOperations
from src.scanner.FileScanner import FileScanner


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scanner = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ExtSpy')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('assets/extspy-logo.png'))

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        main_widget.setLayout(layout)

        # Header section
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout()
        header_frame.setLayout(header_layout)

        # Title with custom font
        self.title_label = QLabel('ExtSpy')
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Subtitle
        self.subtitle_label = QLabel('File Extension Analyzer')
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)
        layout.addWidget(header_frame)

        # Action buttons container
        action_frame = QFrame()
        action_frame.setObjectName("actionFrame")
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        action_frame.setLayout(button_layout)

        # Folder scan button with icon
        self.folder_btn = QPushButton(' Scan Folder')
        self.folder_btn.setObjectName("primaryButton")
        self.folder_btn.clicked.connect(self.start_folder_scan)
        self.folder_btn.setFixedHeight(50)
        button_layout.addWidget(self.folder_btn)

        # File scan button with icon
        self.file_btn = QPushButton(' Scan Single File')
        self.file_btn.setObjectName("primaryButton")
        self.file_btn.clicked.connect(self.start_file_scan)
        self.file_btn.setFixedHeight(50)
        button_layout.addWidget(self.file_btn)

        layout.addWidget(action_frame)

        # Progress section
        progress_frame = QFrame()
        progress_frame.setObjectName("progressFrame")
        progress_layout = QVBoxLayout()
        progress_frame.setLayout(progress_layout)

        # Progress bar with modern style
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        progress_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel('Ready')
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.status_label)

        layout.addWidget(progress_frame)

        # Save button at bottom
        self.save_btn = QPushButton('Save Output')
        self.save_btn.setObjectName("secondaryButton")
        self.save_btn.clicked.connect(self.save_output)
        self.save_btn.setFixedHeight(50)
        layout.addWidget(self.save_btn)

        # Add stretch to push content to top
        layout.addStretch()

        # Apply modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            
            #headerFrame {
                background-color: transparent;
                margin-bottom: 20px;
            }
            
            #titleLabel {
                color: #1a73e8;
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            #subtitleLabel {
                color: #5f6368;
                font-size: 18px;
            }
            
            #actionFrame {
                background-color: transparent;
                margin: 20px 0;
            }
            
            #primaryButton {
                background-color: #1a73e8;
                color: white;
                font-size: 16px;
                font-weight: 500;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            
            #primaryButton:hover {
                background-color: #1557b0;
            }
            
            #primaryButton:disabled {
                background-color: #89b4f7;
            }
            
            #secondaryButton {
                background-color: #f8f9fa;
                color: #1a73e8;
                font-size: 16px;
                font-weight: 500;
                border: 2px solid #1a73e8;
                border-radius: 8px;
                padding: 10px 20px;
            }
            
            #secondaryButton:hover {
                background-color: #e8f0fe;
            }
            
            #progressFrame {
                background-color: transparent;
                margin: 20px 0;
            }
            
            #progressBar {
                background-color: #e8f0fe;
                border: none;
                border-radius: 4px;
            }
            
            #progressBar::chunk {
                background-color: #1a73e8;
                border-radius: 4px;
            }
            
            #statusLabel {
                color: #5f6368;
                font-size: 14px;
                margin-top: 10px;
            }
            
            QMessageBox {
                background-color: white;
            }
            
            QMessageBox QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        
    def save_output(self):
        FileOperations.save_output(self)

    def start_folder_scan(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder to Scan')
        if not folder_path:
            return

        output_file = FileOperations.get_output_path()
        if not output_file:
            return

        self.scanner = FileScanner(folder_path, output_file, scan_type='folder')
        self.connect_scanner()
        self.scanner.start()

    def start_file_scan(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File to Scan')
        if not file_path:
            return

        output_file = FileOperations.get_output_path()
        if not output_file:
            return

        self.scanner = FileScanner(file_path, output_file, scan_type='file')
        self.connect_scanner()
        self.scanner.start()

    def connect_scanner(self):
        self.scanner.update_progress.connect(self.update_progress)
        self.scanner.finished.connect(self.scan_finished)
        self.scanner.error_occurred.connect(self.show_error)
        self.folder_btn.setEnabled(False)
        self.file_btn.setEnabled(False)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.status_label.setText(f'Scanning... {value}%')

    def scan_finished(self, success, message):
        self.folder_btn.setEnabled(True)
        self.file_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, 'Success', 
                f'Scanning completed!\nResults saved to: {message}')
        else:
            QMessageBox.warning(self, 'Warning', message)
        self.progress_bar.reset()
        self.status_label.setText('Ready')

    def show_error(self, message):
        self.folder_btn.setEnabled(True)
        self.file_btn.setEnabled(True)
        QMessageBox.critical(self, 'Error', f'An error occurred: {message}')
        self.progress_bar.reset()
        self.status_label.setText('Error occurred')

    def closeEvent(self, event):
        if self.scanner and self.scanner.isRunning():
            self.scanner.stop()
            self.scanner.quit()
            self.scanner.wait(2000)
        event.accept()