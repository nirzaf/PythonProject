#!/usr/bin/env python3
"""
HL7 to JSON Converter

This script converts HL7 ADT messages to JSON format using the hl7conv2 library.
It can process individual messages or extract multiple messages from markdown files.

Usage:
    python hl7_to_json_converter.py [input_file] [output_file]

    Or run without arguments to launch the GUI.
"""

import os
import sys
import json
import re
import warnings
from typing import List, Dict, Any, Optional, Tuple
from hl7conv2 import Hl7Json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                            QTextEdit, QMessageBox, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt

# Suppress the sipPyTypeDict deprecation warning
warnings.filterwarnings("ignore", message=".*sipPyTypeDict.*")


class HL7Converter:
    """Class to handle conversion of HL7 messages to JSON format"""

    @staticmethod
    def extract_hl7_messages_from_markdown(file_path: str) -> List[str]:
        """
        Extract HL7 messages from a markdown file.

        Args:
            file_path: Path to the markdown file containing HL7 messages

        Returns:
            List of extracted HL7 messages as strings
        """
        with open(file_path, 'r') as file:
            content = file.read()

        # Find all HL7 messages enclosed in triple backticks
        pattern = r'```\n(.*?)\n```'
        messages = re.findall(pattern, content, re.DOTALL)

        return messages

    @staticmethod
    def convert_hl7_to_json(hl7_message: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Convert a single HL7 message to JSON format.

        Args:
            hl7_message: HL7 message string

        Returns:
            Tuple of (JSON object or None, error message or None)
        """
        try:
            # Use hl7conv2 to convert the message
            hl7_obj = Hl7Json(hl7_message)
            json_data = hl7_obj.hl7_json
            return json_data, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def process_file(input_file: str, output_file: str) -> Tuple[int, int]:
        """
        Process a markdown file containing HL7 messages and convert them to JSON.

        Args:
            input_file: Path to the input markdown file
            output_file: Path to the output JSON file

        Returns:
            Tuple of (number of successful conversions, number of failed conversions)
        """
        # Extract messages from the markdown file
        messages = HL7Converter.extract_hl7_messages_from_markdown(input_file)

        successful = 0
        failed = 0
        results = []

        # Process each message
        for i, message in enumerate(messages):
            json_data, error = HL7Converter.convert_hl7_to_json(message)

            if json_data:
                # Add metadata to help identify the message
                result = {
                    "message_index": i + 1,
                    "conversion_status": "success",
                    "data": json_data
                }
                results.append(result)
                successful += 1
            else:
                # Include error information for failed conversions
                result = {
                    "message_index": i + 1,
                    "conversion_status": "failed",
                    "error": error,
                    "original_message": message
                }
                results.append(result)
                failed += 1

        # Write the results to the output file
        with open(output_file, 'w') as file:
            json.dump(results, file, indent=2)

        return successful, failed


class HL7ConverterGUI(QMainWindow):
    """GUI for the HL7 to JSON Converter"""

    def __init__(self):
        super().__init__()
        self.input_file = ""
        self.output_file = ""
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("HL7 to JSON Converter")
        self.setMinimumSize(700, 500)

        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # File selection group
        file_group = QGroupBox("File Selection")
        file_layout = QGridLayout()

        # Input file selection
        self.input_label = QLabel("Input File:")
        self.input_path = QLabel("No file selected")
        self.input_button = QPushButton("Browse...")
        self.input_button.clicked.connect(self.select_input_file)

        # Output file selection
        self.output_label = QLabel("Output File:")
        self.output_path = QLabel("No file selected")
        self.output_button = QPushButton("Browse...")
        self.output_button.clicked.connect(self.select_output_file)

        # Add widgets to file layout
        file_layout.addWidget(self.input_label, 0, 0)
        file_layout.addWidget(self.input_path, 0, 1)
        file_layout.addWidget(self.input_button, 0, 2)
        file_layout.addWidget(self.output_label, 1, 0)
        file_layout.addWidget(self.output_path, 1, 1)
        file_layout.addWidget(self.output_button, 1, 2)

        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # Results area
        results_group = QGroupBox("Conversion Results")
        results_layout = QVBoxLayout()

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)

        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)

        # Buttons
        button_layout = QHBoxLayout()

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_file)
        self.convert_button.setEnabled(False)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_results)

        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        # Set central widget
        self.setCentralWidget(central_widget)

    def select_input_file(self):
        """Open file dialog to select input file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input File", "", "Markdown Files (*.md);;All Files (*)"
        )

        if file_path:
            self.input_file = file_path
            self.input_path.setText(file_path)
            self.update_convert_button()

    def select_output_file(self):
        """Open file dialog to select output file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select Output File", "", "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            self.output_file = file_path
            self.output_path.setText(file_path)
            self.update_convert_button()

    def update_convert_button(self):
        """Enable convert button if both input and output files are selected"""
        self.convert_button.setEnabled(bool(self.input_file and self.output_file))

    def convert_file(self):
        """Process the input file and convert HL7 messages to JSON"""
        if not os.path.exists(self.input_file):
            QMessageBox.critical(self, "Error", f"Input file '{self.input_file}' not found.")
            return

        self.results_text.clear()
        self.results_text.append(f"Processing {self.input_file}...")

        try:
            successful, failed = HL7Converter.process_file(self.input_file, self.output_file)

            self.results_text.append(f"\nConversion complete:")
            self.results_text.append(f"  - Successfully converted: {successful} messages")
            self.results_text.append(f"  - Failed conversions: {failed} messages")
            self.results_text.append(f"  - Output saved to: {self.output_file}")

            if successful > 0:
                QMessageBox.information(self, "Success", f"Conversion complete. {successful} messages converted successfully.")
            else:
                QMessageBox.warning(self, "Warning", "No messages were converted successfully.")

        except Exception as e:
            self.results_text.append(f"\nError during conversion: {str(e)}")
            QMessageBox.critical(self, "Error", f"An error occurred during conversion: {str(e)}")

    def clear_results(self):
        """Clear the results text area"""
        self.results_text.clear()


def main():
    """Main function to handle command line arguments or launch GUI"""
    # If command line arguments are provided, use CLI mode
    if len(sys.argv) > 1:
        if len(sys.argv) < 3:
            print(f"Usage: {sys.argv[0]} input_file output_file")
            sys.exit(1)

        input_file = sys.argv[1]
        output_file = sys.argv[2]

        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            sys.exit(1)

        print(f"Processing {input_file}...")
        successful, failed = HL7Converter.process_file(input_file, output_file)

        print(f"Conversion complete:")
        print(f"  - Successfully converted: {successful} messages")
        print(f"  - Failed conversions: {failed} messages")
        print(f"  - Output saved to: {output_file}")
    # Otherwise, launch the GUI
    else:
        app = QApplication(sys.argv)
        window = HL7ConverterGUI()
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
