"""
@author Kristen Kamouh
@date 18/2/2025
@description This module contains utility functions for file operations
"""

import os
import shutil
import tempfile
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class FileOperations:
    _temp_file = None
    _current_scan_file = None  # Track the current scan output file

    @staticmethod
    def get_output_path():
        """
        Creates a temporary file for storing scan results.
        Returns the path to the temporary file.
        """
        try:
            # Close previous temp file if it exists
            if FileOperations._temp_file:
                try:
                    FileOperations._temp_file.close()
                except:
                    pass

            # Create new temporary file
            FileOperations._temp_file = tempfile.NamedTemporaryFile(
                mode='w',
                delete=False,
                suffix='.txt',
                prefix='extspy_',
                encoding='utf-8'
            )
            FileOperations._current_scan_file = FileOperations._temp_file.name
            return FileOperations._current_scan_file
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error",
                f"Failed to create temporary file:\n{str(e)}"
            )
            return None

    @staticmethod
    def save_output(parent_window, temp_path=None):
        """
        Saves the scan results to a user-selected location.
        
        Args:
            parent_window: The main window instance for showing dialogs
            temp_path: Optional path to temp file. If None, uses last known scan file
        """
        # Use the tracked scan file if no temp_path provided
        temp_path = temp_path or FileOperations._current_scan_file

        if not temp_path or not os.path.exists(temp_path):
            QMessageBox.warning(
                parent_window,
                "Warning",
                "No scan results available to save!"
            )
            return False

        try:
            # Get size of temp file to verify it has content
            if os.path.getsize(temp_path) == 0:
                QMessageBox.warning(
                    parent_window,
                    "Warning",
                    "No scan results available to save!"
                )
                return False

            # Get save location from user
            save_path, _ = QFileDialog.getSaveFileName(
                parent_window,
                "Save Output File",
                os.path.join(os.path.expanduser('~'), 'extspy_output.txt'),
                "Text Files (*.txt)"
            )

            if not save_path:
                return False

            # Ensure the save path has .txt extension
            if not save_path.lower().endswith('.txt'):
                save_path += '.txt'

            # Remove existing file if it exists
            if os.path.exists(save_path):
                try:
                    os.remove(save_path)
                except PermissionError:
                    QMessageBox.critical(
                        parent_window,
                        "Permission Denied",
                        f"Could not overwrite existing file:\n{save_path}\n"
                        "Please check file permissions or choose another location."
                    )
                    return False

            # Copy the temp file to the destination
            shutil.copyfile(temp_path, save_path)

            # Verify the file was saved successfully
            if not os.path.exists(save_path) or os.path.getsize(save_path) == 0:
                raise Exception("Failed to save file or file is empty")

            QMessageBox.information(
                parent_window,
                "Success",
                f"Output successfully saved to:\n{save_path}"
            )
            return True

        except PermissionError as e:
            QMessageBox.critical(
                parent_window,
                "Permission Denied",
                f"Could not save to {save_path}\nCheck file permissions and ensure you have "
                "write access to the selected location."
            )
            return False

        except Exception as e:
            QMessageBox.critical(
                parent_window,
                "Error",
                f"Failed to save output:\n{str(e)}\nPlease try saving to a different location."
            )
            return False

    @staticmethod
    def cleanup():
        """Clean up temporary files when the application exits"""
        # Clean up current scan file
        if FileOperations._current_scan_file and os.path.exists(FileOperations._current_scan_file):
            try:
                os.remove(FileOperations._current_scan_file)
            except:
                pass

        # Clean up temp file if different from scan file
        if (FileOperations._temp_file and 
            FileOperations._temp_file.name != FileOperations._current_scan_file and 
            os.path.exists(FileOperations._temp_file.name)):
            try:
                FileOperations._temp_file.close()
                os.remove(FileOperations._temp_file.name)
            except:
                pass

        FileOperations._temp_file = None
        FileOperations._current_scan_file = None