from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QHeaderView, QFileDialog
)
from PyQt6.QtCore import Qt
import sys
import csv
class BaseTableWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        print('tao trang ..')
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
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ID Học sinh")
        self.search_input.setStyleSheet("border: 1px solid #CCCCCC;border-radius: 4px;padding: 5px;")

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
        search_button.clicked.connect(self.search_by_id)  # Kết nối nút tìm kiếm

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
        view_all_button.clicked.connect(self.view_all_rows)  # Hiển thị tất cả các hàng

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
        export_csv_button.clicked.connect(self.export_to_csv)  # Kết nối nút xuất CSV với hàm xử lý

        # Thêm các nút vào layout tìm kiếm
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(view_all_button)
        search_layout.addWidget(export_csv_button)
        layout.addLayout(search_layout)

        self.table = QTableWidget(10, 4)
        self.table.setHorizontalHeaderLabels(["ID SV", "Tên Học sinh", "Buổi", "Ngày"])

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

        # Hàm xử lý khi nhấn nút Xuất CSV.
        # Thực hiện việc ghi dữ liệu từ bảng ra tệp CSV.
    def export_to_csv(self):
        # Hiển thị hộp thoại để chọn vị trí lưu tệp CSV
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu tệp CSV", "", "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:  # Nếu người dùng chọn vị trí lưu tệp
            try:
                with open(file_path, mode="w", newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)

                    # Ghi tiêu đề cột vào tệp CSV
                    headers = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]
                    writer.writerow(headers)

                    # Ghi dữ liệu từng dòng vào tệp CSV
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)  # Lấy dữ liệu từng ô
                            row_data.append(item.text() if item else "")  # Nếu ô trống thì ghi chuỗi rỗng
                        writer.writerow(row_data)

                print(f"Dữ liệu đã được xuất thành công tại: {file_path}")
            except Exception as e:
                print(f"Lỗi khi xuất CSV: {e}")
        else:
            print("Người dùng đã hủy thao tác xuất CSV.")

    # Tìm kiếm trong bảng theo ID nhập vào.
    def search_by_id(self):
        search_text = self.search_input.text().strip()  # Lấy nội dung trong ô tìm kiếm
        if not search_text:
            print("Vui lòng nhập ID để tìm kiếm.")
            return
        found = False
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)  # Lấy giá trị ở cột đầu tiên (ID)
            if item and item.text() == search_text:
                self.table.setRowHidden(row, False)  # Hiển thị hàng phù hợp
                found = True
            else:
                self.table.setRowHidden(row, True)  # Ẩn các hàng không phù hợp
        if not found:
            print(f"Không tìm thấy ID: {search_text}")

    # Hiển thị lại tất cả các hàng.
    def view_all_rows(self):
        for row in range(self.table.rowCount()):
            self.table.setRowHidden(row, False)