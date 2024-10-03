import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QProgressBar, QPushButton
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon


class VMWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Window settings
        self.setWindowTitle("Virtual Machines")
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #E8F0F2;")

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Back button with icon
        back_button = QPushButton()
        back_button.setIcon(QIcon("../assets/main_menu/back.png"))  # Set the back arrow image path here
        back_button.setIconSize(QSize(40, 40))  # Set icon size
        back_button.setStyleSheet("background-color: transparent; border: none;")  # Remove background and borders
        back_button.clicked.connect(self.go_back)  # Connect the button to the back function
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Icon and title layout (Vertical with icon above title)
        icon_title_layout = QVBoxLayout()

        # Add icon above the title
        icon_label = QLabel()
        icon_pixmap = QPixmap("../assets/main_menu/VMs.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_title_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel("VIRTUAL MACHINES")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Palatino Linotype", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1565C0; padding-top: -7px;")
        icon_title_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the icon and title layout to the main layout
        main_layout.addLayout(icon_title_layout)

        # Machines layout
        self.machines_layout = QHBoxLayout()

        # Create and add VM cards (wrapped in QWidget)
        self.vm1 = self.create_vm_card("Windows 11", "Windows 11", "8 GB", "4 GB", "4", "0.37.208.72", "../assets/OS/windows 11.png")
        self.vm2 = self.create_vm_card("Windows 11", "Windows 11", "8 GB", "4 GB", "4", "124.208.27.73", "../assets/OS/windows 11.png")
        self.vm3 = self.create_vm_card("Windows 11", "Windows 11", "8 GB", "4 GB", "4", "1.137.244.126", "../assets/OS/windows 11.png")

        self.machines_layout.addWidget(self.wrap_in_widget(self.vm1["layout"]))
        self.machines_layout.addWidget(self.wrap_in_widget(self.vm2["layout"]))
        self.machines_layout.addWidget(self.wrap_in_widget(self.vm3["layout"]))

        main_layout.addLayout(self.machines_layout)

        # Add Install button at the bottom
        install_button = QPushButton("Install")
        install_button.setStyleSheet("background-color: #1565C0; color: white; font-size: 16px; padding: 10px;")
        install_button.clicked.connect(self.start_installation)
        main_layout.addWidget(install_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Timer for simulating progress bars
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

        # List of all progress bars to update
        self.progress_bars = [self.vm1["progress_bar"], self.vm2["progress_bar"], self.vm3["progress_bar"]]

    def wrap_in_widget(self, layout):
        """Wraps a layout in a QWidget so it can be added to another layout."""
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_vm_card(self, name, os_name, os_size, os_ram, p_cores, ip_address, icon_path):
        """Create a virtual machine card with icon, labels, and a progress bar."""
        vm_layout = QVBoxLayout()

        # Black box to contain the icon
        black_box = QWidget()
        black_box.setStyleSheet("background-color: black; border-radius: 10px;")  # Set the background color to black
        black_box_layout = QVBoxLayout(black_box)

        # Set the size of the black box
        black_box.setFixedSize(70, 70)  # Set width and height (adjust width here)

        # Icon
        icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        black_box_layout.addWidget(icon_label)

        # Add the black box to the VM layout
        vm_layout.addWidget(black_box, alignment=Qt.AlignmentFlag.AlignCenter)

        # OS Label
        os_label = QLabel(os_name)
        os_label.setFont(QFont("Palatino Linotype", 14, QFont.Weight.Bold))
        os_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vm_layout.addWidget(os_label)

        # Info section
        info_layout = QVBoxLayout()
        info_layout.addWidget(self.create_info_label(f"OS: {os_name}"))
        info_layout.addWidget(self.create_info_label(f"Size: {os_size}"))
        info_layout.addWidget(self.create_info_label(f"RAM: {os_ram}"))
        info_layout.addWidget(self.create_info_label(f"P-cores: {p_cores}"))
        info_layout.addWidget(self.create_info_label(f"IP: {ip_address}"))
        vm_layout.addLayout(info_layout)

        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setValue(0)  # Initially set to 0
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 15px;  # Smaller height
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
        """)
        vm_layout.addWidget(progress_bar)

        return {"layout": vm_layout, "progress_bar": progress_bar}


    def create_info_label(self, text):
        """Create styled info labels."""
        label = QLabel(text)
        label.setFont(QFont("Palatino Linotype", 12))
        label.setStyleSheet("color: white; background-color: #1565C0; padding: 5px;")
        return label

    def start_installation(self):
        """Start the installation process and progress bars."""
        self.timer.start(100)  # Start the timer to update progress every 100ms

    def update_progress(self):
        """Update the progress bars for all VMs."""
        all_finished = True
        for progress_bar in self.progress_bars:
            if progress_bar.value() < 100:
                progress_bar.setValue(progress_bar.value() + 1)
                all_finished = False

        if all_finished:
            self.timer.stop()  # Stop the timer when all bars reach 100%

    def go_back(self):
        """Go back to the main application window."""
        self.parent.show()
        self.close()