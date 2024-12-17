import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QTabWidget, QPushButton, QLabel, QFrame, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate

from StudentInformationManagement import StudentInformationManagement
from SystemStatistics import SystemStatistics
from Profile import ProfileView
from RecognitionStudent import RecognitionStudentView


class HomeView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Face Recognition System')
        self.setGeometry(0, 0, 1200, 700)
        self.setStyleSheet("color: black;")
        self.init_ui()

    def init_ui(self):
        # Giao diện chính
        self.central_widget = QWidget(self)
        self.central_widget.setFixedSize(1200, 700)
        self.central_widget.setStyleSheet("background-color: lightblue;")

        # Tạo panel chính
        self.panel = QFrame(self.central_widget)
        self.panel.setGeometry(15, 15, 1150, 650)
        self.panel.setStyleSheet("""
                           background-color: white;
                           border-radius: 10px;
                       """)

        # Tạo header
        self.header_panel = QFrame(self.panel)
        self.header_panel.setGeometry(0, 0, 1150, 50)
        self.header_panel.setStyleSheet("""
                            background-color: white;
                            border-top-right-radius: 10px;
                            border-top-left-radius: 10px;
                            border-bottom: 1px solid black;
                        """)

        # Thêm đồng hồ và ngày tháng
        self.clock_panel = QFrame(self.header_panel)
        self.clock_panel.setGeometry(5, 5, 50, 40)
        self.clock_panel.setStyleSheet("border: none;")

        self.clock_icon = QLabel(self.clock_panel)
        self.clock_icon.setPixmap(QPixmap('../Image/clock-icon.png').scaled(35, 30))
        self.clock_icon.setGeometry(5, 5, 35, 30)

        self.time_date_panel = QFrame(self.header_panel)
        self.time_date_panel.setGeometry(50, 5, 150, 40)
        self.time_date_layout = QVBoxLayout(self.time_date_panel)
        self.time_date_layout.setContentsMargins(0, 0, 0, 0)
        self.time_date_panel.setStyleSheet("border: none;")

        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 12px; font-weight: bold; border: none;")
        self.time_date_layout.addWidget(self.time_label)

        self.date_label = QLabel()
        self.date_label.setStyleSheet("font-size: 12px; font-weight: bold; border: none;")
        self.time_date_layout.addWidget(self.date_label)

        # Tạo title
        self.title_label = QLabel("Hệ thống nhận diện khuôn mặt")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_panel = QFrame(self.header_panel)
        self.title_panel.setGeometry(300, 5, 550, 40)
        self.title_panel.setStyleSheet("border: none;")

        self.title_layout = QHBoxLayout(self.title_panel)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.addWidget(self.title_label)

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        self.main_widget = QWidget(self.panel)
        self.main_widget.setStyleSheet("background-color: white;")
        self.main_widget.setGeometry(0, 50, 1150, 600)

        # Layout chính cho main_widget
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)

        # Tạo QTabWidget
        self.tab = QTabWidget(self.main_widget)
        self.tab.setStyleSheet("""
            QTabBar::tab:selected { 
                background: white; 
                border-bottom: 1px solid #0078D7;
                padding: 5px;
            }
        """)

        # Thêm các trang vào tab
        self.Profile_page = ProfileView(self)
        self.RecognitionStudent_page = RecognitionStudentView(self)
        self.StudentInformationManagement = StudentInformationManagement(self)
        self.SystemStatistics = SystemStatistics(self)

        self.tab.addTab(self.SystemStatistics, 'Thống kê')
        self.tab.addTab(self.StudentInformationManagement, 'Quản lí')
        self.tab.addTab(self.RecognitionStudent_page, 'Nhận diện')
        self.tab.addTab(self.Profile_page, 'Thông tin')

        # Thêm QTabWidget vào layout chính
        self.main_layout.addWidget(self.tab)

        # Đồng hồ cập nhật
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        self.update_time()
        self.show()

    def update_time(self):
        self.time_label.setText(QTime.currentTime().toString("hh:mm:ss"))
        self.date_label.setText(QDate.currentDate().toString("dd/MM/yyyy"))
