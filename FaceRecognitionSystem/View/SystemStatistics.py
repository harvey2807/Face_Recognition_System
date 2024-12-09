import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from FaceRecognitionSystem.View.BaseTableWindow import LateWindow, AbsentWindow, NoAttendanceWindow


class SystemStatistics(QMainWindow):
    def __init__(self,stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        # Cài đặt tiêu đề và kích thước cửa sổ chính
        self.setWindowTitle("Thống kê hệ thống")
        self.setGeometry(100, 100, 1200, 700)
        self.setup_ui()  # Gọi hàm thiết lập giao diện
        self.center_window()
        self.setStyleSheet("background-color: white; color:black;")  # Đặt màu nền và màu chữ

    def setup_ui(self):
        # Tạo layout chính
        main_layout = QVBoxLayout()

        # Thêm biểu đồ với viền
        chart_widget = self.create_chart_with_border()
        main_layout.addWidget(chart_widget)

        # Tạo layout cho các nút
        button_layout = QHBoxLayout()
        late_button = self.create_hover_button("Học sinh đi muộn")  # Nút "Học sinh đi muộn"
        late_button.clicked.connect(self.open_late_window)  # Kết nối nút với phương thức mở cửa sổ LateWindow
        absent_button = self.create_hover_button("Học sinh vắng")  # Nút "Học sinh vắng"
        absent_button.clicked.connect(self.open_absent_window)  # Kết nối nút với phương thức mở cửa sổ AbsentWindow
        no_attendance_button = self.create_hover_button("Học sinh đã điểm danh")  # Nút "Học sinh đã điểm danh"
        no_attendance_button.clicked.connect(
            self.open_no_attendance_window)  # Kết nối nút với phương thức mở cửa sổ NoAttendanceWindow
        button_layout.addWidget(late_button)
        button_layout.addWidget(absent_button)
        button_layout.addWidget(no_attendance_button)
        main_layout.addLayout(button_layout)  # Thêm layout các nút vào layout chính

        # Tạo widget trung tâm và đặt layout chính cho nó
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)  # Đặt widget trung tâm cho cửa sổ chính

    def center_window(self):
        # Lấy thông tin khung của cửa sổ
        frame_geometry = self.frameGeometry()
        # Lấy màn hình chính (màn hình đầu tiên)
        screen = QApplication.primaryScreen()
        # Lấy trung tâm của màn hình
        screen_center = screen.availableGeometry().center()
        # Đặt khung cửa sổ sao cho nó nằm ở giữa màn hình
        frame_geometry.moveCenter(screen_center)
        # Đặt vị trí của cửa sổ
        self.move(frame_geometry.topLeft())

    def create_chart_with_border(self):
        """Tạo một container chứa biểu đồ với viền và hiệu ứng."""
        # Tạo một QFrame để chứa biểu đồ
        chart_container = QFrame()
        chart_container.setStyleSheet("""
            QFrame {
                background-color: #ffffff; /* Nền trắng */
                border: 2px solid #4faaff; /* Viền xanh dương */
                border-radius: 10px;      /* Bo góc */
                padding: 10px;           /* Khoảng cách nội dung */
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Hiệu ứng bóng */
            }
        """)

        # Thêm biểu đồ vào container
        chart_layout = QVBoxLayout()
        chart = self.create_area_chart()  # Gọi hàm tạo biểu đồ
        chart_layout.addWidget(chart)
        chart_container.setLayout(chart_layout)

        return chart_container  # Trả về container chứa biểu đồ

    def create_area_chart(self):
        """Tạo biểu đồ dạng vùng (area chart) với phong cách mềm mại."""
        # Tạo đối tượng Figure từ matplotlib
        figure = Figure(figsize=(10, 6))
        ax = figure.add_subplot(111)

        # Dữ liệu mẫu
        x = ["Buổi 1", "Buổi2", "Buổi 3", "Buổi 4", "Buổi 5"]
        sumst = [10, 30, 25, 20, 15]  # Tổng số học sinh
        miss = [15, 25, 20, 30, 10]   # Số lần vắng
        dd = [40, 15, 10, 25, 20]     # Số bản điểm danh

        # Vẽ biểu đồ dạng vùng
        ax.fill_between(x, sumst, color="#80bfff", alpha=0.7, label="Số học sinh")
        ax.fill_between(x, miss, color="#ffcc80", alpha=0.7, label="Số lần vắng")
        ax.fill_between(x, dd, color="#b3ff80", alpha=0.7, label="Số bản điểm danh")

        # Hiển thị giá trị lên các điểm dữ liệu
        for i, value in enumerate(sumst):
            ax.text(i, value + 2, f"{value}", color="#ffffff", fontsize=9, ha="center", va="bottom")
        for i, value in enumerate(miss):
            ax.text(i, value + 2, f"{value}", color="#ffffff", fontsize=9, ha="center", va="bottom")
        for i, value in enumerate(dd):
            ax.text(i, value + 2, f"{value}", color="#ffffff", fontsize=9, ha="center", va="bottom")

        # Cài đặt tiêu đề, trục và phong cách
        ax.set_title("Thống kê hệ thống", fontsize=18, fontweight="bold", color="#ffffff", pad=20)
        ax.set_ylabel("Số lần", fontsize=12, color="#ffffff", labelpad=10)
        ax.set_xlabel("Buổi", fontsize=12, color="#ffffff", labelpad=10)
        ax.tick_params(axis="both", colors="#ffffff", labelsize=10)
        ax.legend(loc="upper right", fontsize=10, facecolor="#4a4a4a", edgecolor="none", labelcolor="white")

        # Cài đặt nền và lưới
        ax.set_facecolor("#323a4a")  # Nền cho biểu đồ
        figure.set_facecolor("#2e3b4e")  # Nền cho toàn bộ figure
        ax.grid(color="#ffffff", linestyle="--", linewidth=0.5, alpha=0.3)

        # Căn chỉnh khoảng cách và bo góc
        figure.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.9)

        # Nhúng biểu đồ vào PyQt
        canvas = FigureCanvas(figure)
        return canvas

    def create_hover_button(self, text):
        """Tạo một nút với hiệu ứng hover."""
        button = QPushButton(text)  # Tạo nút
        button.setFixedSize(200, 50)  # Đặt kích thước cố định
        button.setStyleSheet("""
            QPushButton {
                font-size: 16px; /* Kích thước font */
                padding: 10px; /* Khoảng cách nội dung */
                background-color: #333333; /* Màu nền */
                color: white; /* Màu chữ */
                border: none; /* Không viền */
                border-radius: 5px; /* Bo góc */
                transition: all 0.3s; /* Hiệu ứng chuyển đổi */
            }
            QPushButton:hover {
                background-color: #555555; /* Đổi màu khi hover */
                transform: scale(1.05); /* Tăng kích thước nhẹ khi hover */
            }
        """)
        return button  # Trả về nút đã tạo

    def open_late_window(self):
        self.late_window = LateWindow()
        self.late_window.show()

    def open_absent_window(self):
        self.absent_window = AbsentWindow()
        self.absent_window.show()

    def open_no_attendance_window(self):
        self.no_attendance_window = NoAttendanceWindow()
        self.no_attendance_window.show()

if __name__ == "__main__":
    # Khởi chạy ứng dụng
    app = QApplication(sys.argv)
    window = SystemStatistics()  # Tạo đối tượng cửa sổ chính
    window.show()  # Hiển thị cửa sổ
    sys.exit(app.exec())  # Thoát ứng dụng khi đóng cửa sổ
