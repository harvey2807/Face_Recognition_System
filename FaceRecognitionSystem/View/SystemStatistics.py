from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt
import sys


class SystemStatistics(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thống kê hệ thống")  # Đặt tiêu đề cửa sổ
        self.setGeometry(100, 100, 1200, 700)  # Đặt kích thước và vị trí cửa sổ
        self.setup_ui()  # Gọi phương thức setup_ui để tạo giao diện

    def setup_ui(self):
        # Tạo layout chính theo chiều dọc (VBox)
        main_layout = QVBoxLayout()

        # Phần tiêu đề
        header_label = QLabel("Thống kê hệ thống")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa tiêu đề
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")  # Đặt kiểu cho tiêu đề
        main_layout.addWidget(header_label)  # Thêm tiêu đề vào layout

        # Phần thống kê tổng quát
        summary_layout = QHBoxLayout()  # Layout theo chiều ngang
        # Thêm các thẻ thống kê vào layout ngang
        summary_layout.addWidget(self.create_summary_card("Số Học sinh", "12", "#4faaff"))
        summary_layout.addWidget(self.create_summary_card("Số bản điểm danh", "1", "#3cd17f"))
        summary_layout.addWidget(self.create_summary_card("Số lần đi muộn", "1", "#9753cc"))
        summary_layout.addWidget(self.create_summary_card("Số lần vắng", "42", "#e44352"))
        main_layout.addLayout(summary_layout)  # Thêm layout vào main_layout

        # Phần bảng chi tiết
        details_layout = QGridLayout()  # Layout dạng lưới

        # Thêm các bảng chi tiết vào layout
        details_layout.addWidget(self.create_table_section("Học sinh đi muộn"), 0, 0)
        details_layout.addWidget(self.create_table_section("Học sinh vắng"), 1, 0)
        details_layout.addWidget(self.create_table_section("Học sinh không điểm danh"), 0, 1, 2, 1)

        main_layout.addLayout(details_layout)  # Thêm layout chi tiết vào main_layout

        # Cài đặt layout chính của cửa sổ
        container = QWidget()
        container.setLayout(main_layout)  # Gán layout chính cho container
        self.setCentralWidget(container)  # Đặt container làm widget trung tâm của cửa sổ

        # Đặt màu nền của cửa sổ chính là trắng và chữ màu đen
        self.setStyleSheet("background-color: white; color: black;")

    def create_summary_card(self, title, value, color):
        """
        Tạo thẻ thống kê tổng quát với tiêu đề, giá trị và màu nền chỉ định.
        :param title: Tiêu đề thẻ (ví dụ: "Số Học sinh")
        :param value: Giá trị thẻ (ví dụ: "12")
        :param color: Màu nền của thẻ
        :return: QWidget chứa thẻ thống kê
        """
        card = QWidget()
        layout = QVBoxLayout()  # Layout theo chiều dọc trong thẻ
        card.setStyleSheet(f"background-color: {color};  border-radius: 10px; padding: 10px;")  # Đặt kiểu cho thẻ
        card.setFixedSize(200, 100)  # Đặt kích thước cố định cho thẻ

        title_label = QLabel(title)  # Tạo nhãn tiêu đề cho thẻ
        title_label.setStyleSheet("font-size: 16px; color: white;")  # Đặt kiểu cho tiêu đề
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa tiêu đề

        value_label = QLabel(value)  # Tạo nhãn giá trị cho thẻ
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")  # Đặt kiểu cho giá trị
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa giá trị

        layout.addWidget(title_label)  # Thêm tiêu đề vào layout
        layout.addWidget(value_label)  # Thêm giá trị vào layout
        card.setLayout(layout)  # Gán layout vào thẻ

        return card  # Trả về thẻ thống kê

    def create_table_section(self, section_title):
        """
        Tạo phần bảng chi tiết với tiêu đề và bảng dữ liệu.
        :param section_title: Tiêu đề của phần bảng (ví dụ: "Học sinh đi muộn")
        :return: QWidget chứa bảng chi tiết
        """
        section_widget = QWidget()  # Tạo widget chứa bảng
        layout = QVBoxLayout()  # Layout theo chiều dọc

        # Tạo nhãn tiêu đề cho bảng
        title_label = QLabel(section_title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")  # Đặt kiểu cho tiêu đề
        layout.addWidget(title_label)  # Thêm tiêu đề vào layout

        # Tạo layout tìm kiếm với trường nhập liệu và các nút bấm
        search_layout = QHBoxLayout()  # Layout theo chiều ngang cho các nút
        search_input = QLineEdit()  # Trường nhập liệu
        search_input.setPlaceholderText("ID Học sinh")  # Đặt placeholder cho trường nhập liệu
        search_button = QPushButton("Tìm kiếm")  # Nút tìm kiếm
        view_all_button = QPushButton("Xem tất cả")  # Nút xem tất cả
        export_csv_button = QPushButton("Xuất CSV")  # Nút xuất CSV
        search_layout.addWidget(search_input)  # Thêm trường nhập liệu vào layout
        search_layout.addWidget(search_button)  # Thêm nút tìm kiếm vào layout
        search_layout.addWidget(view_all_button)  # Thêm nút xem tất cả vào layout
        search_layout.addWidget(export_csv_button)  # Thêm nút xuất CSV vào layout
        layout.addLayout(search_layout)  # Thêm layout tìm kiếm vào layout chính

        # Tạo bảng hiển thị dữ liệu
        table = QTableWidget()  # Tạo bảng
        table.setColumnCount(5)  # Đặt số cột trong bảng
        table.setHorizontalHeaderLabels(["ID SV", "Tên Học sinh", "Lớp học", "Ngày", "Trạng thái"])  # Đặt tiêu đề cột
        table.setRowCount(10)  # Đặt số dòng trong bảng
        for i in range(10):  # Thêm dữ liệu giả vào bảng
            for j in range(5):
                table.setItem(i, j, QTableWidgetItem(f"Dữ liệu {i+1},{j+1}"))
        table.setStyleSheet("border: 1px solid black;")  # Thêm border cho bảng

        layout.addWidget(table)  # Thêm bảng vào layout

        section_widget.setLayout(layout)  # Gán layout vào widget chứa bảng
        return section_widget  # Trả về widget chứa bảng chi tiết


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Khởi tạo ứng dụng
    window = SystemStatistics()  # Khởi tạo cửa sổ thống kê
    window.show()  # Hiển thị cửa sổ
    sys.exit(app.exec())  # Chạy ứng dụng và thoát khi đóng cửa sổ
