import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize, Qt
from virtual_machines import VMWindow
from anti_virus import AVWindow
from scans import ScanWindow

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("AV Pipeline")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #E8F0F2;")

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("Select a Page")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; padding-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # Add buttons with icons and subtitles
        vm_button = self.create_button("Virtual Machines", "../assets/main_menu/VMs.png", self.open_vm_page)
        antivirus_button = self.create_button("Antivirus", "../assets/main_menu/AV.png", self.open_av_page)
        scans_button = self.create_button("Scan", "../assets/main_menu/Scan.png", self.open_scans_page)

        buttons_layout.addWidget(vm_button)
        buttons_layout.addWidget(antivirus_button)
        buttons_layout.addWidget(scans_button)

        main_layout.addLayout(buttons_layout)

    def create_button(self, text, icon_path, action):
        """Helper function to create a button with an icon and subtitle."""
        button = QPushButton()
        button.setFixedSize(150, 120)  # Larger button size
        button.setStyleSheet("""
            QPushButton {
                background-color: #0056b3;  /* Button background blue */
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 15px;
                border: 2px solid #1054bc;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #003c82;  /* Darker blue on hover */
            }
        """)

        # Layout for icon and text inside the button
        button_layout = QVBoxLayout(button)
        button_layout.setSpacing(5)  # Reduce the space between icon and text

        # Create the icon label
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(60, 60)))  # Adjust the icon size to fit better
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background-color: #0056b3;")  # Icon caption background to blue

        # Create the subtitle label
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("""
            color: white; 
            font-size: 14px; 
            padding-top: 0px;  /* Reduced padding */
            padding-bottom: 0px;  /* Reduced padding */
            background-color: #0056b3;
        """)  # Reduce padding to shrink text area

        # Add icon and text to button layout
        button_layout.addWidget(icon_label)
        button_layout.addWidget(text_label)

        # Connect the button to its action
        button.clicked.connect(action)

        return button

    def open_vm_page(self):
        """Opens the Virtual Machines page."""
        self.vm_window = VMWindow(self)
        self.vm_window.show()
        self.hide()

    def open_av_page(self):
        """Opens the Antivirus page."""
        self.av_window = AVWindow(self)
        self.av_window.show()
        self.hide()

    def open_scans_page(self):
        """Opens the Scan page."""
        self.scans_window = ScanWindow(self)
        self.scans_window.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_font = QFont("Palatino Linotype", 12)
    app.setFont(app_font)
    home_page = HomePage()
    home_page.show()
    sys.exit(app.exec())
