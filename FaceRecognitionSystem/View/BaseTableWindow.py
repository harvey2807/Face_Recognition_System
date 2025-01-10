from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QHeaderView, QFileDialog
)
from PyQt6.QtCore import Qt
import sys
import openpyxl  # Thêm thư viện openpyxl để xuất dữ liệu ra Excel
from openpyxl import Workbook

class BaseTableWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(50, 40, 1200, 700)
        self.setup_ui(title)
        self.setStyleSheet("background-color: white; color:black;")
        self.searched_class_name = ""  # Thêm thuộc tính lưu tên lớp đã tìm kiếm

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
        self.search_input.setPlaceholderText("ID Học sinh hoặc tên lớp học")
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
        search_button.clicked.connect(self.search_by_id_or_class_name)  # Kết nối nút tìm kiếm

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

        export_excel_button = QPushButton("Xuất Excel")
        export_excel_button.setStyleSheet("""
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
        export_excel_button.clicked.connect(self.export_to_excel)  # Kết nối nút xuất excel với hàm xử lý

        # Thêm các nút vào layout tìm kiếm
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(view_all_button)
        search_layout.addWidget(export_excel_button)
        layout.addLayout(search_layout)

        self.table = QTableWidget(10, 5)
        self.table.setHorizontalHeaderLabels(["Tên lớp", "ID SV", "Tên Học sinh", "Buổi", "Ngày"])

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

    def export_to_excel(self):
        # Hiển thị hộp thoại để chọn vị trí lưu tệp Excel
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu tệp Excel", "", "Excel Files (*.xlsx);;All Files (*)"
        )

        if file_path:  # Nếu người dùng chọn vị trí lưu tệp
            try:
                workbook = Workbook()
                sheet = workbook.active
                sheet.title = "Dữ liệu học sinh"
                sheet.append(["STT", "Tên lớp", "ID SV", "Tên Học sinh", "Số buổi", "Ngày"])

                data_grouped = {}
                print(f"Lớp đã tìm kiếm: {self.searched_class_name}")

                for row in range(self.table.rowCount()):
                    if self.table.isRowHidden(row):
                        continue

                    class_name_item = self.table.item(row, 0)
                    id_item = self.table.item(row, 1)
                    name_item = self.table.item(row, 2)
                    session_item = self.table.item(row, 3)
                    date_item = self.table.item(row, 4)

                    # Bỏ qua nếu bất kỳ giá trị nào bị thiếu
                    if not class_name_item or not id_item or not name_item or not session_item or not date_item:
                        print(f"Bỏ qua hàng do thiếu dữ liệu ở hàng {row + 1}")
                        continue

                    class_name = class_name_item.text().strip()
                    student_id = id_item.text().strip()
                    student_name = name_item.text().strip()
                    session = session_item.text().strip()
                    date = date_item.text().strip()

                    # Kiểm tra lớp (không phân biệt chữ hoa/chữ thường)
                    if hasattr(self, 'searched_class_name') and self.searched_class_name:
                        if self.searched_class_name.strip().lower() != class_name.lower():
                            continue  # Bỏ qua lớp không phải lớp đang tìm kiếm

                    # Nhóm dữ liệu theo ID SV, Tên học sinh và Tên lớp
                    key = (class_name, student_id, student_name)
                    if key not in data_grouped:
                        data_grouped[key] = {"count": 0, "dates": []}
                    data_grouped[key]["count"] += 1
                    data_grouped[key]["dates"].append(date)

                    # Debug: In dữ liệu được thêm
                    print(f"Key thêm vào: {key}, Số buổi: {data_grouped[key]['count']}, Ngày: {data_grouped[key]['dates']}")

                if not data_grouped:
                    print(f"Không có dữ liệu phù hợp với lớp: {self.searched_class_name}")
                    return

                stt = 1
                for (class_name, student_id, student_name), data in data_grouped.items():
                    session_count = data["count"]
                    dates = ", ".join(data["dates"])
                    print(f"STT: {stt}, Lớp: {class_name}, ID: {student_id}, Tên: {student_name}, Số buổi: {session_count}, Ngày: {dates}")
                    sheet.append([stt, class_name, student_id, student_name, session_count, dates])
                    stt += 1

                workbook.save(file_path)
                print(f"Dữ liệu đã được xuất thành công tại: {file_path}")
            except Exception as e:
                print(f"Lỗi khi xuất Excel: {e}")
        else:
            print("Người dùng đã hủy thao tác xuất Excel.")




    def search_by_id_or_class_name(self):
        search_text = self.search_input.text().strip()  # Lấy nội dung tìm kiếm
        if not search_text:
            print("Vui lòng nhập ID hoặc Tên lớp để tìm kiếm.")
            return

        self.searched_class_name = search_text  # Lưu tên lớp tìm kiếm
        found = False
        for row in range(self.table.rowCount()):
            # Lấy giá trị ở cột Tên lớp (cột 0) và ID học sinh (cột 1)
            class_name_item = self.table.item(row, 0)
            id_item = self.table.item(row, 1)

            # Kiểm tra khớp với Tên lớp hoặc ID học sinh
            if (class_name_item and search_text.lower() in class_name_item.text().lower()) or (id_item and search_text == id_item.text()):
                self.table.setRowHidden(row, False)  # Hiển thị hàng phù hợp
                found = True
            else:
                self.table.setRowHidden(row, True)  # Ẩn hàng không phù hợp

        if not found:
            print(f"Không tìm thấy kết quả phù hợp với: {search_text}")

    def view_all_rows(self):
        self.searched_class_name = ""  # Reset khi xem lại tất cả
        for row in range(self.table.rowCount()):
            self.table.setRowHidden(row, False)


