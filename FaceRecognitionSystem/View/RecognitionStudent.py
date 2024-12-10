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
        self.main_widget.setGeometry(0, 0, 1160, 565)

        # Grid Layout cho các phần
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        # Groupbox cho màn hình nhận diện
        self.recognition_group = QGroupBox("Màn hình nhận diện")
        self.recognition_group.setStyleSheet("""
                font-size: 13px;
                background-color: white; border: 1px solid gray;
                border-radius: 5px;
                padding-top: -10px;
                padding: 10px;
            """)
        self.recognition_layout = QVBoxLayout()
        self.recognition_group.setLayout(self.recognition_layout)

        # Combobox để chọn lớp và loại điểm danh
        choose_layout = QHBoxLayout()
        self.course_label = QLabel("Chọn Lớp:")
        self.course_label.setStyleSheet("border: none")
        self.course_combo = QComboBox()
        self.course_combo.addItems(["Cấu trúc dữ liệu", "Python"])
        self.course_combo.setStyleSheet("padding: 5px; border: 1px solid gray;")

        self.class_label = QLabel("Chọn Buổi:")
        self.class_label.setStyleSheet("border: none")
        self.class_combo = QComboBox()
        self.class_combo.addItems(["1", "2", "3"])
        self.class_combo.setStyleSheet("padding: 5px; border: 1px solid gray;")

        self.attendance_label = QLabel("Loại Điểm Danh:")
        self.attendance_label.setStyleSheet("border: none")
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
        self.camera_feed.setStyleSheet("border: 1px solid blue; text-align: center;")
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
        self.grid_layout.addWidget(self.recognition_group, 0, 0)

        # Thông tin điểm danh (Phần bên phải)
        self.infor_content = QWidget(self.main_widget)
        self.infor_playout = QVBoxLayout(self.infor_content)

        self.attendance_group = QGroupBox("Điểm danh thành công")
        self.attendance_group.setStyleSheet("""
            border: 1px solid gray;
            background-color: white; border-radius: 5px;
            padding-top: 5px;
            padding-right: 5px;
            padding-bottom: 5px;""")
        self.attendance_layout = QGridLayout()
        self.attendance_group.setLayout(self.attendance_layout)

        # Hiển thị ảnh nhận diện
        self.detected_face = QLabel()
        self.detected_face.setPixmap(QPixmap("../Image/img.png").scaled(40, 30, Qt.AspectRatioMode.KeepAspectRatio))
        self.detected_face.setStyleSheet("border: 1px solid blue; text-align: center;")
        self.attendance_layout.addWidget(self.detected_face)

        self.id_label = QLabel("ID Học sinh:")
        self.id_label.setStyleSheet("border: none")
        self.id_input = QLineEdit()
        self.id_input.setStyleSheet("""
                    border: 1px solid #CCCCCC;
                    border-radius: 4px;
                    padding: 5px;
                    margin-bottom: 10px;
                """)

        self.name_label = QLabel("Tên Học sinh:")
        self.name_label.setStyleSheet("border: none")
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("""
                            border: 1px solid #CCCCCC;
                            border-radius: 4px;
                            padding: 5px;
                            margin-bottom: 10px;
                        """)

        self.time_label = QLabel("Thời gian:")
        self.time_label.setStyleSheet("border: none")
        self.time_input = QLineEdit()
        self.time_input.setStyleSheet("""
                            border: 1px solid #CCCCCC;
                            border-radius: 4px;
                            padding: 5px;
                            margin-bottom: 10px;
                        """)
        self.attendance_layout.addWidget(self.id_label, 0, 0)
        self.attendance_layout.addWidget(self.id_input, 0, 1)
        self.attendance_layout.addWidget(self.name_label, 1, 0)
        self.attendance_layout.addWidget(self.name_input, 1, 1)
        self.attendance_layout.addWidget(self.time_label, 2, 0)
        self.attendance_layout.addWidget(self.time_input, 2, 1)

        # Thêm groupbox vào layout chính
        self.infor_playout.addWidget(self.attendance_group)

        # Thông tin buổi học (Phần bên dưới)
        session_group = QGroupBox("Thông tin buổi học")
        session_group.setStyleSheet("""
            border: 1px solid gray;
            background-color: white; border-radius: 5px;
            padding-top: 5px;
            padding-bottom: 5px;""")
        session_layout = QVBoxLayout()
        session_group.setLayout(session_layout)

        self.class_info = QTextEdit()
        self.class_info.setStyleSheet("border: none")
        self.class_info.setText("Lớp: Cấu trúc dữ liệu\nID Buổi học: 5\nThời gian: 7:00:00 - 11:30:00")
        session_layout.addWidget(self.class_info)

        # Thêm groupbox thông tin buổi học vào layout
        self.infor_playout.addWidget(session_group)

        # Thêm phần layout vào widget chính
        self.grid_layout.addWidget(self.infor_content, 0, 1)

        # Đặt tỷ lệ kích thước cho các cột
        self.grid_layout.setColumnStretch(0, 2)  # recognition_group chiếm 2 phần
        self.grid_layout.setColumnStretch(1, 1)  # infor_content chiếm 1 phần






