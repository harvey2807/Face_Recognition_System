from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QVBoxLayout,
    QHBoxLayout, QGroupBox, QGridLayout, QHeaderView, QDateTimeEdit
)
from PyQt6.QtCore import Qt, QDate


class StudentInformationManagement(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        # Thiết lập tiêu đề và kích thước cửa sổ
        self.setWindowTitle("Quản lý thông tin Học sinh")
        self.setGeometry(100, 100, 1200, 700)

        # Định nghĩa CSS để tạo giao diện
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QTableWidget, QDateTimeEdit {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                border: 1px solid black;
                border-radius: 4px;
                padding: 8px;
                color white;           
            }
            QPushButton:hover {
                background-color: black;
                color: white;
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

        # Layout ngoài cùng chứa toàn bộ nội dung
        outer_layout = QVBoxLayout()

        # Tiêu đề chính
        header_label = QLabel("Thống kê hệ thống")
        header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Căn giữa tiêu đề
        header_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: black; margin: 0px; padding: 0px;"
        )
        outer_layout.addWidget(header_label)  # Thêm tiêu đề vào layout ngoài

        # Spacer nhỏ để tạo khoảng cách giữa tiêu đề và nội dung
        outer_layout.addSpacing(10)

        # Layout chính (chứa hai phần: thông tin học sinh và hệ thống tìm kiếm)
        main_layout = QHBoxLayout()

        # ----------- Phần thông tin học sinh (bên trái) -----------
        student_group = QGroupBox("Thông tin Học sinh")  # Nhóm chứa thông tin học sinh
        student_layout = QGridLayout()  # Layout dạng lưới

        # Các ô nhập liệu thông tin
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.class_input = QLineEdit()
        self.cmnd_input = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Nam", "Nữ"])  # Thêm tùy chọn "Nam" và "Nữ
        self.dob_input = QDateTimeEdit(self, calendarPopup=True)
        self.dob_input.setDate(QDate.currentDate())  # Ngày mặc định
        self.dob_input.setDisplayFormat("dd/MM/yyyy")  # Định dạng hiển thị

        calendar = self.dob_input.calendarWidget()
        calendar.setStyleSheet("""
            QCalendarWidget QTableView {
                selection-background-color: lightblue; /* Màu nền khi chọn */
                selection-color: black; /* Màu chữ khi chọn */
            }

            QCalendarWidget QTableView::item {
                color: black; /* Màu chữ mặc định của các ngày */
                background-color: white; /* Màu nền mặc định của các ngày */
            }

            QCalendarWidget QHeaderView::section {
                background-color: #1E90FF; /* Màu nền của hàng thứ */
                color: white; /* Màu chữ của hàng thứ */
                font-weight: bold;
                border: 1px solid #CCCCCC;
                padding: 5px;
            }
        """)

        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()

        # Thêm các thành phần nhập liệu vào lưới
        student_layout.addWidget(QLabel("ID Học sinh:"), 1, 0)
        student_layout.addWidget(self.id_input, 1, 1)
        student_layout.addWidget(QLabel("Tên Học sinh:"), 1, 2)
        student_layout.addWidget(self.name_input, 1, 3)
        student_layout.addWidget(QLabel("Lớp học:"), 2, 0)
        student_layout.addWidget(self.class_input, 2, 1)
        student_layout.addWidget(QLabel("CMND:"), 2, 2)
        student_layout.addWidget(self.cmnd_input, 2, 3)
        student_layout.addWidget(QLabel("Giới tính:"), 3, 0)
        student_layout.addWidget(self.gender_combo, 3, 1)
        student_layout.addWidget(QLabel("Ngày sinh:"), 3, 2)
        student_layout.addWidget(self.dob_input, 3, 3)
        student_layout.addWidget(QLabel("Email:"), 4, 0)
        student_layout.addWidget(self.email_input, 4, 1)
        student_layout.addWidget(QLabel("SĐT:"), 4, 2)
        student_layout.addWidget(self.phone_input, 4, 3)
        student_layout.addWidget(QLabel("Địa chỉ:"), 5, 0)
        student_layout.addWidget(self.address_input, 5, 1)

        # Các nút chức năng (Lưu, Sửa, Xóa)
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Lưu")
        self.save_button.setStyleSheet("background-color: black; color: white;")
        self.edit_button = QPushButton("Sửa")
        self.edit_button.setStyleSheet("background-color: black; color: white;")
        self.delete_button = QPushButton("Xóa")
        self.delete_button.setStyleSheet("background-color: black; color: white;")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        student_layout.addLayout(button_layout, 6, 0, 1, 4)  # Thêm hàng nút vào layout lưới
        student_group.setLayout(student_layout)  # Đặt layout cho nhóm

        # ----------- Phần hệ thống tìm kiếm (bên phải) -----------
        table_group = QGroupBox("Hệ Thống Tìm kiếm")  # Nhóm chứa bảng và chức năng tìm kiếm
        table_layout = QVBoxLayout()  # Layout dạng dọc

        # Thanh tìm kiếm
        self.search_combo = QComboBox()
        self.search_combo.addItems(["ID Học sinh"])  # Thêm tiêu chí tìm kiếm
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Tìm kiếm")
        self.view_all_button = QPushButton("Xem tất cả")
        self.table = QTableWidget(5, 3)  # Bảng chứa kết quả tìm kiếm
        self.table.setHorizontalHeaderLabels(["ID Học sinh", "Họ tên", "CMND"])  # Đặt tên các cột

        # Điều chỉnh kích thước các cột trong bảng
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Layout chứa thanh tìm kiếm
        table_search_layout = QHBoxLayout()
        table_search_layout.addWidget(QLabel("Tìm kiếm theo:"))
        table_search_layout.addWidget(self.search_combo)
        table_search_layout.addWidget(self.search_input)
        table_search_layout.addWidget(self.search_button)
        table_search_layout.addWidget(self.view_all_button)

        # Thêm thanh tìm kiếm và bảng vào layout
        table_layout.addLayout(table_search_layout)
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)  # Đặt layout cho nhóm

        # ----------- Thêm các phần vào layout chính -----------
        main_layout.addWidget(student_group, 2)  # Phần bên trái (thông tin học sinh)
        main_layout.addWidget(table_group, 2)  # Phần bên phải (hệ thống tìm kiếm)

        # Thêm layout chính vào outer_layout
        outer_layout.addLayout(main_layout)

        # Đặt outer_layout làm layout chính của cửa sổ
        self.setLayout(outer_layout)


# ----------- Chạy ứng dụng -----------
if __name__ == "__main__":
    app = QApplication([])  # Tạo ứng dụng
    window = StudentInformationManagement()  # Tạo cửa sổ chính
    window.show()  # Hiển thị cửa sổ
    exit(app.exec())  # Bắt đầu vòng lặp sự kiện
