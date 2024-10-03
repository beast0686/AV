import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QProgressBar, QFileDialog, QWidget, QFrame
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QTimer, QSize


class ScanWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        # Window settings
        self.setWindowTitle("Anti-Virus Scanner")
        self.setFixedSize(900, 600)

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Back button with an icon instead of text
        back_button = QPushButton()
        back_button.setIcon(QIcon("../assets/main_menu/back.png"))
        back_button.setIconSize(QSize(40, 40))
        back_button.setStyleSheet("background-color: transparent; border: none;")
        back_button.clicked.connect(self.go_back)

        # Create a horizontal layout to place the back button at the top left
        top_layout = QHBoxLayout()
        top_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        top_layout.addStretch()  # Add stretch to push any other elements to the right
        main_layout.addLayout(top_layout)

        # Create a frame to wrap the header (like a box)
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)

        # Icon above the header
        icon_label = QLabel()
        icon_pixmap = QPixmap("../assets/main_menu/Scan.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(icon_label)

        # Create the header QLabel
        header = QLabel("SCAN & REPORT")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Palatino Linotype", 16, QFont.Weight.Bold))
        header.setStyleSheet("""
                    color: #1565C0;
                    padding: -7px;
                """)
        header_layout.addWidget(header)

        # Add header frame to the main layout (without border)
        main_layout.addWidget(header_frame)

        # Folder selection section
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Select Folder:")
        folder_label.setFont(QFont("Palatino Linotype", 12))
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Enter Path ...")
        self.folder_input.setFixedHeight(30)
        self.folder_input.setStyleSheet("background-color: #ADD8E6; font-size: 14px; padding-left: 5px;")
        browse_button = QPushButton("Browse")
        browse_button.setStyleSheet("background-color: #1565C0; color: white; font-size: 14px; padding: 5px;")
        browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_button)
        main_layout.addLayout(folder_layout)

        # Scanning section
        scanning_label = QLabel("SCANNING")
        scanning_label.setFont(QFont("Palatino Linotype", 14, QFont.Weight.Bold))
        scanning_label.setStyleSheet("color: black;")
        main_layout.addWidget(scanning_label)

        # Antivirus scanning progress
        scanning_layout = QHBoxLayout()
        self.progress_bars = []
        scanning_layout.addLayout(self.create_scan_progress("Microsoft Defender", 0))
        scanning_layout.addLayout(self.create_scan_progress("Trend Micro Security", 0))
        scanning_layout.addLayout(self.create_scan_progress("Eset Internet Security", 0))
        main_layout.addLayout(scanning_layout)

        # Add "Scan" button
        scan_button = QPushButton("Scan")
        scan_button.setStyleSheet("background-color: #1565C0; color: white; font-size: 14px; padding: 10px;")
        scan_button.clicked.connect(self.start_scanning)
        main_layout.addWidget(scan_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Infected files section
        infected_label = QLabel("INFECTED FILES")
        infected_label.setFont(QFont("Palatino Linotype", 14, QFont.Weight.Bold))
        infected_label.setStyleSheet("color: black;")
        main_layout.addWidget(infected_label)

        # Blue background box for infected files and AV report
        blue_box_frame = QFrame()
        blue_box_frame.setStyleSheet("background-color: #1565C0;")
        blue_box_layout = QHBoxLayout(blue_box_frame)

        # Infected files display
        self.files_display = QLabel("Files ...")
        self.files_display.setStyleSheet(
            "background-color: white; font-size: 14px; padding: 5px; border: 2px solid black;")
        self.files_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # AV report display
        self.report_display = QLabel("AV Report ...")
        self.report_display.setStyleSheet(
            "background-color: white; font-size: 14px; padding: 5px; border: 2px solid black;")
        self.report_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        blue_box_layout.addWidget(self.files_display)
        blue_box_layout.addWidget(self.report_display)

        main_layout.addWidget(blue_box_frame)  # Add the blue box to the main layout

        # Action buttons (moved to the bottom-right)
        action_button_layout = QHBoxLayout()
        action_button_layout.addStretch()  # Push buttons to the right

        infected_folder_button = QPushButton("Infected Folder")
        infected_folder_button.setFixedSize(120, 40)  # Make button smaller
        infected_folder_button.setStyleSheet("background-color: #1565C0; color: white; font-size: 12px; padding: 5px;")
        infected_folder_button.clicked.connect(self.open_infected_folder)

        report_button = QPushButton("Report")
        report_button.setFixedSize(120, 40)  # Make button smaller
        report_button.setStyleSheet("background-color: #1565C0; color: white; font-size: 12px; padding: 5px;")
        report_button.clicked.connect(self.generate_report)

        action_button_layout.addWidget(infected_folder_button)
        action_button_layout.addWidget(report_button)
        main_layout.addLayout(action_button_layout)

        # Timer for simulating progress bar updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bars)

    def create_scan_progress(self, name, progress_value):
        """Create a layout with antivirus name and progress bar."""
        scan_layout = QVBoxLayout()

        # Antivirus name
        av_name_label = QLabel(name)
        av_name_label.setFont(QFont("Palatino Linotype", 14, QFont.Weight.Bold))
        av_name_label.setStyleSheet("color: white; background-color: #1565C0; padding: 5px;")
        scan_layout.addWidget(av_name_label)

        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setValue(progress_value)
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
        scan_layout.addWidget(progress_bar)
        self.progress_bars.append(progress_bar)
        return scan_layout

    def browse_folder(self):
        """Open file dialog to select folder."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_input.setText(folder_path)

    def open_infected_folder(self):
        """Dummy function to open infected folder."""
        print("Infected Folder button clicked")

    def generate_report(self):
        """Dummy function to generate the report."""
        print("Report button clicked")

    def start_scanning(self):
        """Start the scanning process."""
        self.timer.start(100)  # Update progress bars every 100ms

    def update_progress_bars(self):
        """Update the progress bars by increasing their values."""
        all_finished = True
        for progress_bar in self.progress_bars:
            if progress_bar.value() < 100:
                progress_bar.setValue(progress_bar.value() + 1)  # Increment by 1
                all_finished = False

        if all_finished:
            self.timer.stop()  # Stop updating when all progress bars reach 100

    def go_back(self):
        """Go back to the main application window."""
        self.parent.show()
        self.close()
