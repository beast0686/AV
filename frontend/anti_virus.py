import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QProgressBar, \
    QPushButton
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon


class AVWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Store progress bars in a list so they can be updated later
        self.progress_bars = []

        # Window settings
        self.setWindowTitle("Anti-Virus Page")
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #E8F0F2;")  # Background color

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        back_button = QPushButton()
        back_button.setIcon(QIcon("../assets/main_menu/back.png"))  # Set the back arrow image path here
        back_button.setIconSize(QSize(40, 40))  # Corrected: Use QSize from PyQt6.QtCore
        back_button.setStyleSheet("background-color: transparent; border: none;")  # Remove background and borders
        back_button.clicked.connect(self.go_back)  # Connect the button to the back function
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Icon above the header
        icon_label = QLabel()
        icon_pixmap = QPixmap("../assets/main_menu/AV.png").scaled(50, 50,
                                                                   Qt.AspectRatioMode.KeepAspectRatio)  # Adjust the icon size if needed
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(icon_label)  # Add icon to the main layout

        # Header
        header = QLabel("ANTI-VIRUS")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Palatino Linotype", 16, QFont.Weight.Bold))
        header.setStyleSheet("""
            color: #1565C0;
            padding: -7px;
        """)
        main_layout.addWidget(header)

        # Anti-virus layout (icons and information)
        av_layout = QHBoxLayout()

        # Add anti-virus cards (wrapped in QWidget)
        av_layout.addWidget(self.wrap_in_widget(
            self.create_av_card("Microsoft Defender", "Windows 11", "8 GB", "4 GB", "4", "0.37.208.72",
                                "../assets/AV/windows_defender.png")))
        av_layout.addWidget(self.wrap_in_widget(
            self.create_av_card("Trend Micro Security", "Windows 11", "8 GB", "4 GB", "4", "124.208.27.73",
                                "../assets/AV/Trend_Micro_Maximum_Security.png")))
        av_layout.addWidget(self.wrap_in_widget(
            self.create_av_card("Eset Internet Security", "Windows 11", "8 GB", "4 GB", "4", "1.137.244.126",
                                "../assets/AV/eset.png")))

        main_layout.addLayout(av_layout)

        # Add Install button at the bottom of the layout
        install_button = QPushButton("Install")
        install_button.setStyleSheet("background-color: #1565C0; color: white; font-size: 14px; padding: 10px;")
        install_button.clicked.connect(self.start_installation)
        main_layout.addWidget(install_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def wrap_in_widget(self, layout):
        """Wraps a layout in a QWidget so it can be added to another layout."""
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_av_card(self, name, os_name, os_size, os_ram, p_cores, ip_address, icon_path):
        """Create a layout for each anti-virus section."""
        card_layout = QVBoxLayout()

        # Black box container - reduce size
        icon_container = QWidget()
        icon_container.setStyleSheet("background-color: black; border-radius: 10px;")
        icon_container.setFixedSize(80, 80)  # Smaller black box size
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        # Icon inside black box - reduce icon size
        icon_label = QLabel()
        icon_pixmap = QPixmap(icon_path).scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)  # Smaller icon size
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)

        card_layout.addWidget(icon_container, alignment=Qt.AlignmentFlag.AlignCenter)

        # Antivirus Name
        name_label = QLabel(name)
        name_label.setFont(QFont("Palatino Linotype", 14, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(name_label)

        # Information Labels
        info_layout = QVBoxLayout()
        info_layout.addWidget(self.create_info_label(f"OS: {os_name}"))
        info_layout.addWidget(self.create_info_label(f"Size: {os_size}"))
        info_layout.addWidget(self.create_info_label(f"RAM: {os_ram}"))
        info_layout.addWidget(self.create_info_label(f"P-cores: {p_cores}"))
        info_layout.addWidget(self.create_info_label(f"IP: {ip_address}"))  # Placeholder for IP info
        card_layout.addLayout(info_layout)

        # Progress Bar - Make smaller in height
        progress_bar = QProgressBar()
        progress_bar.setValue(0)  # Initially set progress to 0
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
        card_layout.addWidget(progress_bar)

        # Store the progress bar in the list for later use
        self.progress_bars.append(progress_bar)

        return card_layout

    def create_info_label(self, text):
        """Create styled info labels."""
        label = QLabel(text)
        label.setFont(QFont("Palatino Linotype", 12))
        label.setStyleSheet("color: white; background-color: #1565C0; padding: 5px;")
        return label

    def go_back(self):
        """Go back to the main application window."""
        self.parent.show()
        self.close()

    def start_installation(self):
        """Start the installation process and update all progress bars."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bars)
        self.timer.start(100)  # Update every 100 milliseconds

    def update_progress_bars(self):
        """Update the progress bars by increasing their values."""
        all_finished = True
        for progress_bar in self.progress_bars:
            if progress_bar.value() < 100:
                progress_bar.setValue(progress_bar.value() + 1)  # Increment by 1
                all_finished = False

        if all_finished:
            self.timer.stop()  # Stop updating when all progress bars reach 100
