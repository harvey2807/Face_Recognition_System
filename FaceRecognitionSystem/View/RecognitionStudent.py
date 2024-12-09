import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, \
    QGridLayout, QTextEdit


class RecognitionStudentView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Main widget và layout chính
        self.main_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setStyleSheet("background-color: #F5F5F5;")
        self.main_widget.setGeometry(0,0, 1000, 570)

        # Grid Layout cho các phần
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        # Groupbox cho màn hình nhận diện
        self.recognition_group = QGroupBox("Màn hình nhận diện")
        self.recognition_group.setStyleSheet("""
                font-size: 16px; font-weight: bold;
                background-color: white; border: 1px solid black;
                border-radius: 5px;
            """)
        self.recognition_layout = QVBoxLayout()
        self.recognition_group.setLayout(self.recognition_layout)

        # Combobox để chọn lớp và loại điểm danh
        choose_layout = QHBoxLayout()
        self.course_label = QLabel("Chọn Lớp:")
        self.course_combo = QComboBox()
        self.course_combo.addItems(["Cấu trúc dữ liệu", "Python"])
        self.course_combo.setStyleSheet("padding: 5px; border: 1px solid gray;")

        self.class_label = QLabel("Chọn Buổi:")
        self.class_combo = QComboBox()
        self.class_combo.addItems(["1", "2", "3"])
        self.class_combo.setStyleSheet("padding: 5px; border: 1px solid gray;")

        self.attendance_label = QLabel("Loại Điểm Danh:")
        self.attendance_combo = QComboBox()
        self.attendance_combo.addItems(["Vào", "Ra"])
        self.attendance_combo.setStyleSheet("padding: 5px; border: 1px solid gray;")

        # Thêm vào layout chọn thông tin
        choose_layout.addWidget(self.course_label)
        choose_layout.addWidget(self.course_combo)
        choose_layout.addWidget(self.class_label)
        choose_layout.addWidget(self.class_combo)
        choose_layout.addWidget(self.attendance_label)
        choose_layout.addWidget(self.attendance_combo)

        # Camera feed
        self.camera_feed = QLabel()
        self.camera_feed.setPixmap(QPixmap("../Image/img.png").scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio))
        self.camera_feed.setStyleSheet("border: 1px solid blue; margin-top: 10px;")
        self.recognition_layout.addLayout(choose_layout)
        self.recognition_layout.addWidget(self.camera_feed)

        # Nút mở và đóng camera
        camera_buttons_layout = QHBoxLayout()
        self.open_camera_btn = QPushButton("Mở Camera")
        self.open_camera_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.close_camera_btn = QPushButton("Đóng Camera")
        self.close_camera_btn.setStyleSheet("background-color: #F44336; color: white; padding: 10px;")
        camera_buttons_layout.addWidget(self.open_camera_btn)
        camera_buttons_layout.addWidget(self.close_camera_btn)
        self.recognition_layout.addLayout(camera_buttons_layout)

        # Thêm màn hình nhận diện vào main layout
        self.main_layout.addWidget(self.recognition_group)

        # Thông tin điểm danh (Phần bên phải)
        attendance_group = QGroupBox("Điểm danh thành công")
        attendance_group.setStyleSheet("""
            border: 1px solid gray;""")
        attendance_layout = QVBoxLayout()
        attendance_group.setLayout(attendance_layout)

        # Hiển thị ảnh nhận diện
        self.detected_face = QLabel()
        self.detected_face.setPixmap(QPixmap("placeholder.png").scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        self.detected_face.setStyleSheet("border: 1px solid black;")
        attendance_layout.addWidget(self.detected_face, alignment=Qt.AlignmentFlag.AlignCenter)

        # Thông tin học sinh
        self.student_group = QGroupBox("Thông tin Học sinh")
        self.student_layout = QGridLayout()
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.time_input = QLineEdit()

        self.student_layout.addWidget(QLabel("ID Học sinh:"), 0, 0)
        self.student_layout.addWidget(self.id_input, 0, 1)
        self.student_layout.addWidget(QLabel("Tên Học sinh:"), 0, 2)
        self.student_layout.addWidget(self.name_input, 0, 3)
        self.student_layout.addWidget(QLabel("Thời gian:"), 1, 0)
        self.student_layout.addWidget(self.time_input, 1, 1)

        attendance_layout.addWidget(QLabel("ID Học sinh:"))
        attendance_layout.addWidget(self.id_input)
        attendance_layout.addWidget(QLabel("Tên Học sinh:"))
        attendance_layout.addWidget(self.name_input)
        attendance_layout.addWidget(QLabel("Thời gian:"))
        attendance_layout.addWidget(self.time_input)

        # Thông tin buổi học (Phần bên dưới)
        session_group = QGroupBox("Thông tin buổi học")
        session_layout = QVBoxLayout()
        session_group.setLayout(session_layout)

        self.class_info = QTextEdit()
        self.class_info.setReadOnly(True)
        self.class_info.setText("Lớp: 9A\nID Buổi học: 5\nThời gian: 7:00:00 - 11:30:00")
        session_layout.addWidget(self.class_info)

        # Thêm phần bên phải vào layout chính
        self.grid_layout.addWidget(self.recognition_group, 0, 0)
        # Thêm phần bên phải vào layout chính
        self.grid_layout.addWidget(attendance_group, 0, 1)
        # Thêm thông tin buổi học vào layout chính
        self.grid_layout.addWidget(session_group,0,1)



