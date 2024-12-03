from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QRadioButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QGroupBox, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt


class StudentInformationManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý thông tin Học sinh")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QTableWidget, QTextEdit {
                border: 1px solid black;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid black;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #dcdcdc;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid gray;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                padding: 4px;
            }
        """)

        # Layout chính
        main_layout = QVBoxLayout()

        # Phần tiêu đề
        title_label = QLabel("Quản lý thông tin Học sinh")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Layout phân chia theo cột
        grid_layout = QGridLayout()

        # Phần thông tin khóa học (bên trái trên)
        course_group = QGroupBox("Thông tin Khóa học")
        course_layout = QGridLayout()
        self.year_combo = QComboBox()
        self.year_combo.addItems(["2022", "2023", "2024"])
        self.base_combo = QComboBox()
        self.base_combo.addItems(["1", "2", "3"])

        # Điều chỉnh chiều cao của các widget trong phần thông tin khóa học
        self.year_combo.setMinimumHeight(30)
        self.base_combo.setMinimumHeight(30)

        course_layout.addWidget(QLabel("Khóa học:"), 0, 0)
        course_layout.addWidget(self.year_combo, 0, 1)
        course_layout.addWidget(QLabel("Cơ sở:"), 0, 2)
        course_layout.addWidget(self.base_combo, 0, 3)

        course_group.setLayout(course_layout)

        # Phần thông tin học sinh (bên trái dưới cùng)
        student_group = QGroupBox("Thông tin Học sinh")
        student_layout = QGridLayout()
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.class_input = QLineEdit()
        self.cmnd_input = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Nam", "Nữ"])
        self.dob_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()
        self.photo_yes = QRadioButton("Có ảnh")
        self.photo_no = QRadioButton("Không ảnh")

        student_layout.addWidget(QLabel("ID Học sinh:"), 0, 0)
        student_layout.addWidget(self.id_input, 0, 1)
        student_layout.addWidget(QLabel("Tên Học sinh:"), 0, 2)
        student_layout.addWidget(self.name_input, 0, 3)
        student_layout.addWidget(QLabel("Lớp học:"), 1, 0)
        student_layout.addWidget(self.class_input, 1, 1)
        student_layout.addWidget(QLabel("CMND:"), 1, 2)
        student_layout.addWidget(self.cmnd_input, 1, 3)
        student_layout.addWidget(QLabel("Giới tính:"), 2, 0)
        student_layout.addWidget(self.gender_combo, 2, 1)
        student_layout.addWidget(QLabel("Ngày sinh:"), 2, 2)
        student_layout.addWidget(self.dob_input, 2, 3)
        student_layout.addWidget(QLabel("Email:"), 3, 0)
        student_layout.addWidget(self.email_input, 3, 1)
        student_layout.addWidget(QLabel("SĐT:"), 3, 2)
        student_layout.addWidget(self.phone_input, 3, 3)
        student_layout.addWidget(QLabel("Địa chỉ:"), 4, 0)
        student_layout.addWidget(self.address_input, 4, 1)
        student_layout.addWidget(self.photo_yes, 4, 2)
        student_layout.addWidget(self.photo_no, 4, 3)

        # Các nút Lưu, Sửa, Xóa ở hàng ngang
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Lưu")
        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        student_layout.addLayout(button_layout, 5, 0, 1, 4)

        student_group.setLayout(student_layout)

        # Phần hệ thống tìm kiếm (bên phải trên)
        table_group = QGroupBox("Hệ Thống Tìm kiếm")
        table_layout = QVBoxLayout()
        self.search_combo = QComboBox()
        self.search_combo.addItems(["ID Học sinh", "Khóa", "Cơ sở"])
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Tìm kiếm")
        self.view_all_button = QPushButton("Xem tất cả")
        self.table = QTableWidget(5, 5)
        self.table.setHorizontalHeaderLabels(["ID Học sinh", "Khóa", "Cơ sở", "Họ tên", "CMND"])

        table_search_layout = QHBoxLayout()
        table_search_layout.addWidget(QLabel("Tìm kiếm theo:"))
        table_search_layout.addWidget(self.search_combo)
        table_search_layout.addWidget(self.search_input)
        table_search_layout.addWidget(self.search_button)
        table_search_layout.addWidget(self.view_all_button)

        table_layout.addLayout(table_search_layout)
        table_layout.addWidget(self.table)

        table_group.setLayout(table_layout)

        # Phần quản lý lớp học (bên phải dưới)
        class_group = QGroupBox("Quản lý lớp học")
        class_layout = QGridLayout()
        self.class_list = QComboBox()
        self.class_list.addItems(["9A", "9B", "9C"])
        self.search_class_button = QPushButton("Tìm kiếm")
        self.view_all_class_button = QPushButton("Xem tất cả")
        self.class_name_input = QLineEdit()
        self.class_id_input = QLineEdit()
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)  # Chỉ đọc

        class_layout.addWidget(QLabel("Lớp:"), 0, 0)
        class_layout.addWidget(self.class_list, 0, 1)
        class_layout.addWidget(self.search_class_button, 0, 2)
        class_layout.addWidget(self.view_all_class_button, 0, 3)
        class_layout.addWidget(QLabel("Mã lớp:"), 1, 0)
        class_layout.addWidget(self.class_id_input, 1, 1)
        class_layout.addWidget(QLabel("Tên lớp:"), 1, 2)
        class_layout.addWidget(self.class_name_input, 1, 3)
        class_layout.addWidget(QLabel("Kết quả:"), 2, 0)
        class_layout.addWidget(self.result_text, 3, 0, 1, 4)

        # Thêm các nút Sửa và Xóa
        update_button_layout = QHBoxLayout()
        self.update_class_button = QPushButton("Sửa")
        self.delete_class_button = QPushButton("Xóa")
        update_button_layout.addWidget(self.update_class_button)
        update_button_layout.addWidget(self.delete_class_button)
        class_layout.addLayout(update_button_layout, 4, 0, 1, 4)

        class_group.setLayout(class_layout)

        # Thêm các phần vào layout chính
        grid_layout.addWidget(course_group, 0, 0)
        grid_layout.addWidget(student_group, 1, 0)
        grid_layout.addWidget(table_group, 0, 1)
        grid_layout.addWidget(class_group, 1, 1)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication([])
    window = StudentInformationManagement()
    window.show()
    exit(app.exec())
