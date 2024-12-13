import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QComboBox
from PyQt6.QtCore import Qt

class FEConfigGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI components
        self.setWindowTitle("FE Configuration Generator")
        self.setGeometry(300, 300, 400, 400)
        self.setStyleSheet("background-color: #2e2e2e; font-family: Arial, sans-serif;")

        # Main layout
        self.layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel("FE Configuration Generator")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #f0f0f0;")
        self.layout.addWidget(self.title_label)

        # Create the form layout for inputs
        self.form_layout = QFormLayout()

        self.inputs = {}
        self.create_input("Vendor Name (Company)", "")
        self.create_input("Model (Name)", "")
        self.create_input("ID Code", "")
        self.create_input("Page Size", "")
        self.create_input("Block Size (Left)", "")
        self.create_input("Block Size (Right)", "")
        self.create_input("Plane Size", "")
        self.create_input("Bank Count", "")
        self.create_input("Bank Size (e.g., 64 GB)", "")

        # Add DDR selection
        self.ddr_combo = QComboBox()
        self.ddr_combo.addItems(["false", "true"])
        self.ddr_combo.setStyleSheet("""
            QComboBox {
                background-color: #333333;
                color: #f0f0f0;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.form_layout.addRow(QLabel("DDR"), self.ddr_combo)

        self.layout.addLayout(self.form_layout)

        # Add instruction note for Plane Size and Block button
        self.plane_note = QLabel("<b>Note:</b><br>Block sizes are converted automatically.<br>Left block uses decimal (block).<br>Right block uses hexadecimal (bytes).<br>Right plane uses hexadecimal (block).")
        self.plane_note.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.plane_note.setStyleSheet("font-size: 14px; color: #b0b0b0; margin-top: 10px;")
        self.layout.addWidget(self.plane_note)

        # Add Generate button with styling
        self.generate_button = QPushButton("Generate FE Format")
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.generate_button.clicked.connect(self.generate_fe)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)

    def create_input(self, label, default_value=""):
        input_field = QLineEdit(default_value)
        input_field.setPlaceholderText(default_value)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                color: #f0f0f0;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.form_layout.addRow(QLabel(label), input_field)
        self.inputs[label] = input_field

    def generate_fe(self):
        try:
            # Extract input values
            vendor_name = self.inputs["Vendor Name (Company)"].text()
            model_name = self.inputs["Model (Name)"].text()
            page_size = int(self.inputs["Page Size"].text())
            block_size_left = int(self.inputs["Block Size (Left)"].text())  # Decimal input for left block size
            block_size_right = int(self.inputs["Block Size (Right)"].text(), 16)  # Hexadecimal input for right block size
            plane_size = int(self.inputs["Plane Size"].text(), 16)
            id_code = self.inputs["ID Code"].text()
            bank_count = int(self.inputs["Bank Count"].text())
            bank_size = self.inputs["Bank Size (e.g., 64 GB)"].text()
            ddr = self.ddr_combo.currentText()

            # Apply WL DDR NAND transformations
            page = page_size // 3  # Divide Page Size by 3
            skip_mask_1 = f"0x{block_size_left - 1:x}"  # Subtract 1 and format as hexadecimal
            skip_page_1 = hex(block_size_right)
            blocks = hex(plane_size)  # Use the right Plane Size for Blocks
            block = hex(block_size_right)  # Use the right Block Size for Block

            # Format Banks field with space
            banks = f"{bank_count} x {bank_size.strip()}"  # e.g., "1 x 64 GB"

            # Create FE format
            fe_format = f"""
// Chip
Company      {vendor_name}
Name         {model_name}
ID code      {id_code}

// Structure
Bus          8
Banks        {banks}
Page         {page}
Block        {block}
Blocks       {blocks}

// Read
Cmd          WL
Col          2
Row          3
DDR          {ddr}

// Timings
RE_Up        2
RE_Down      2

// Special
Power
Retry
Skip_Mask_1  {skip_mask_1}
Skip_Page_1  {skip_page_1}
Skip_Mask_2  0xffffffff
Skip_Page_2  0xffffffff
Join CE
"""

            # Save to file
            with open("Chip.txt", "w") as file:
                file.write(fe_format)

            # Success message
            QMessageBox.information(self, "Success", "FE configuration saved to Chip.txt")

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set global style for the application
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2e2e2e;
        }
        QWidget {
            background-color: #2e2e2e;
            color: #f0f0f0;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """)

    window = FEConfigGenerator()
    window.show()
    sys.exit(app.exec())
