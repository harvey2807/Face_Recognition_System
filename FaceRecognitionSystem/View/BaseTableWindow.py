from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QHeaderView
)
from PyQt6.QtCore import Qt
import sys

class BaseTableWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(50, 40, 1200, 700)
        self.setup_ui(title)
        self.setStyleSheet("background-color: white; color:black;")

    def setup_ui(self, title):
        layout = QVBoxLayout()
        layout.addSpacing(20)
        header_label = QLabel(title)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        layout.addWidget(header_label)

        # Tạo thanh tìm kiếm
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("ID Học sinh")
        search_input.setStyleSheet("border: 1px solid #CCCCCC;border-radius: 4px;padding: 5px;")

        # Nút tìm kiếm
        search_button = QPushButton("Tìm kiếm")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #333333;
                color: white;
            }
        """)

        view_all_button = QPushButton("Xem tất cả")
        view_all_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #333333;
                color: white;
            }
        """)

        export_csv_button = QPushButton("Xuất CSV")
        export_csv_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #333333;
                color: white;
            }
        """)

        # Thêm các nút vào layout tìm kiếm
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(view_all_button)
        search_layout.addWidget(export_csv_button)
        layout.addLayout(search_layout)

        self.table = QTableWidget(10, 4)
        self.table.setHorizontalHeaderLabels(["ID SV", "Tên Học sinh", "Lớp học", "Ngày"])

        data = [
            ["SV001", "Nguyễn Văn A", "Lớp 1", "01/12/2024"],
            ["SV002", "Trần Thị B", "Lớp 2", "02/12/2024"],
            ["SV003", "Phạm Minh C", "Lớp 3", "03/12/2024"],
            ["SV004", "Lê Thi D", "Lớp 4", "04/12/2024"],
            ["SV005", "Hoàng Quân E", "Lớp 1", "05/12/2024"],
            ["SV006", "Vũ Thị F", "Lớp 2", "06/12/2024"],
            ["SV007", "Đặng Thị G", "Lớp 3", "07/12/2024"],
            ["SV008", "Bùi Minh H", "Lớp 4", "08/12/2024"],
            ["SV009", "Ngô Thị I", "Lớp 1", "09/12/2024"],
            ["SV010", "Dương Văn J", "Lớp 2", "10/12/2024"]
        ]

        # Điền dữ liệu vào bảng
        for i in range(10):
            for j in range(4):
                self.table.setItem(i, j, QTableWidgetItem(data[i][j]))

        # Thêm bảng vào layout
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Điều chỉnh kích thước các cột trong bảng
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        container = QWidget()
        container.setLayout(layout)
        self.setLayout(layout)  # Đặt layout vào widget cha

